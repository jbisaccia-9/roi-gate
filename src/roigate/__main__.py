"""CLI:  python -m roigate simulate | report | gate [--assumptions FILE]"""
import argparse
import json
import pathlib
import sys

from . import simulate, adoption, model, gate

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(prog="roigate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("simulate", help="regenerate the seeded synthetic event log")
    rp = sub.add_parser("report", help="adoption + value breakdown -> results/report.json")
    rp.add_argument("--assumptions", default=None)
    gp = sub.add_parser("gate", help="apply the conservatism gate to an assumptions file")
    gp.add_argument("--assumptions", default=None)
    args = ap.parse_args()
    if args.cmd == "simulate":
        simulate.main()
        return
    a = model.load_assumptions(args.assumptions)
    if args.cmd == "gate":
        sys.exit(gate.check(a))
    events = adoption.load_events()
    adopt = adoption.analyze(events, total_seats=a["total_seats"])
    value = model.compute(adopt, a)
    out = ROOT / "results"; out.mkdir(exist_ok=True)
    report = {"adoption": adopt, "value": value}
    (out / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
