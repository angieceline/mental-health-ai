import streamlit as st
import plotly.graph_objects as go

st.title("📈 Mood Tracking Over Time")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("No assessments recorded yet.")
else:
    dates = [h["timestamp"] for h in st.session_state.history]
    totals = [h["total"] for h in st.session_state.history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=totals,
        mode="lines+markers",
        name="Mental Health Score"
    ))

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Score",
        title="Mental Health Trend"
    )

    st.plotly_chart(fig, use_container_width=True)
