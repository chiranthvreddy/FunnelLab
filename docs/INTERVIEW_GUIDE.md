# FunnelLab — Interview Preparation

## 45-second explanation
“I built FunnelLab as a personal product management project to explore the full growth decision loop. It lets a PM diagnose a four-step funnel, compare conversion across segments, inspect weekly retention, interpret a simulated A/B test with confidence intervals and guardrails, and prioritize potential improvements with RICE. I wrote the PRD and product case study and built the analytics in Python and Streamlit. The data is synthetic, so I present the outputs as a working demonstration rather than customer evidence.”

## Questions to expect
**Why this product?** Teams need to translate event data into prioritization and experiment decisions, not just display charts.

**What is activation?** The first meaningful core-value event. Here it is an explicitly simplified fictional 'activate' milestone.

**How do you find the biggest problem?** Look at step conversion, absolute drop-off, segment size, business value and confidence in the event definition. The largest numerical drop-off is not always the best opportunity.

**Does mobile underperformance prove mobile UX is worse?** No. Channel mix and user intent could confound observational comparisons. Investigate with user research and a controlled experiment.

**How is retention defined?** Percentage of the activated signup-week cohort with an activity event in week N; week zero is the baseline.

**When would you ship an A/B winner?** After checking allocation, pre-registered statistical evidence, practical effect, guardrails and operational readiness.

**What is SRM?** Sample-ratio mismatch: an unexpected treatment/control allocation imbalance that may indicate broken assignment or instrumentation.

**Why RICE?** It forces explicit reach, impact, confidence and effort assumptions, but scores are only as reliable as those assumptions.

**What is missing?** Real users, validated event tracking, production persistence, experiment power design and real usability testing.

## Honest resume bullets
- Built FunnelLab, an independent product-growth analytics prototype with segmented conversion funnels, activation-cohort retention, simulated A/B testing and RICE prioritization.
- Defined product requirements, metric denominators, statistical guardrails and a validation roadmap; implemented reproducible synthetic datasets and automated analytics tests.
