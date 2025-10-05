# Grants & Funding Tracker

Minimal CSV + Python tool to:
- track opportunities (credits, grants),
- estimate potential based on planned hires,
- flag urgent deadlines,
- export a partner-facing summary.

## Usage
```bash
python tools/grants/grant_tracker.py \
  --csv data/grant-opportunities.csv \
  --export data/funding-summary.md \
  --vets 2 --recovery 3 --women 2
```

First run creates data/grant-opportunities.csv with examples you can edit.
