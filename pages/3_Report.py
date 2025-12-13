import streamlit as st
from utils import generate_pdf

st.title("📄 Download Your Report")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.warning("No assessment data available.")
else:
    latest = st.session_state.history[-1]

    pdf = generate_pdf(
        latest["phq"],
        latest["gad"],
        latest["total"],
        latest["level"]
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="MindCheck_Report.pdf",
        mime="application/pdf"
    )
