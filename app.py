import streamlit as st
import matplotlib.pyplot as plt

from quantum.oracle import create_balanced_oracle, create_constant_oracle
from quantum.deutsch_jozsa import build_deutsch_jozsa_circuit, run_circuit
from quantum.simulator import classify_counts
from quantum.fidelity import compute_simple_fidelity, validate_fidelity, final_decision

st.set_page_config(page_title="Quantum Multi-Fault Simulator", layout="wide")

st.title("Quantum Multi-Fault Detection Simulator")
st.subheader("Using Deutsch–Jozsa Algorithm with Fidelity-Based Validation")

st.markdown("Select subsystem faults below. The simulator will generate the binary pattern, identify the error, and validate the result.")

# ----------------------------
# Fault identification helpers
# ----------------------------
def identify_fault(binary_pattern):
    fault_map = {
        "000": "No fault",
        "001": "Communication fault",
        "010": "Actuator fault",
        "011": "Actuator + Communication fault",
        "100": "Sensor fault",
        "101": "Sensor + Communication fault",
        "110": "Sensor + Actuator fault",
        "111": "Sensor + Actuator + Communication fault"
    }
    return fault_map.get(binary_pattern, "Unknown fault pattern")

def count_faults(binary_pattern):
    return binary_pattern.count("1")

def fault_severity(binary_pattern):
    count = count_faults(binary_pattern)
    if count == 0:
        return "Normal"
    elif count == 1:
        return "Low"
    elif count == 2:
        return "Medium"
    return "High"

def expected_type_from_pattern(binary_pattern):
    if binary_pattern == "000":
        return "constant"
    return "balanced"

def recommendation(severity):
    if severity == "Normal":
        return "System is stable. No corrective action needed."
    elif severity == "Low":
        return "Inspect the faulty subsystem."
    elif severity == "Medium":
        return "Perform detailed diagnosis and corrective maintenance."
    return "Critical condition. Immediate intervention required."

# ----------------------------
# Input section
# ----------------------------
st.write("## Fault Input")

col1, col2, col3 = st.columns(3)

with col1:
    sensor = st.checkbox("Sensor Fault")

with col2:
    actuator = st.checkbox("Actuator Fault")

with col3:
    communication = st.checkbox("Communication Fault")

binary_pattern = (
    ("1" if sensor else "0") +
    ("1" if actuator else "0") +
    ("1" if communication else "0")
)
# Manual override input
manual_input = st.text_input("Or enter 3-bit binary pattern manually", value=binary_pattern)

# Validate and override pattern
if len(manual_input) == 3 and all(bit in "01" for bit in manual_input):
    binary_pattern = manual_input
else:
    st.warning("Enter a valid 3-bit binary pattern (only 0 and 1)")
st.write("### Generated Binary Pattern")
st.code(binary_pattern)

noise_mode = st.checkbox("Enable Noise Simulation")

# ----------------------------
# Run simulation
# ----------------------------
if st.button("Run Simulator"):
    detected_fault = identify_fault(binary_pattern)
    fault_count = count_faults(binary_pattern)
    severity = fault_severity(binary_pattern)
    expected_type = expected_type_from_pattern(binary_pattern)

    n = len(binary_pattern)

    if expected_type == "constant":
        oracle = create_constant_oracle(n)
    else:
        oracle = create_balanced_oracle(n)

    qc = build_deutsch_jozsa_circuit(n, oracle)
    counts = run_circuit(qc)
    predicted_type = classify_counts(counts, n)

    fidelity = compute_simple_fidelity(expected_type, predicted_type)

    if noise_mode:
        fidelity = max(0.0, fidelity - 0.20)

    status = validate_fidelity(fidelity)
    decision = final_decision(predicted_type, fidelity)
    advice = recommendation(severity)

    # ----------------------------
    # Display results
    # ----------------------------
    st.write("## Error Identification")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Fault Pattern", binary_pattern)
    with c2:
        st.metric("Detected Error", detected_fault)
    with c3:
        st.metric("Fault Count", fault_count)
    with c4:
        st.metric("Severity", severity)

    st.write("## Quantum Simulation")

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric("Expected Type", expected_type)
    with q2:
        st.metric("Predicted Type", predicted_type)
    with q3:
        st.metric("Validation Status", status)

    st.write("### Measurement Counts")
    st.write(counts)

    st.write("### Quantum Circuit")
    st.text(qc.draw(output="text"))

    st.write("## Fidelity Validation")
    st.metric("Fidelity Score", f"{fidelity:.2f}")

    fig, ax = plt.subplots()
    ax.bar(["Fidelity"], [fidelity])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    st.pyplot(fig)

    st.write("## Final Diagnosis")
    st.success(decision)

    st.write("### Recommendation")
    st.info(advice)