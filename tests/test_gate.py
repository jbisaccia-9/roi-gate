import json
import pathlib
from roigate.gate import check
from roigate.model import load_assumptions

HERE = pathlib.Path(__file__).parent


def test_base_assumptions_pass():
    assert check(load_assumptions()) == 0


def test_aggressive_assumptions_refused():
    aggressive = json.loads((HERE / "aggressive_example.json").read_text())
    assert check(aggressive) == 1


def test_each_lever_alone_fails():
    base = load_assumptions()
    for key, bad in [("realization_discount", 1.0),
                     ("charge_all_assigned_seats", False),
                     ("license_cost_per_seat_month", 0),
                     ("excluded_seat_fraction", 0.0)]:
        a = dict(base); a[key] = bad
        assert check(a) == 1, f"gate should refuse {key}={bad}"
