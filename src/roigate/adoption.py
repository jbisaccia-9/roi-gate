"""Adoption analytics: who actually uses the deployment, and how deeply.

Depth tiers are the honest unit of adoption. A seat that opened one feature
once is not the same evidence as a seat living in five of them, and a benefit
model that prices both identically is inflating itself.
"""
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_events(path=None):
    path = pathlib.Path(path) if path else ROOT / "data" / "synthetic_events.jsonl"
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def analyze(events, total_seats, window_days=30):
    last_day = max((e["day"] for e in events), default=0)
    recent = [e for e in events if e["day"] > last_day - window_days]
    week = [e for e in events if e["day"] > last_day - 7]
    areas_by_user, days_by_user = defaultdict(set), defaultdict(set)
    for e in recent:
        areas_by_user[e["user"]].add(e["area"])
        days_by_user[e["user"]].add(e["day"])

    def tier(u):
        n = len(areas_by_user[u])
        if n >= 4: return "heavy"
        if n >= 2: return "medium"
        if n >= 1: return "light"
        return "inactive"

    users = set(areas_by_user)
    tiers = {t: sum(1 for u in users if tier(u) == t) for t in ("heavy", "medium", "light")}
    tiers["inactive"] = total_seats - len(users)
    return {
        "total_seats": total_seats,
        "active_30d": len(users),
        "active_30d_pct": round(len(users) / total_seats, 4),
        "active_7d": len({e["user"] for e in week}),
        "tiers": tiers,
        "median_active_days": sorted(len(d) for d in days_by_user.values())[len(days_by_user) // 2] if days_by_user else 0,
    }
