"""Generate a synthetic usage-event log for a fictional 150-seat deployment.

Every value here is invented. The org, the seats, the feature areas, and the
usage distribution are synthetic by construction — the point of this repo is
the measurement METHOD, so the data only needs to be shaped like reality.
"""
import json
import pathlib
import random

FEATURE_AREAS = ["drafting", "summarize", "search", "sheets", "meetings", "inbox"]
ROOT = pathlib.Path(__file__).resolve().parents[2]


def generate(seats=150, days=30, seed=7):
    rng = random.Random(seed)  # seeded: the committed dataset is reproducible
    events = []
    for uid in range(seats):
        # Synthetic engagement mix: some users adopt deeply, some never start.
        engagement = rng.choices(["heavy", "medium", "light", "none"],
                                 weights=[0.30, 0.28, 0.22, 0.20])[0]
        n_areas = {"heavy": rng.randint(4, 6), "medium": rng.randint(2, 3),
                   "light": 1, "none": 0}[engagement]
        areas = rng.sample(FEATURE_AREAS, n_areas)
        p_active = {"heavy": 0.8, "medium": 0.45, "light": 0.15, "none": 0.0}[engagement]
        for day in range(1, days + 1):
            if rng.random() < p_active:
                for area in areas:
                    if rng.random() < 0.7:
                        events.append({"user": f"u{uid:03d}", "day": day, "area": area,
                                       "actions": rng.randint(1, 12)})
    return events


def main(path=None):
    path = pathlib.Path(path) if path else ROOT / "data" / "synthetic_events.jsonl"
    events = generate()
    path.write_text("\n".join(json.dumps(e) for e in events))
    print(f"wrote {len(events)} synthetic events -> {path.name}")


if __name__ == "__main__":
    main()
