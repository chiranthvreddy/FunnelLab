# Example Growth Experiment Plan (hypothetical)

## Hypothesis
Simplifying mobile onboarding increases activation and downstream purchase conversion without increasing error rates.

## Unit of randomization
Unique eligible user ID, stable assignment, 50/50 control vs treatment.

## Primary outcome
Purchase conversion among eligible assigned users during a fixed observation window. For a real test, predefine exposure, conversion attribution and late-arriving events.

## Guardrails
Checkout error rate, latency, complaint rate, sample-ratio mismatch (SRM) and data completeness.

## Design safeguards
- Pre-register minimum detectable effect, power, alpha, exposure window and stopping rules.
- Conduct A/A and event integrity checks before rollout.
- Investigate SRM at p < 0.001 before interpreting outcome.
- Monitor treatment/control exposure and logging symmetry.
- Avoid repeated uncorrected peeking and unplanned subgroup fishing.
- Review practical significance and costs, not only statistical significance.

## Analysis in prototype
Two-sided pooled z-test for difference in proportions under the null; unpooled normal-approximation 95% CI for absolute lift; chi-square 50/50 allocation check. The app reports both conversion rates, sample sizes, effect and error-rate guardrail.

## Decision framework
- SRM detected → investigate instrumentation/assignment.
- Confidence interval spans zero → inconclusive, not a loss or win.
- Statistically positive but guardrails regress → do not automatically launch.
- Statistically and practically positive with acceptable guardrails → consider staged rollout after technical and privacy review.

**No actual experiment has been run. All displayed assignment and outcomes are synthetic.**
