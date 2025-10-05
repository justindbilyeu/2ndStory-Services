#!/usr/bin/env bash
set -euo pipefail
python tools/grants/grant_tracker.py --csv data/grant-opportunities.csv --export data/funding-summary.md --vets 2 --recovery 3 --women 2
echo "Open data/funding-summary.md for your partner brief."
