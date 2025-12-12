import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MindCheck - Mental Health AI", layout="centered")

st.App {
    background-color: "#fde8f1" 
}

st.markdown("""
<style>
    body {
        background-color: #fde8f1;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6a8dff, #9ac6ff);
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-box {
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 25px;
    }
    .footer-text {
        text-align: center;
        font-size: 13px;
        color: #666;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'><h2>🧠 MindCheck - Mental Health Self Assessment</h2></div>", unsafe_allow_html=True)

st.write("Your responses are **anonymous**. This tool is for **self-awareness**, not clinical diagnosis.")

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

options = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
responses = []

for section, qs in questions.items():
    st.markdown(f"<div class='section-title'>{section}</div>", unsafe_allow_html=True)
    for q in qs:
        with st.container():
            st.markdown(f"<div class='question-box'>{q}</div>", unsafe_allow_html=True)
            choice = st.radio("", options, index=0, key=q)
            responses.append(int(choice[-2]))

if st.button("🔍 Analyze My Mental Health", use_container_width=True):
    score = np.sum(responses)

    if score <= 9:
        level, color, msg = "Low", "#4CAF50", "Your symptoms appear mild. Keep taking care of yourself."
    elif score <= 18:
        level, color, msg = "Moderate", "#ff9800", "You're experiencing noticeable stress. Healthy support practices can help."
    else:
        level, color, msg = "High", "#f44336", "Your emotional state may be significantly affected. Consider reaching out to a mental health professional."

    st.divider()
    st.markdown(f"<h3 style='color:{color};'>Risk Level: {level}</h3>", unsafe_allow_html=True)
    st.write(f"**Total Score:** {score}")
    st.write(f"**Recommendation:** {msg}")

    phq_sum = np.sum(responses[:9])
    gad_sum = np.sum(responses[9:])

    fig = go.Figure(data=go.Scatterpolar(
        r=[phq_sum, gad_sum],
        theta=["PHQ-9 (Depression)", "GAD-7 (Anxiety)"],
        fill='toself'
    ))

    fig.update_layout(title="🧩 Emotional State Visualization", showlegend=False)
    st.plotly_chart(fig)

st.markdown("<p class='footer-text'>✨ This assessment is educational and reflective. If you're struggling, please talk to someone who can support you.</p>", unsafe_allow_html=True)

