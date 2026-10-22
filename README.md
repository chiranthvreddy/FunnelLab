# FunnelLab — Product Growth & Experimentation Studio

**An independent passion project exploring how product managers turn behavioral data into growth decisions.**

FunnelLab is a hands-on Streamlit product analytics workspace: onboarding funnel, weekly retention, segment breakdowns, A/B test analysis, and a prioritized opportunity backlog. It uses **deterministic synthetic events** and illustrative experiments. It is not a production analytics service, and no customer impact is claimed.

## What you can do
- Inspect visitor → signup → activation → purchase conversion and step drop-offs.
- Compare funnel performance across acquisition channels, devices and signup cohorts.
- Inspect weekly retention cohorts and activation-to-purchase lag.
- Analyze a randomized **synthetic** A/B test with lift, confidence intervals, and sample-ratio mismatch checks.
- Rank product opportunities with explicit RICE assumptions and create a growth decision memo.
- Download aggregated CSVs and view definitions for every metric.

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy
In Streamlit Community Cloud, select this repository, branch `main`, and entrypoint `app.py`. No secrets or external database are required.

## Project structure
- `app.py` — interactive application
- `funnellab/data.py` — reproducible synthetic event and experiment generation
- `funnellab/analytics.py` — reusable metric calculations
- `tests/` — analytics and generator tests
- `docs/PRD.md` — product definition and user stories
- `docs/CASE_STUDY.md` — product thinking, trade-offs and roadmap
- `docs/EXPERIMENT_PLAN.md` — guardrails and experiment interpretation
- `docs/INTERVIEW_GUIDE.md` — interview-ready walkthrough

## Data integrity and limitations
All users, events, channels, orders, and experiment outcomes are simulated. Conversion and retention are observational descriptions of this generated dataset, **not evidence of real product performance**. The experiment assignment is simulated and is not an actual deployed randomized trial. The app runs locally or in a hosted Streamlit process without user accounts or persistence. Dates, metrics and decisions should be described as demonstration outputs.

## Skills demonstrated
Product metric design · Funnel diagnosis · Retention analysis · Experimentation · Statistical interpretation · Prioritization · Product requirements · Python · Pandas · Streamlit · Plotly · Pytest

Built as a standalone personal portfolio project, without company affiliation.
