import pandas as pd
import pytest
from funnellab.data import generate_users, generate_activity, generate_experiment
from funnellab.analytics import funnel, segment_funnel, retention, experiment_summary, rice_score


def test_reproducible_generation():
    assert generate_users(200, seed=7).equals(generate_users(200, seed=7))


def test_funnel_monotonic():
    users = generate_users(500)
    counts = funnel(users).users.tolist()
    assert counts == sorted(counts, reverse=True)
    assert counts[0] == 500


def test_empty_funnel():
    users = generate_users(0)
    out = funnel(users)
    assert out.users.sum() == 0
    assert out.visit_conversion.sum() == 0


def test_segment_totals():
    users = generate_users(300)
    by_device = segment_funnel(users, "device")
    assert by_device.loc[by_device.step == "Visit", "users"].sum() == 300


def test_invalid_segment():
    with pytest.raises(ValueError):
        segment_funnel(generate_users(10), "password")


def test_retention_baseline():
    users = generate_users(500)
    activity = generate_activity(users, weeks=5)
    ret = retention(users, activity, weeks=5)
    assert (ret.loc[ret.week == 0, "retention"] == 1).all()
    assert ret.retention.between(0, 1).all()


def test_experiment_reproducible():
    assert generate_experiment(100, seed=8).equals(generate_experiment(100, seed=8))


def test_experiment_statistics():
    result = experiment_summary(generate_experiment(6000))
    assert 0 <= result["p_value"] <= 1
    assert 0 <= result["srm_p_value"] <= 1
    assert result["ci_lower"] <= result["absolute_lift"] <= result["ci_upper"]


def test_experiment_missing_variant():
    with pytest.raises(ValueError):
        experiment_summary(pd.DataFrame({"variant": ["Control"], "eligible": [True], "converted": [False]}))


def test_rice():
    assert rice_score(100, 2, .5, 5) == 20
    with pytest.raises(ValueError):
        rice_score(100, 2, 1.2, 5)
