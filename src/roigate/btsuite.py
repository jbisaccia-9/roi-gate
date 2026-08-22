"""Braintrust-shaped eval suite: data -> task -> scorers.

Cases pair an assumptions file with the gate outcome it must produce, plus a
value-regression pin: the fixture deployment must always price to the same
net annual figure. Deterministic components get evals to catch REGRESSION -
change a discount floor or a tier minute and CI says so before it ships.
"""
import json
import pathlib

from . import gate
from .adoption import load_events, analyze
from .model import compute, load_assumptions

ROOT = pathlib.Path(__file__).resolve().parents[2]

CASES = [
    {"id": "base-conservative", "file": "assumptions.json", "expected_gate": 0},
    {"id": "vendor-deck", "file": "tests/aggressive_example.json", "expected_gate": 1},
]
PINNED_NET_ANNUAL = 24048.0


def task(case):
    return {"gate": gate.check(load_assumptions(ROOT / case["file"]))}


def gate_expected(case, out):
    return 1.0 if out["gate"] == case["expected_gate"] else 0.0


def value_regression():
    a = load_assumptions()
    v = compute(analyze(load_events(), total_seats=a["total_seats"]), a)
    return 1.0 if v["net_annual_value"] == PINNED_NET_ANNUAL else 0.0


def run_local():
    scores = {c["id"]: gate_expected(c, task(c)) for c in CASES}
    scores["value_regression"] = value_regression()
    for k, v in scores.items():
        print(f"  {k}: {v}")
    ok = all(v == 1.0 for v in scores.values())
    print("SUITE: PASS - no regressions." if ok else "SUITE: FAIL - a scorer regressed.")
    return 0 if ok else 1


def push_braintrust():
    import braintrust  # optional extra
    braintrust.Eval("roi-gate",
                    data=lambda: [{"input": c, "expected": c["expected_gate"]} for c in CASES],
                    task=task,
                    scores=[lambda input, expected, output:
                            braintrust.Score(name="gate_expected",
                                             score=gate_expected(input, output))])
