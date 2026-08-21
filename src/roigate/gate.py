"""The conservatism gate: an ROI figure is reportable only if the model that
produced it was biased against the claim. Exit 0 = defensible; 1 = the number
is inflated by construction and must not be reported.

These are the checks a skeptical CFO would run. Encoding them as CI means the
aggressive version of the number cannot exist quietly.
"""
import sys

CHECKS = [
    ("realization_discount applied (<= 0.6)",
     lambda a: a["realization_discount"] <= 0.6,
     "measured time saved must be discounted before it is claimed as value"),
    ("every assigned seat charged",
     lambda a: a["charge_all_assigned_seats"] is True,
     "charging only active seats hides the cost of shelfware"),
    ("license costs included",
     lambda a: a["license_cost_per_seat_month"] > 0,
     "value net of nothing is not net value"),
    ("some seats excluded from benefit",
     lambda a: a["excluded_seat_fraction"] > 0,
     "senior/edge roles whose time savings can't be verified earn zero"),
    ("inactive seats earn zero benefit",
     lambda a: "inactive" not in a["minutes_saved_per_day"],
     "a seat with no usage produces no value, whatever the license says"),
]


def check(assumptions):
    failures = []
    for name, fn, why in CHECKS:
        ok = fn(assumptions)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            failures.append((name, why))
    if failures:
        print("GATE: FAILED - this configuration inflates the claim:")
        for name, why in failures:
            print(f"    - {name}: {why}")
        return 1
    print("GATE: PASSED - the model is biased against the claim; the number is reportable.")
    return 0


if __name__ == "__main__":
    from .model import load_assumptions
    sys.exit(check(load_assumptions()))
