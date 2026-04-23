def compute_simple_fidelity(expected_label, predicted_label):
    if expected_label == predicted_label:
        return 0.95
    return 0.65

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