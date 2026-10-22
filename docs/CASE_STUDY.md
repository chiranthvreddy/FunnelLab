# FunnelLab — Product Management Case Study

## One-line pitch
A self-initiated product growth studio that connects funnel diagnosis, retention analysis, experiment interpretation and roadmap prioritization.

## Why I chose the problem
A signup number alone does not tell a product team whether acquisition, onboarding or the core product experience is the bottleneck. I wanted a workspace where each view naturally leads to the next PM decision.

## Problem framing
**User:** Growth PM / product analyst (hypothesized persona).
**Pain:** Disconnected funnel charts, retention tables, statistical calculators and prioritization spreadsheets.
**Opportunity:** Make metric definitions and decision trade-offs explicit in one lightweight prototype.

## Product decisions
**One user per funnel:** Counts are unique fictional users with monotonic stage progression, avoiding accidental inflation from repeat events.

**Activation before retention:** Retention denominator is the activated cohort. This makes the meaning clear but does not answer signup-based retention; production should support both.

**Two separate datasets:** Funnel behavior and experiment assignment are simulated separately to avoid suggesting the dashboard is connected to a live experiment.

**Statistical transparency:** Report effect sizes, intervals, p-values and sample-ratio mismatch; do not automatically label a treatment a business win.

**RICE as scenario planning:** Users can challenge confidence and effort assumptions rather than treating rankings as facts.

## Demonstration workflow
1. Inspect visit-to-purchase funnel and locate the largest relative drop-off.
2. Segment by mobile vs desktop to formulate an onboarding hypothesis.
3. Inspect activated-user retention to distinguish acquisition from engagement.
4. Review simulated experiment results and statistical guardrails.
5. Prioritize an opportunity using explicit RICE assumptions.

## Trade-offs
- **Streamlit vs full-stack app:** Faster reproducible analysis, weaker production UX and collaboration.
- **Synthetic vs real data:** Safe and shareable, but cannot validate customer demand or prove outcomes.
- **Weekly vs daily retention:** Easier to interpret, less useful for high-frequency products.
- **Normal-approximation CI:** Simple and explainable, but not ideal for very small samples or rare outcomes.
- **Session-only interactions:** No account management or database.

## What I would validate next
Interview five real PMs or analysts, conduct moderated tasks, instrument task completion, evaluate preferred metric denominators, and test whether the decision workflow reduces analysis time. This is a proposed plan, **not research already completed**.

## Roadmap
**Now:** Robust event validation, segmented funnels, retention, experiment interpretation, reproducible synthetic examples.
**Next:** Custom event schemas, flexible cohort definitions, experiment power planning, sharable decision memos.
**Later:** Warehouse integration, role permissions, audit history, metric governance, alerting.

## Portfolio integrity
This project does not claim real users, real A/B tests, measured business lift, customer interviews or deployed production integrations.
