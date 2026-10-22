import pytest
from funnellab.decisions import validate_opportunities, decision_memo

ROWS = [
    {"opportunity": "Mobile onboarding", "reach": 1000, "impact": 1.5, "confidence": .7, "effort": 4},
    {"opportunity": "Referral prompts", "reach": 500, "impact": 1.0, "confidence": .5, "effort": 5},
]

def test_valid_opportunities():
    assert validate_opportunities(ROWS)

def test_reject_zero_effort():
    with pytest.raises(ValueError):
        validate_opportunities([{**ROWS[0], "effort": 0}])

def test_reject_nonfinite():
    with pytest.raises(ValueError):
        validate_opportunities([{**ROWS[0], "impact": float("nan")}])

def test_decision_memo_selects_highest():
    memo = decision_memo("Problem", "Evidence", "Hypothesis", ROWS, "Errors", "Interview users")
    assert "**Mobile onboarding**" in memo
    assert "synthetic data" in memo
    assert "Interview users" in memo
