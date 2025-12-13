import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="MindCheck - Mental Health AI", layout="centered")

st.markdown("""
<style>
/* --- App Background --- */
.stApp {
    background: radial-gradient(circle at top, #1b1f3b, #0b0e1a);
    color: #e6e6ff;
    font-family: 'Segoe UI', sans-serif;
}

/* --- Title Card --- */
.main-title {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, #6a5acd, #00bcd4);
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 0 30px rgba(106, 90, 205, 0.6);
}

/* --- Section Titles --- */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 35px;
    color: #c6b7ff;
}

/* --- Question Cards --- */
.question-box {
    background: rgba(255, 255, 255, 0.08);
    padding: 16px 20px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 0 18px rgba(0, 188, 212, 0.15);
    margin-bottom: 10px;
    color: #f2f2ff;
}

/* --- Radio Buttons Text --- */
div[role="radiogroup"] label {
    color: #e0e0ff !important;
}

/* --- Divider Glow --- */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #6a5acd, transparent);
    margin: 30px 0;
}

/* --- Footer --- */
.footer-text {
    text-align: center;
    font-size: 13px;
    color: #aaa;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# --------- Helper Functions ----------
def calculate_scores(responses):
    phq = sum(responses[:9])
    gad = sum(responses[9:])
    total = phq + gad
    return phq, gad, total

def interpret_score(score):
    if score <= 9:
        return "Low", "#4CAF50", "Your symptoms appear mild. Maintain healthy routines."
    elif score <= 18:
        return "Moderate", "#ff9800", "You’re experiencing noticeable stress. Consider stress-management techniques."
    else:
        return "High", "#f44336", "Your emotional state may be significantly affected. Professional support may help."

def render_chart(phq, gad):
    fig = go.Figure()
    fig.add_bar(name="Depression (PHQ-9)", x=["Assessment"], y=[phq])
    fig.add_bar(name="Anxiety (GAD-7)", x=["Assessment"], y=[gad])

    fig.update_layout(
        title="🧩 Emotional State Overview",
        barmode="group",
        yaxis_title="Score",
        showlegend=True
    )
    return fig

# --------- UI ----------
st.markdown(
    "<div class='main-title'><h2>🧠 MindCheck - Mental Health Self Assessment</h2></div>",
    unsafe_allow_html=True
)

st.write("Your responses are **anonymous**. This tool is for **self-awareness**, not diagnosis.")
st.divider()

questions = {
    "PHQ-9 (Depression Scale)": [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling asleep or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself or like a failure",
        "Trouble concentrating on tasks",
        "Moving slowly or feeling restless",
        "Thoughts of self-harm or not wanting to be alive",
    ],
    "GAD-7 (Anxiety Scale)": [
        "Feeling nervous or on edge",
        "Unable to stop worrying",
        "Worrying about many things",
        "Trouble relaxing",
        "Restlessness",
        "Becoming irritated easily",
        "Feeling afraid something awful might happen",
    ]
}

options = [
    "Not at all (0)",
    "Several days (1)",
    "More than half the days (2)",
    "Nearly every day (3)"
]

if "history" not in st.session_state:
    st.session_state.history = []

responses = []

for section, qs in questions.items():
    st.markdown(f"<div class='section-title'>{section}</div>", unsafe_allow_html=True)
    for q in qs:
        st.markdown(f"<div class='question-box'>{q}</div>", unsafe_allow_html=True)
        choice = st.radio("", options, index=0, key=q)
        responses.append(int(choice[-2]))

if st.button("🔍 Analyze My Mental Health", use_container_width=True):
    phq, gad, total = calculate_scores(responses)
    level, color, msg = interpret_score(total)
    
    st.session_state.history.append({
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "phq": phq,
    "gad": gad,
    "total": total,
    "level": level
})

    st.divider()
    st.markdown(f"<h3 style='color:{color};'>Risk Level: {level}</h3>", unsafe_allow_html=True)
    st.write(f"**Total Score:** {total}")
    st.write(f"**Recommendation:** {msg}")

    # Ethical safeguard
    if responses[8] > 0:
        st.warning(
            "If you're experiencing thoughts of self-harm, please consider reaching out to a trusted person or mental health professional."
        )

    fig = render_chart(phq, gad)
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<p class='footer-text'>✨ This assessment is for educational purposes only and does not replace professional care.</p>",
    unsafe_allow_html=True
)
