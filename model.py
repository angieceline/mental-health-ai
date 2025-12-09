# model.py

import numpy as np

def calculate_risk_score(responses):
    # Responses are 0 to 3 each (PHQ-9 style scoring)
    score = np.sum(responses)

    if score <= 4:
        return score, "Low", "You're doing okay. Maintain healthy habits."
    elif score <= 9:
        return score, "Mild", "You may be experiencing mild stress. Consider journaling or relaxation exercises."
    elif score <= 14:
        return score, "Moderate", "This may be affecting your daily life. Talking to someone you trust may help."
    else:
        return score, "High", "It is recommended to consult a mental health professional for support."
