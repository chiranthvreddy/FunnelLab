"""FunnelLab — interactive product growth case study."""
import pandas as pd
import plotly.express as px
import streamlit as st

from funnellab.data import generate_users, generate_activity, generate_experiment
from funnellab.analytics import funnel, segment_funnel, retention, experiment_summary, rice_score
from funnellab.decisions import decision_memo, validate_opportunities

st.set_page_config(page_title="FunnelLab | Growth Studio", page_icon="📈", layout="wide")
st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1280px}
h1,h2,h3{letter-spacing:-.035em}
[data-testid="stMetric"]{background:#f4f7fb;padding:15px;border-radius:12px}
</style>""", unsafe_allow_html=True)

@st.cache_data
def demo_data():
    users = generate_users()
    return users, generate_activity(users), generate_experiment()

users, activity, experiment = demo_data()
st.title("FunnelLab")
st.caption("PRODUCT GROWTH STUDIO  /  Independent passion project  /  Synthetic data only")
st.markdown("**Scenario: TeamNest**, a fictional freemium collaboration product. Diagnose onboarding friction, test hypotheses, and write a product decision memo.")

with st.sidebar:
    st.header("Analysis controls")
    channel = st.multiselect("Acquisition channels", sorted(users.channel.unique()), default=sorted(users.channel.unique()))
    device = st.multiselect("Devices", sorted(users.device.unique()), default=sorted(users.device.unique()))
    st.divider()
    st.info("Demo dataset: 5,000 fictional users. No live tracking or real customer data.")
    st.caption("All outcomes are illustrative, not measured business results.")

selected = users.loc[users.channel.isin(channel) & users.device.isin(device)]
tabs = st.tabs(["Overview", "Funnel explorer", "Retention", "Experiments", "Opportunity lab", "Metric dictionary"])

with tabs[0]:
    st.subheader("Growth command centre")
    f = funnel(selected)
    visits = int(f.iloc[0].users)
    signups = int(f.iloc[1].users)
    activated = int(f.iloc[2].users)
    buyers = int(f.iloc[3].users)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Visitors", f"{visits:,}")
    c2.metric("Signup conversion", f"{signups/visits:.1%}" if visits else "N/A")
    c3.metric("Activation / signup", f"{activated/signups:.1%}" if signups else "N/A")
    c4.metric("Purchase / visitor", f"{buyers/visits:.1%}" if visits else "N/A")
    st.plotly_chart(px.bar(f, x="step", y="users", text="users", title="End-to-end funnel"), use_container_width=True)
    st.markdown("**Interpretation:** Compare step-to-step conversion before prioritizing interventions. This dataset intentionally models mobile activation friction; that is a synthetic hypothesis, not a user finding.")
    st.download_button("Download funnel CSV", f.to_csv(index=False), "funnel_summary.csv", "text/csv")

with tabs[1]:
    st.subheader("Funnel explorer")
    dimension = st.selectbox("Compare segments", ["channel", "device", "cohort_week"])
    if selected.empty:
        st.warning("No users match the selected filters.")
    else:
        breakdown = segment_funnel(selected, dimension)
        chart = breakdown.loc[breakdown.step != "Visit"].copy()
        chart["segment"] = chart[dimension].astype(str)
        st.plotly_chart(px.bar(chart, x="step", y="step_conversion", color="segment", barmode="group",
                               title="Step conversion by segment", labels={"step_conversion":"Step conversion"}),
                        use_container_width=True)
        st.dataframe(breakdown, use_container_width=True, hide_index=True)
        st.download_button("Export segment metrics", breakdown.to_csv(index=False), "segment_funnel.csv", "text/csv")
        st.caption("Segment comparisons are descriptive and may be confounded. Do not infer causality from this chart.")

with tabs[2]:
    st.subheader("Weekly retention cohorts")
    st.caption("Cohorts are grouped by signup week; denominator is activated users from that signup cohort. Week N represents simulated activity N weeks after activation, not N calendar weeks after signup.")
    active_users = selected.loc[selected.activate]
    selected_activity = activity.loc[activity.user_id.isin(active_users.user_id)]
    ret = retention(selected, selected_activity)
    if ret.empty:
        st.info("No activated users match the current filters.")
    else:
        heat = ret.pivot(index="cohort_week", columns="week", values="retention")
        heat.index = heat.index.strftime("%Y-%m-%d")
        st.plotly_chart(px.imshow(heat, text_auto=".0%", color_continuous_scale="Blues",
                                 zmin=0, zmax=1, labels={"x":"Week since activation", "y":"Cohort", "color":"Retention"}),
                        use_container_width=True)
        summary = ret.groupby("week", as_index=False).agg(active=("active", "sum"), cohort_size=("cohort_size", "sum"))
        summary["retention"] = summary.active / summary.cohort_size
        st.plotly_chart(px.line(summary, x="week", y="retention", markers=True,
                                title="Weighted retention by week"), use_container_width=True)
        st.download_button("Export retention", ret.to_csv(index=False), "retention.csv", "text/csv")
        st.caption("Synthetic activity is generated for a full eight-week observation window per cohort; this is not a calendar-censored production retention calculation.")

with tabs[3]:
    st.subheader("Experiment decision room")
    st.markdown("**Hypothesis:** A simplified activation flow increases purchase conversion without materially increasing errors.")
    st.caption("Separate fictional randomized experiment sample; sidebar filters do not apply.")
    e = experiment_summary(experiment)
    a,b,c,d = st.columns(4)
    a.metric("Control conversion", f"{e['control_rate']:.2%}", f"n={e['control_n']:,}", delta_color="off")
    b.metric("Treatment conversion", f"{e['treatment_rate']:.2%}", f"n={e['treatment_n']:,}", delta_color="off")
    c.metric("Absolute lift", f"{e['absolute_lift']*100:+.2f} pp")
    d.metric("Two-sided p-value", f"{e['p_value']:.3f}")
    st.markdown(f"**95% CI for absolute lift:** {e['ci_lower']*100:+.2f} to {e['ci_upper']*100:+.2f} percentage points.")
    st.markdown(f"**Sample-ratio mismatch p-value:** {e['srm_p_value']:.4f} " +
                ("— investigate allocation before interpretation." if e["srm_warning"] else "— no strong SRM signal at the 0.001 threshold."))
    st.markdown(f"**Guardrail error rates:** Control {e['control_error']:.2%} · Treatment {e['treatment_error']:.2%}.")
    if e["srm_warning"]:
        st.error("Do not ship: assignment imbalance needs investigation.")
    elif not e["significant"]:
        st.warning("Inconclusive: do not declare a winner. Review power and continue only under a pre-registered plan.")
    elif e["treatment_error"] > e["control_error"] + .01:
        st.warning("Statistical signal detected, but investigate error-rate guardrail before rollout.")
    elif e["absolute_lift"] > 0:
        st.success("Positive statistical signal in synthetic data; validate guardrails and operational readiness before any real launch.")
    else:
        st.warning("Treatment underperforms in synthetic data.")
    st.caption("Normal-approximation two-proportion z-test; illustrative, not a real deployment or proof of causality in any actual product.")

with tabs[4]:
    st.subheader("Opportunity prioritization")
    st.markdown("Edit the individual opportunity assumptions and turn the results into a downloadable product decision. All values are hypothetical.")
    items = [
        ("Mobile onboarding simplification", 2100, 1.8, .75, 5),
        ("Referral onboarding guidance", 900, 1.5, .70, 3),
        ("Activation reminder sequence", 1600, 1.2, .65, 4),
        ("Checkout trust signals", 700, 1.4, .60, 4),
    ]
    default_rows = pd.DataFrame([
        {"opportunity": name, "reach": reach, "impact": impact, "confidence": conf, "effort": eff}
        for name, reach, impact, conf, eff in items
    ])
    edited = st.data_editor(
        default_rows, num_rows="dynamic", hide_index=True, use_container_width=True,
        column_config={
            "opportunity": st.column_config.TextColumn("Opportunity", required=True),
            "reach": st.column_config.NumberColumn("Reach / quarter (assumed)", min_value=0, step=100),
            "impact": st.column_config.NumberColumn("Impact (assumed)", min_value=0.0, step=0.1),
            "confidence": st.column_config.NumberColumn("Confidence (0–1)", min_value=0.0, max_value=1.0, step=0.05),
            "effort": st.column_config.NumberColumn("Effort (person-weeks)", min_value=0.1, step=0.5),
        },
        key="opportunity_editor",
    )
    rows = edited.to_dict("records")
    try:
        validate_opportunities(rows)
        backlog = edited.copy()
        backlog["RICE"] = backlog.apply(lambda r: rice_score(r["reach"], r["impact"], r["confidence"], r["effort"]), axis=1)
        backlog = backlog.sort_values("RICE", ascending=False)
        st.dataframe(backlog, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(backlog, x="RICE", y="opportunity", orientation="h",
                               title="Scenario-based RICE ranking"), use_container_width=True)
        st.download_button("Download opportunity backlog", backlog.to_csv(index=False), "opportunities.csv", "text/csv")
        st.markdown("### Product decision memo")
        problem = st.text_area("Problem statement", "Mobile visitors appear less likely to activate; the cause is not yet validated.")
        evidence = st.text_area("Evidence and uncertainty", "Synthetic funnel segments show differences. Channel mix and user intent are alternative explanations.")
        hypothesis = st.text_area("Testable hypothesis", "A shorter mobile onboarding flow improves first-value activation.")
        guardrail = st.text_input("Guardrail", "No meaningful increase in checkout or onboarding errors.")
        next_step = st.text_input("Next action", "Interview target users, instrument real activation, then preregister an experiment.")
        memo = decision_memo(problem, evidence, hypothesis, rows, guardrail, next_step)
        st.download_button("Download decision memo (.md)", memo, "funnellab_decision_memo.md", "text/markdown")
        with st.expander("Preview memo"):
            st.markdown(memo)
    except (ValueError, TypeError, KeyError) as exc:
        st.error(f"Correct the opportunity inputs to continue: {exc}")
    st.caption("RICE ranks assumed opportunities; it is not a measured forecast or causal estimate.")

with tabs[5]:
    st.subheader("Metric dictionary")
    dictionary = [
        ("Visitor", "Unique synthetic user with a visit event", "All users"),
        ("Signup conversion", "Signed-up visitors / all visitors", "Visitor"),
        ("Activation rate", "Activated users / signed-up users", "Signed-up users"),
        ("Purchase conversion", "Purchased users / visitors", "Visitor"),
        ("Step drop-off", "Previous step users − current step users", "Previous step"),
        ("Week-N retention", "Activated cohort members active in week N / activated cohort size", "Activated cohort"),
        ("Experiment lift", "Treatment conversion − control conversion", "Eligible assigned users"),
        ("RICE", "Reach × Impact × Confidence / Effort", "Scenario assumptions"),
    ]
    st.dataframe(pd.DataFrame(dictionary, columns=["Metric", "Definition", "Denominator / basis"]),
                 use_container_width=True, hide_index=True)
    st.markdown("**Tracking design:** One canonical user ID; mutually exclusive assignment for experiments; UTC event timestamps; documented event schema; deduplication; exclusion and guardrail rules; consent and privacy review before production.")
