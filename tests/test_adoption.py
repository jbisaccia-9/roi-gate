from roigate.adoption import analyze


def events_for(user, day, areas):
    return [{"user": user, "day": day, "area": a, "actions": 1} for a in areas]


def test_tiering_by_depth():
    ev = (events_for("u1", 30, ["drafting", "summarize", "search", "sheets"]) +
          events_for("u2", 30, ["drafting", "summarize"]) +
          events_for("u3", 30, ["inbox"]))
    r = analyze(ev, total_seats=10)
    assert r["tiers"] == {"heavy": 1, "medium": 1, "light": 1, "inactive": 7}
    assert r["active_30d"] == 3 and r["active_30d_pct"] == 0.3


def test_seven_day_window_narrower_than_thirty():
    ev = events_for("old", 1, ["drafting"]) + events_for("new", 30, ["drafting"])
    r = analyze(ev, total_seats=5)
    assert r["active_30d"] == 2 and r["active_7d"] == 1
