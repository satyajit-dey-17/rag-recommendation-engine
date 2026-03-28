import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
import re

st.set_page_config(page_title="Multi-Cloud Recommender", layout="wide")


def parse_cost_midpoint(cost_str: str) -> float:
    numbers = re.findall(r'\d+', str(cost_str))
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    elif len(numbers) == 1:
        return float(numbers[0])
    return 0.0


st.title("☁️ Multi-Cloud Architecture Recommender")

# --- Input Form ---
with st.form("workload_form"):
    app_name = st.text_input("App Name")
    workload_type = st.selectbox("Workload Type", ["web_api", "ml_platform", "batch", "event_driven", "microservices"])
    user_scale = st.selectbox("User Scale", ["small", "medium", "large"])
    traffic_pattern = st.selectbox("Traffic Pattern", ["steady", "spiky", "batch"])
    compute_preference = st.selectbox("Compute Preference", ["serverless", "containers", "vms", "kubernetes"])
    database_type = st.selectbox("Database Type", ["relational", "nosql", "in_memory", "warehouse"])
    high_availability = st.checkbox("High Availability")
    disaster_recovery = st.checkbox("Disaster Recovery")
    budget_priority = st.selectbox("Budget Priority", ["low", "medium", "high"])
    preferred_region = st.text_input("Preferred Region (optional)")
    compliance = st.selectbox("Compliance", ["none", "hipaa", "soc2", "pci"])
    team_preference = st.selectbox("Team Preference", ["neutral", "aws", "azure", "gcp"])
    additional_context = st.text_area("Additional Context (optional)")
    submitted = st.form_submit_button("Analyze")

if submitted:
    with st.spinner("Analyzing your workload..."):
        payload = {
            "app_name": app_name,
            "workload_type": workload_type,
            "user_scale": user_scale,
            "traffic_pattern": traffic_pattern,
            "compute_preference": compute_preference,
            "database_type": database_type,
            "high_availability": high_availability,
            "disaster_recovery": disaster_recovery,
            "budget_priority": budget_priority,
            "preferred_region": preferred_region,
            "compliance": compliance,
            "team_preference": team_preference,
            "additional_context": additional_context,
        }

        try:
            response = requests.post("http://localhost:8000/analyze", json=payload)
            st.session_state.result = response.json()
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
            st.stop()

