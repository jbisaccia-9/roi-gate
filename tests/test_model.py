from roigate.model import compute


def test_hand_computed_value():
    adoption = {"total_seats": 10, "tiers": {"heavy": 2, "medium": 1, "light": 0, "inactive": 7}}
    a = {"excluded_seat_fraction": 0.1, "minutes_saved_per_day": {"heavy": 10, "medium": 5},
         "workdays_per_month": 20, "hourly_rate": 30, "realization_discount": 0.5,
         "charge_all_assigned_seats": True, "license_cost_per_seat_month": 10}
    v = compute(adoption, a)
    # heavy: 2*10*20=400 min; medium: 1*5*20=100 min -> 500 min = 8.333h * $30 = $250 gross
    assert v["gross_monthly_value"] == 250.0
    assert v["realized_monthly_value"] == 125.0     # 50% realization
    assert v["license_cost_monthly"] == 100.0       # ALL 10 seats, not the 3 active
    assert v["net_annual_value"] == 300.0           # (125-100)*12


def test_inactive_seats_earn_zero():
    adoption = {"total_seats": 100, "tiers": {"heavy": 0, "medium": 0, "light": 0, "inactive": 100}}
    a = {"excluded_seat_fraction": 0.1, "minutes_saved_per_day": {"heavy": 10, "medium": 5},
         "workdays_per_month": 20, "hourly_rate": 30, "realization_discount": 0.5,
         "charge_all_assigned_seats": True, "license_cost_per_seat_month": 10}
    v = compute(adoption, a)
    assert v["gross_monthly_value"] == 0.0
    assert v["net_annual_value"] == -12000.0        # pure license cost: honest negative
