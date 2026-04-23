import random


def compute_simple_fidelity(expected_label, predicted_label, noise=False, severity="Normal", noise_strength=0.15):
    if expected_label == predicted_label:
        base = random.uniform(0.90, 0.98)
    else:
        base = random.uniform(0.55, 0.75)

    if severity == "Medium":
        base -= 0.03
    elif severity == "High":
        base -= 0.06

    if noise:
        base -= random.uniform(0.05, noise_strength)

    return round(max(0.0, min(base, 1.0)), 2)


def validate_fidelity(fidelity, threshold=0.85):
    if fidelity >= threshold:
        return "Reliable"
    elif fidelity >= 0.70:
        return "Warning"
    return "Uncertain"


def final_decision(predicted_type, fidelity):
    if fidelity >= 0.85:
        return f"{predicted_type.upper()} detected - Accept Result"
    elif fidelity >= 0.70:
        return f"{predicted_type.upper()} detected - Recheck Recommended"
    return "Ambiguous Result - Retry or Classical Verification"