# Insurance Sanity Check — Texas Workers’ Comp (Public Data)

**Purpose:** Use official Texas Department of Insurance (TDI) sources to estimate workers’ comp cost for 2nd Story’s services without waiting on broker quotes.

---

## The Formula (Texas)
**Rate per $100 payroll = Advisory Loss Cost × Carrier LCM (Loss-Cost Multiplier)**

- TDI publishes **advisory loss costs** by class.
- Each carrier files an **LCM** with TDI; multiplying loss cost × LCM produces your **rate per $100** payroll.

**References (official/public):**
- TDI “Basis of Rates / Rate Guide” (explains loss cost × LCM; shows Roofing 5551 example).  
  https://www.tdi.texas.gov/wc/regulation/rcomp.html
- TDI 2025 loss-cost bulletin (overall **–11.5%** average loss-cost change effective **July 1, 2025**).  
  https://www.tdi.texas.gov/bulletins/2025/B-0002-25.html
- 2025 Texas Loss Costs (PDF).  
  https://www.tdi.texas.gov/wc/regulation/documents/2025txlosscosts.pdf
- Texas is generally **not mandatory** for private employers (non-subscriber option).  
  https://www.tdi.texas.gov/wc/employer/coverage.html

---

## Class We Care About First (Pilot)
**5551 — Roofing, All Kinds & Drivers (used here for tear-off/site prep baseline)**  
TDI example notes **Loss Cost = 2.27** for Code 5551 (effective 7/1/2025).  
For planning, assume a reasonable LCM band (e.g., **1.30 / 1.50 / 1.90**).

**Rate per $100 payroll (5551):**
- LCM 1.30 → 2.27 × 1.30 = **$2.951**
- LCM 1.50 → 2.27 × 1.50 = **$3.405**
- LCM 1.90 → 2.27 × 1.90 = **$4.313**

---

## Quick Premium Table (Pilot payroll scenarios)

| LCM | Payroll | Rate per $100 | Estimated Annual Premium |
|---:|---:|---:|---:|
| 1.30 | $40,000 | $2.951 | **$1,180.40** |
| 1.30 | $60,000 | $2.951 | **$1,770.60** |
| 1.30 | $100,000 | $2.951 | **$2,951.00** |
| 1.50 | $40,000 | $3.405 | **$1,362.00** |
| 1.50 | $60,000 | $3.405 | **$2,043.00** |
| 1.50 | $100,000 | $3.405 | **$3,405.00** |
| 1.90 | $40,000 | $4.313 | **$1,725.20** |
| 1.90 | $60,000 | $4.313 | **$2,587.80** |
| 1.90 | $100,000 | $4.313 | **$4,313.00** |

> Formula check: **Premium ≈ (Loss Cost × LCM) × (Payroll ÷ 100)**

---

## Expansion Classes (reference points)
As we add services, underwriters may use other classes. Public agency tables show indicative TX ranges:

- **6400 Fence Installation & Repair:** ~$2.44–$11.91 per $100 payroll  
- **6216 Excavation/Grading (proxy for some erosion tasks):** ~$2.07–$10.10 per $100 payroll  
Reference: WorkersCompensationShop TX class rate table (for sanity checks; actual carrier/LCM applies).  
https://www.workerscompensationshop.com/insurance-states/texas/rates

---

## Practical Guidance
- These numbers are **planning-grade**, good enough to green-light the pilot P&L.  
- If/when we bid municipal/commercial work or bind a policy, confirm **final class code(s)** and **LCM** with a carrier/broker.
- Safety programs (**OSHA-10 lead, toolbox talks, fall protection where applicable**) may qualify for credits.

**Update cadence:** When TDI publishes new loss costs or bulletins, refresh the table and `data/comp-scenarios.csv`.
