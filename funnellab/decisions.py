"""Product opportunity scoring and decision memo generation."""
import math


def validate_opportunities(rows):
    for row in rows:
        reach = float(row["reach"])
        impact = float(row["impact"])
        confidence = float(row["confidence"])
        effort = float(row["effort"])
        if not all(math.isfinite(x) for x in (reach, impact, confidence, effort)):
            raise ValueError("All inputs must be finite")
        if reach < 0 or impact < 0 or not 0 <= confidence <= 1 or effort <= 0:
            raise ValueError("Reach/impact must be nonnegative; confidence 0–1; effort positive")
    return True


def decision_memo(problem, evidence, hypothesis, rows, guardrail, next_step):
    validate_opportunities(rows)
    ranked = sorted(rows, key=lambda r: float(r["reach"])*float(r["impact"])*float(r["confidence"])/float(r["effort"]), reverse=True)
    leader = ranked[0] if ranked else None
    choice = leader["opportunity"] if leader else "No opportunity selected"
    return f"""# FunnelLab — Product Decision Memo

**Context:** Fictional freemium team collaboration product (illustrative case).

## Problem
{problem.strip()}

## Evidence and uncertainty
{evidence.strip()}

## Hypothesis
{hypothesis.strip()}

## Prioritized bet
**{choice}** (highest modeled RICE score, not proof of impact).

## Guardrail
{guardrail.strip()}

## Next action
{next_step.strip()}

## Interpretation
This memo is a scenario exercise using synthetic data and assumed prioritization inputs. It is not evidence of customer research, real experiments, or business outcomes.
"""
