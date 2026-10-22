# Product Requirements Document — FunnelLab
**Status:** Portfolio prototype · **Owner:** Independent builder · **Data:** Synthetic

## Problem
Early-stage product teams can observe top-line signups without understanding where users stall, whether activation predicts repeat usage, or whether an experiment is safe to launch.

## Target users
- Associate PM diagnosing onboarding conversion
- Growth PM prioritizing experiments
- Product analyst validating metric definitions

These personas are hypotheses, not interview findings.

## Job to be done
“When a growth metric changes, help me locate the failing step, compare meaningful segments, understand retention, and make an evidence-aware decision.”

## MVP scope
1. Filterable visitor → signup → activation → purchase funnel
2. Channel, device and signup-week breakdowns
3. Weekly retention cohort heatmap
4. Illustrative A/B analysis with confidence interval, p-value, SRM and error guardrail
5. Editable RICE scenario assumptions and CSV exports
6. Metric dictionary and transparent data limitations

## Out of scope
Live analytics SDK, authentication, persistence, enterprise governance, experiment assignment service, event ingestion and real user tracking.

## User stories / acceptance criteria
- As a PM, I can identify each funnel step's count, conversion and drop-off; zero-denominator cases do not crash.
- As an analyst, I can compare device/channel conversion using the same event definitions.
- As a PM, I can view cohort retention relative to the activated cohort, including 100% week-zero baseline.
- As an experiment owner, I can see absolute and relative lift, 95% confidence interval, two-sided p-value and SRM warning.
- As a PM, I can adjust RICE assumptions and download the ranking.

## North Star and guardrails
Proposed North Star: weekly activated users completing the product's core value action. The demo uses a simplified 'activate' event. Guardrails: checkout error rate, experiment allocation quality, performance, privacy and user complaints.

## Success criteria for a real pilot
Task completion and time-to-insight in moderated usability sessions; metric consistency against a trusted event warehouse; repeat weekly use by target PMs. None measured yet.

## Design principles
Explain denominators, avoid causal claims from observational segments, surface uncertainty, never hide synthetic-data provenance.
