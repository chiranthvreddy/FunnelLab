"""Metric definitions and statistical summaries; pure functions for testing."""
import math
import pandas as pd
from scipy.stats import norm, chi2

STEPS = ("visit", "signup", "activate", "purchase")


def funnel(users):
    counts = [int(users[step].sum()) for step in STEPS]
    rows = []
    for i, (step, count) in enumerate(zip(STEPS, counts)):
        previous = counts[i - 1] if i else count
        rows.append({
            "step": step.title(), "users": count,
            "step_conversion": count / previous if previous else 0.0,
            "visit_conversion": count / counts[0] if counts[0] else 0.0,
            "drop_off": previous - count if i else 0,
        })
    return pd.DataFrame(rows)


def segment_funnel(users, segment):
    if segment not in ("channel", "device", "cohort_week"):
        raise ValueError("Unsupported segment")
    parts = []
    for label, group in users.groupby(segment, dropna=False):
        summary = funnel(group)
        summary[segment] = label
        parts.append(summary)
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()


def retention(users, activity, weeks=8):
    """Cohorts are defined by activation; denominator is cohort activated users."""
    activated = users.loc[users["activate"], ["user_id", "cohort_week"]]
    if activated.empty:
        return pd.DataFrame()
    cohort_sizes = activated.groupby("cohort_week")["user_id"].nunique()
    active = activity.merge(activated, on=["user_id", "cohort_week"], how="inner")
    counts = active.groupby(["cohort_week", "week_number"])["user_id"].nunique()
    records = []
    for cohort, size in cohort_sizes.items():
        for week in range(weeks):
            count = int(counts.get((cohort, week), 0))
            records.append({"cohort_week": cohort, "week": week, "active": count,
                            "cohort_size": int(size), "retention": count / size})
    return pd.DataFrame(records)


def experiment_summary(events, alpha=.05):
    """Two-sided unpooled normal CI for risk difference; pooled z-test for H0.
    Requires independent Bernoulli observations. Treat as directional for small counts.
    """
    sample = events.loc[events["eligible"]].copy()
    groups = sample.groupby("variant")["converted"].agg(["sum", "count"])
    if not {"Control", "Treatment"}.issubset(groups.index):
        raise ValueError("Both variants must have eligible users")
    nc, nt = int(groups.loc["Control", "count"]), int(groups.loc["Treatment", "count"])
    if min(nc, nt) < 1:
        raise ValueError("Both variants need observations")
    xc, xt = int(groups.loc["Control", "sum"]), int(groups.loc["Treatment", "sum"])
    pc, pt = xc / nc, xt / nt
    diff = pt - pc
    se = math.sqrt(pc * (1 - pc) / nc + pt * (1 - pt) / nt)
    zcrit = norm.ppf(1 - alpha / 2)
    lower, upper = diff - zcrit * se, diff + zcrit * se
    pooled = (xc + xt) / (nc + nt)
    null_se = math.sqrt(pooled * (1 - pooled) * (1 / nc + 1 / nt))
    pvalue = 2 * norm.sf(abs(diff / null_se)) if null_se > 0 else (1.0 if diff == 0 else 0.0)
    total = nc + nt
    srm_chi = ((nc - total / 2) ** 2 + (nt - total / 2) ** 2) / (total / 2)
    srm_p = chi2.sf(srm_chi, df=1)
    errors = sample.groupby("variant")["guardrail_error"].mean()
    return {
        "control_n": nc, "treatment_n": nt, "control_conversions": xc,
        "treatment_conversions": xt, "control_rate": pc, "treatment_rate": pt,
        "absolute_lift": diff, "relative_lift": diff / pc if pc else float("nan"),
        "ci_lower": lower, "ci_upper": upper, "p_value": pvalue,
        "srm_p_value": srm_p, "srm_warning": srm_p < .001,
        "control_error": float(errors.get("Control", float("nan"))),
        "treatment_error": float(errors.get("Treatment", float("nan"))),
        "significant": pvalue < alpha,
    }


def rice_score(reach, impact, confidence, effort):
    if effort <= 0 or reach < 0 or impact < 0 or not 0 <= confidence <= 1:
        raise ValueError("Invalid RICE inputs")
    return reach * impact * confidence / effort
