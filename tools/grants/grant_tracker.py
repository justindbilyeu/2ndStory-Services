#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2nd Story Services - Grant & Funding Tracker
Tracks opportunities, calculates potential based on planned hires,
flags urgent deadlines, and exports partner-facing summaries.
"""

from __future__ import annotations
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import argparse
from typing import Dict, List

TEMPLATE_HEADERS = [
    "program_name","agency","priority","amount_min","amount_max",
    "populations","deadline","status","complexity",
    "requires_partnership","infrastructure_needed","realistic_timeline","notes"
]

TEMPLATE_EXAMPLES = [
    {
        "program_name":"Work Opportunity Tax Credit (WOTC)",
        "agency":"IRS/TWC",
        "priority":"5",
        "amount_min":"2400",
        "amount_max":"9600",
        "populations":"veterans,reentry,recovery,public_assistance",
        "deadline":"rolling",
        "status":"research",
        "complexity":"medium",
        "requires_partnership":"no",
        "infrastructure_needed":"Add Form 8850 to hiring packet; track hours 120/400; file Form 5884 at tax time",
        "realistic_timeline":"immediate",
        "notes":"Per-hire credit; submit Form 8850 within 28 days of hire"
    },
    {
        "program_name":"Apprenticeship Tax Refund (TX)",
        "agency":"State of Texas",
        "priority":"3",
        "amount_min":"2500",
        "amount_max":"2500",
        "populations":"veterans,reentry,recovery",
        "deadline":"rolling",
        "status":"watching",
        "complexity":"high",
        "requires_partnership":"yes",
        "infrastructure_needed":"DOL-registered apprenticeship; partner training provider",
        "realistic_timeline":"2-3 months",
        "notes":"Amount per apprentice; confirm current program rules"
    },
    {
        "program_name":"Texas Skills Development Fund",
        "agency":"TWC",
        "priority":"3",
        "amount_min":"50000",
        "amount_max":"500000",
        "populations":"veterans,reentry,recovery,women",
        "deadline":"rolling",
        "status":"watching",
        "complexity":"high",
        "requires_partnership":"yes",
        "infrastructure_needed":"Community college partner (e.g., ACC); proposal development",
        "realistic_timeline":"3-6 months",
        "notes":"Training grant via college partner; use pilot data in application"
    }
]

@dataclass
class Opportunity:
    program_name: str
    agency: str
    priority: int
    amount_min: int
    amount_max: int
    populations: str
    deadline: str
    status: str
    complexity: str
    requires_partnership: str
    infrastructure_needed: str
    realistic_timeline: str
    notes: str

class GrantTracker:
    def __init__(self, csv_path: str = "data/grant-opportunities.csv"):
        self.csv_path = Path(csv_path)
        self.opportunities: List[Opportunity] = []

    def load(self) -> None:
        if not self.csv_path.exists():
            print(f"Creating new tracker at {self.csv_path}")
            self._create_template()
        with self.csv_path.open("r", newline="") as f:
            reader = csv.DictReader(f)
            self.opportunities = []
            for row in reader:
                try:
                    self.opportunities.append(
                        Opportunity(
                            program_name=row["program_name"].strip(),
                            agency=row["agency"].strip(),
                            priority=int(row["priority"] or 0),
                            amount_min=int(row["amount_min"] or 0),
                            amount_max=int(row["amount_max"] or 0),
                            populations=row["populations"].strip(),
                            deadline=row["deadline"].strip(),
                            status=row["status"].strip(),
                            complexity=row["complexity"].strip(),
                            requires_partnership=row.get("requires_partnership","no").strip(),
                            infrastructure_needed=row.get("infrastructure_needed","").strip(),
                            realistic_timeline=row.get("realistic_timeline","").strip(),
                            notes=row["notes"].strip(),
                        )
                    )
                except Exception as e:
                    print(f"Skipping row due to error: {e}\nRow: {row}")

    def _create_template(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        with self.csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=TEMPLATE_HEADERS)
            writer.writeheader()
            for ex in TEMPLATE_EXAMPLES:
                writer.writerow(ex)

    def calculate_potential(self, workers_by_population: Dict[str,int]) -> Dict:
        total_min = 0
        total_max = 0
        breakdown = []
        for opp in self.opportunities:
            if opp.status in {"dead","rejected"}:
                continue
            pops = [p.strip() for p in opp.populations.split(",") if p.strip()]
            applicable_workers = sum(workers_by_population.get(p,0) for p in pops)
            if applicable_workers <= 0:
                continue
            per_hire = ("per-hire" in opp.notes.lower()) or ("per hire" in opp.notes.lower()) or (opp.program_name.lower().startswith("work opportunity"))
            if per_hire:
                opp_min = opp.amount_min * applicable_workers
                opp_max = opp.amount_max * applicable_workers
            else:
                opp_min = opp.amount_min
                opp_max = opp.amount_max
            total_min += opp_min
            total_max += opp_max
            breakdown.append({
                "program": opp.program_name,
                "workers": applicable_workers,
                "min": opp_min,
                "max": opp_max,
                "priority": opp.priority,
                "status": opp.status
            })
        breakdown.sort(key=lambda x: x["priority"], reverse=True)
        return {"total_min": total_min, "total_max": total_max, "breakdown": breakdown}

    def urgent_deadlines(self, days: int = 30) -> List[Dict]:
        urgent = []
        today = datetime.now()
        for opp in self.opportunities:
            if opp.deadline.lower() == "rolling":
                continue
            try:
                deadline = datetime.strptime(opp.deadline, "%Y-%m-%d")
            except ValueError:
                continue
            days_until = (deadline - today).days
            if 0 <= days_until <= days:
                urgent.append({
                    "program": opp.program_name,
                    "deadline": opp.deadline,
                    "days_until": days_until,
                    "priority": opp.priority,
                    "status": opp.status
                })
        urgent.sort(key=lambda x: x["days_until"])
        return urgent

    def partner_talking_points(self, workers_by_population: Dict[str,int]) -> str:
        p = self.calculate_potential(workers_by_population)
        lines = []
        lines.append("=== FUNDING TALKING POINTS ===")
        lines.append(f"Total Potential: ${p['total_min']:,} - ${p['total_max']:,}")
        lines.append("Top Opportunities:")
        for item in p["breakdown"][:5]:
            lines.append(f"  • {item['program']}: ${item['min']:,}-${item['max']:,} ({item['workers']} workers, Priority {item['priority']})")
        lines.append("")
        lines.append("When partners refer candidates, we can potentially capture:")
        for pop, count in workers_by_population.items():
            pop_total = 0
            for opp in self.opportunities:
                if opp.status in {"dead","rejected"}: 
                    continue
                if pop in [p.strip() for p in opp.populations.split(",")]:
                    if ("per-hire" in opp.notes.lower()) or ("per hire" in opp.notes.lower()) or (opp.program_name.lower().startswith("work opportunity")):
                        pop_total += opp.amount_max
            if pop_total > 0 and count > 0:
                lines.append(f"  • {count} {pop} workers → up to ${pop_total:,} in credits/grants (program-dependent)")
        return "\n".join(lines)

    def action_summary(self) -> str:
        by_status: Dict[str, List[Opportunity]] = {}
        for opp in self.opportunities:
            by_status.setdefault(opp.status, []).append(opp)
        order = ["urgent","ready_to_file","research","pending_grok","watching"]
        lines = ["=== ACTION SUMMARY ==="]
        for status in order:
            if status in by_status:
                lines.append(f"\n{status.upper().replace('_',' ')} ({len(by_status[status])}):")
                for o in by_status[status]:
                    lines.append(f"  • {o.program_name} (Priority {o.priority})")
        return "\n".join(lines)

    def export_partner_sheet(self, workers_by_population: Dict[str,int], output_path: str = "data/funding-summary.md") -> Path:
        p = self.calculate_potential(workers_by_population)
        urgent = self.urgent_deadlines(30)
        out = []
        out.append("# 2nd Story Services - Funding Summary")
        out.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        out.append("## Total Potential Funding")
        out.append(f"**${p['total_min']:,} - ${p['total_max']:,}**\n")
        out.append("## By Program\n")
        out.append("| Program | Workers | Amount | Priority | Status |")
        out.append("|---------|---------|--------|----------|--------|")
        for item in p["breakdown"]:
            out.append(f"| {item['program']} | {item['workers']} | ${item['min']:,}-${item['max']:,} | {item['priority']} | {item['status']} |")
        if urgent:
            out.append("\n## Urgent Deadlines (Next 30 Days)\n")
            out.append("| Program | Deadline | Days Until | Priority |")
            out.append("|---------|----------|------------|----------|")
            for u in urgent:
                out.append(f"| {u['program']} | {u['deadline']} | {u['days_until']} | {u['priority']} |")
        out.append("\n## Partner Value Proposition\n")
        out.append("When your organization refers candidates to 2nd Story Services, we can potentially capture credits/grants that are reinvested into supports (transport, training):\n")
        for pop, count in workers_by_population.items():
            matches = [o for o in self.opportunities if pop in o.populations and o.status not in {"dead","rejected"}]
            if matches and count > 0:
                out.append(f"**{pop.title()} ({count} workers):**")
                for o in matches[:3]:
                    out.append(f"- {o.program_name}: ${o.amount_min:,}-${o.amount_max:,} ({o.realistic_timeline})")
                out.append("")  # blank line
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(out), encoding="utf-8")
        return output

def main():
    parser = argparse.ArgumentParser(description="2nd Story Services Grants Tracker")
    parser.add_argument("--csv", default="data/grant-opportunities.csv", help="Path to opportunities CSV")
    parser.add_argument("--export", default="data/funding-summary.md", help="Output markdown path")
    parser.add_argument("--vets", type=int, default=2)
    parser.add_argument("--recovery", type=int, default=3)
    parser.add_argument("--women", type=int, default=2)
    args = parser.parse_args()

    crew = {"veterans": args.vets, "recovery": args.recovery, "women": args.women}
    gt = GrantTracker(args.csv)
    gt.load()
    print(gt.partner_talking_points(crew))
    print()
    print(gt.action_summary())
    urgent = gt.urgent_deadlines(30)
    if urgent:
        print("\n=== URGENT (Next 30 Days) ===")
        for u in urgent:
            print(f"  {u['program']}: {u['days_until']} days (Priority {u['priority']})")
    out = gt.export_partner_sheet(crew, args.export)
    print(f"\n✓ Partner summary exported to {out}")

if __name__ == "__main__":
    main()
