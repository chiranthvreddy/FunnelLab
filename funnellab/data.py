"""Deterministic, synthetic SaaS user journeys and randomized demo experiments."""
import numpy as np
import pandas as pd

STEPS = ("visit", "signup", "activate", "purchase")
CHANNELS = ("Organic", "Paid Search", "Social", "Referral")
DEVICES = ("Desktop", "Mobile")


def generate_users(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    channels = rng.choice(CHANNELS, n, p=[0.36, 0.28, 0.21, 0.15])
    devices = rng.choice(DEVICES, n, p=[0.54, 0.46])
    cohorts = pd.Timestamp("2026-01-05") + pd.to_timedelta(rng.integers(0, 12, n) * 7, unit="D")
    base = np.array([{"Organic": .44, "Paid Search": .33, "Social": .27, "Referral": .51}[c] for c in channels])
    base -= (devices == "Mobile") * .06
    signup = rng.random(n) < base
    activation = signup & (rng.random(n) < np.where(devices == "Mobile", .49, .64))
    purchase = activation & (rng.random(n) < np.where(channels == "Referral", .40, .29))
    out = pd.DataFrame({
        "user_id": [f"U{i:06d}" for i in range(1, n + 1)],
        "channel": channels, "device": devices, "cohort_week": cohorts,
        "visit": True, "signup": signup, "activate": activation, "purchase": purchase,
    })
    out["days_to_activation"] = np.where(activation, rng.integers(0, 8, n), np.nan)
    return out


def generate_activity(users, weeks=8, seed=43):
    """Week 0 contains every activated user; later weeks simulate repeat usage."""
    rng = np.random.default_rng(seed)
    activated = users.loc[users["activate"], ["user_id", "cohort_week", "channel"]]
    frames = []
    for week in range(weeks):
        probability = 1.0 if week == 0 else max(.10, .69 * (.82 ** (week - 1)))
        mask = rng.random(len(activated)) < probability
        part = activated.loc[mask, ["user_id", "cohort_week"]].copy()
        part["week_number"] = week
        frames.append(part)
    return pd.concat(frames, ignore_index=True)


def generate_experiment(n=6000, seed=44):
    """Illustrative independent user assignment; no real-world experiment."""
    rng = np.random.default_rng(seed)
    variant = rng.choice(["Control", "Treatment"], n)
    eligible = rng.random(n) < .97
    conversion_prob = np.where(variant == "Treatment", .125, .112)
    converted = eligible & (rng.random(n) < conversion_prob)
    return pd.DataFrame({
        "user_id": [f"E{i:06d}" for i in range(n)],
        "variant": variant, "eligible": eligible, "converted": converted,
        "guardrail_error": rng.random(n) < np.where(variant == "Treatment", .026, .021),
    })