# --- Results ---
if "result" in st.session_state:
    if st.button("🔄 Start New Analysis"):
        del st.session_state.result
        st.rerun()

    result = st.session_state.result 

    recommendations = result.get("recommendations", [])
    best = result.get("best_provider", "").upper()


    # --- Best Provider Banner ---
    st.success(f"✅ Recommended Provider: **{best}**")

    # --- Architecture Summary ---
    st.subheader("Architecture Summary")
    st.write(result.get("architecture_summary", ""))

    # --- Assumptions ---
    with st.expander("Assumptions"):
        for a in result.get("assumptions", []):
            st.markdown(f"- {a}")

    st.divider()

    # --- Architecture Diagram ---
    st.subheader(f"Architecture Diagram — {best}")

    mermaid_diagram = result.get("mermaid_diagram")

    if mermaid_diagram:
        try:
            from streamlit_mermaid import st_mermaid
            st_mermaid(mermaid_diagram, height=500)
        except Exception:
            st.warning("Could not render diagram. Raw Mermaid definition:")
            st.code(mermaid_diagram, language="text")
    else:
        st.info("No architecture diagram was returned.")

    st.divider()

    # --- Provider Comparison Table ---
    st.subheader("Provider Comparison")

    df = pd.DataFrame([
        {
            "Provider": r["provider"].upper(),
            "Score": r["score"],
            "Min Cost ($/mo)": r.get("cost_estimate", {}).get("monthly_min", "N/A"),
            "Max Cost ($/mo)": r.get("cost_estimate", {}).get("monthly_max", "N/A"),
            "Compute": r.get("service_mapping", {}).get("compute", ""),
            "Database": r.get("service_mapping", {}).get("database", ""),
            "Network": r.get("service_mapping", {}).get("network", ""),
            "Observability": r.get("service_mapping", {}).get("observability", ""),
        }
        for r in recommendations
    ])

    st.dataframe(df, use_container_width=True)

    st.divider()

    # --- Cost Breakdown Table ---
    st.subheader("Cost Breakdown by Service")

    breakdown_rows = []
    for r in recommendations:
        breakdown = r.get("cost_estimate", {}).get("breakdown", {})
        row = {"Provider": r["provider"].upper()}
        row.update(breakdown)
        breakdown_rows.append(row)

    df_breakdown = pd.DataFrame(breakdown_rows).fillna("N/A")
    st.dataframe(df_breakdown, use_container_width=True)

    st.divider()

    # --- Score Comparison Chart ---
    st.subheader("Provider Score Comparison")

    providers = [r["provider"].upper() for r in recommendations]
    scores = [r["score"] for r in recommendations]

    fig_score = go.Figure(data=[
        go.Bar(
            x=providers,
            y=scores,
            marker_color=[
                "#f59e0b" if r["provider"] == result.get("best_provider") else "#60a5fa"
                for r in recommendations
            ],
            text=scores,
            textposition="outside",
        )
    ])

    fig_score.update_layout(
        yaxis_title="Score (0-100)",
        xaxis_title="Cloud Provider",
        yaxis_range=[0, 110],
        height=400,
    )

    st.plotly_chart(fig_score, use_container_width=True)

    st.divider()

    # --- Cost Breakdown Stacked Bar Chart ---
    st.subheader("Estimated Monthly Cost by Provider & Service")

    all_services = []
    for r in recommendations:
        for service in r.get("cost_estimate", {}).get("breakdown", {}).keys():
            if service not in all_services:
                all_services.append(service)

    service_colors = {
        "compute":       "#60a5fa",
        "database":      "#f59e0b",
        "storage":       "#34d399",
        "network":       "#a78bfa",
        "observability": "#fb923c",
    }

    fig_stacked = go.Figure()

    for service in all_services:
        values = []
        hover_texts = []
        for r in recommendations:
            breakdown = r.get("cost_estimate", {}).get("breakdown", {})
            raw = breakdown.get(service, "$0/mo")
            values.append(parse_cost_midpoint(raw))
            hover_texts.append(f"{service.capitalize()}: {raw}")

        fig_stacked.add_trace(go.Bar(
            name=service.capitalize(),
            x=providers,
            y=values,
            textposition="inside",
            hovertext=hover_texts,
            hovertemplate="%{hovertext}<extra></extra>",
            marker_color=service_colors.get(service, "#94a3b8"),
        ))

    fig_stacked.update_layout(
        barmode="stack",
        yaxis_title="Estimated USD / Month (midpoint)",
        xaxis_title="Cloud Provider",
        legend_title="Service",
        height=450,
        hovermode="x unified",
    )

    st.plotly_chart(fig_stacked, use_container_width=True)

    # --- Cost Range Line Chart ---
    st.subheader("Estimated Monthly Cost Range by Provider")

    min_costs = [r.get("cost_estimate", {}).get("monthly_min", 0) for r in recommendations]
    max_costs = [r.get("cost_estimate", {}).get("monthly_max", 0) for r in recommendations]
    avg_costs = [(mn + mx) // 2 for mn, mx in zip(min_costs, max_costs)]

    fig_cost = go.Figure()

    fig_cost.add_trace(go.Scatter(
        x=providers, y=max_costs,
        mode="lines+markers",
        name="Max Cost",
        line=dict(color="#f87171", width=2, dash="dash"),
        marker=dict(size=10),
    ))

    fig_cost.add_trace(go.Scatter(
        x=providers, y=avg_costs,
        mode="lines+markers",
        name="Avg Cost",
        line=dict(color="#60a5fa", width=3),
        marker=dict(size=10),
        fill="tonexty",
        fillcolor="rgba(248, 113, 113, 0.1)",
    ))

    fig_cost.add_trace(go.Scatter(
        x=providers, y=min_costs,
        mode="lines+markers",
        name="Min Cost",
        line=dict(color="#4ade80", width=2, dash="dash"),
        marker=dict(size=10),
        fill="tonexty",
        fillcolor="rgba(96, 165, 250, 0.1)",
    ))

    fig_cost.update_layout(
        yaxis_title="USD / Month",
        xaxis_title="Cloud Provider",
        legend_title="Cost Range",
        height=400,
        hovermode="x unified",
    )

    st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()

    # --- Terraform Output ---
    st.subheader(f"Terraform Starter — {best}")
    st.code(result.get("terraform", ""), language="hcl")