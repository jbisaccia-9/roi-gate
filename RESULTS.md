# Results

Generated 2026-08-21 by `scripts/make_results.py` — every block below is captured command output, not prose.

## Unit tests

`python -m pytest -q` — exit 0, OK

```
.......                                                                  [100%]
7 passed in 0.01s
```

## Adoption + value report (synthetic data)

`python -m roigate report` — exit 0, OK

```
{
  "adoption": {
    "total_seats": 150,
    "active_30d": 121,
    "active_30d_pct": 0.8067,
    "active_7d": 107,
    "tiers": {
      "heavy": 44,
      "medium": 35,
      "light": 42,
      "inactive": 29
    },
    "median_active_days": 13
  },
  "value": {
    "assumptions": {
      "_comment": "All values are synthetic examples for a fictional 150-seat deployment.",
      "total_seats": 150,
      "excluded_seat_fraction": 0.12,
      "minutes_saved_per_day": {
        "heavy": 12,
        "medium": 6,
        "light": 2
      },
      "workdays_per_month": 21,
      "hourly_rate": 40,
      "realization_discount": 0.5,
      "charge_all_assigned_seats": true,
      "license_cost_per_seat_month": 25
    },
    "excluded_seats": 18,
    "monthly_minutes_by_tier": {
      "heavy": 11088,
      "medium": 4410,
      "light": 1764
    },
    "hours_recovered_monthly": 287.7,
    "gross_monthly_value": 11508.0,
    "realized_monthly_value": 5754.0,
    "license_cost_monthly": 3750,
    "net_annual_value": 24048.0
  }
}
```

## Conservatism gate: base assumptions

`python -m roigate gate` — exit 0, OK

```
PASS  realization_discount applied (<= 0.6)
  PASS  every assigned seat charged
  PASS  license costs included
  PASS  some seats excluded from benefit
  PASS  inactive seats earn zero benefit
GATE: PASSED - the model is biased against the claim; the number is reportable.
```

## Conservatism gate: vendor-deck assumptions (must be refused)

`python -m roigate gate --assumptions tests/aggressive_example.json` — expected non-zero exit, OK

```
FAIL  realization_discount applied (<= 0.6)
  FAIL  every assigned seat charged
  FAIL  license costs included
  FAIL  some seats excluded from benefit
  FAIL  inactive seats earn zero benefit
GATE: FAILED - this configuration inflates the claim:
    - realization_discount applied (<= 0.6): measured time saved must be discounted before it is claimed as value
    - every assigned seat charged: charging only active seats hides the cost of shelfware
    - license costs included: value net of nothing is not net value
    - some seats excluded from benefit: senior/edge roles whose time savings can't be verified earn zero
    - inactive seats earn zero benefit: a seat with no usage produces no value, whatever the license says
```

## Braintrust-shaped eval suite

`python -m roigate suite` — exit 0, UNEXPECTED

```
usage: roigate [-h] {simulate,report,gate} ...
roigate: error: argument cmd: invalid choice: 'suite' (choose from 'simulate', 'report', 'gate')
```
