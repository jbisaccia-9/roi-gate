"""Conservative ROI model: convert adoption depth into a defensible dollar figure.

The design bias is deliberate: every assumption that involves judgment leans
AGAINST the value claim. Benefit is tiered by depth of use, discounted by a
realization factor (measured time saved is not the same as time converted to
output), excluded roles earn zero, and every assigned seat is charged whether
or not it was ever used. The number that survives is smaller — and defensible.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_assumptions(path=None):
    path = pathlib.Path(path) if path else ROOT / "assumptions.json"
    return json.loads(path.read_text())


def compute(adoption, a):
    """Return the full value breakdown. Every intermediate is in the output —
    a number whose arithmetic can't be inspected is a slide, not a measurement."""
    tiers = adoption["tiers"]
    excluded = round(adoption["total_seats"] * a["excluded_seat_fraction"])
    minutes = a["minutes_saved_per_day"]          # per tier, from time studies
    monthly_minutes = {
        t: tiers[t] * minutes.get(t, 0) * a["workdays_per_month"]
        for t in ("heavy", "medium", "light")
    }
    gross_monthly = sum(monthly_minutes.values()) / 60 * a["hourly_rate"]
    realized_monthly = gross_monthly * a["realization_discount"]
    # Cost side: every ASSIGNED seat is charged, active or not.
    license_monthly = adoption["total_seats"] * a["license_cost_per_seat_month"]
    net_annual = (realized_monthly - license_monthly) * 12
    return {
        "assumptions": a,
        "excluded_seats": excluded,
        "monthly_minutes_by_tier": monthly_minutes,
        "hours_recovered_monthly": round(sum(monthly_minutes.values()) / 60, 1),
        "gross_monthly_value": round(gross_monthly, 2),
        "realized_monthly_value": round(realized_monthly, 2),
        "license_cost_monthly": round(license_monthly, 2),
        "net_annual_value": round(net_annual, 2),
    }
