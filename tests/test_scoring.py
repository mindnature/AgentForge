from runtime.scoring import classify_grade, evaluate


def test_a_grade():
    payload = {
        "need": {"frequency": 5, "time_cost": 4, "error_cost": 4, "friction": 4, "repeatability": 5},
        "ai_fit": {"model_capability": 5, "input_access": 5, "output_verifiability": 4, "toolability": 5, "autonomy_safety": 4},
        "verification": 4,
    }
    result = evaluate(payload)
    assert result["grade"] == "A"
    assert result["need_score"] >= 70
    assert result["ai_fit_score"] >= 70


def test_hard_stop_forces_d():
    payload = {
        "need": {"frequency": 5, "time_cost": 5, "error_cost": 5, "friction": 5, "repeatability": 5},
        "ai_fit": {"model_capability": 5, "input_access": 5, "output_verifiability": 5, "toolability": 5, "autonomy_safety": 5},
        "verification": 5,
        "unacceptable_irreversible_risk": True,
    }
    assert evaluate(payload)["grade"] == "D"


def test_threshold_order():
    assert classify_grade(90, 90, 90) == "A"
    assert classify_grade(65, 60, 50) == "B"
    assert classify_grade(50, 40, 30) == "C"
    assert classify_grade(30, 80, 80) == "D"
