import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from quantum.oracle import create_balanced_oracle, create_constant_oracle
from quantum.deutsch_jozsa import build_deutsch_jozsa_circuit, run_circuit
from quantum.simulator import classify_counts
from quantum.fidelity import compute_simple_fidelity, validate_fidelity, final_decision


# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Quantum Multi-Fault Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0a0f1f, #111827, #1f2937);
    color: white;
}
h1, h2, h3, h4 {
    color: #00e5ff;
    font-family: 'Segoe UI', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0a0f1f, #111827, #1f2937);
}
.stMarkdown, .stText, .stSubheader, .stHeader, label, div, p {
    color: white !important;
}
.stButton > button {
    background: linear-gradient(90deg, #00e5ff, #7c3aed);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.7rem 1.2rem;
    font-weight: bold;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #7c3aed, #00e5ff);
    color: white;
}
.metric-card {
    background: rgba(255,255,255,0.06);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 0 12px rgba(0,229,255,0.20);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    min-height: 140px;
}
.result-box {
    padding: 18px;
    border-radius: 16px;
    margin-top: 10px;
    font-weight: bold;
    font-size: 18px;
}
.green-box {
    background: rgba(34,197,94,0.15);
    border: 1px solid #22c55e;
}
.yellow-box {
    background: rgba(234,179,8,0.15);
    border: 1px solid #eab308;
}
.red-box {
    background: rgba(239,68,68,0.15);
    border: 1px solid #ef4444;
}
.glow-title {
    font-size: 40px;
    font-weight: 800;
    color: #00e5ff;
    text-align: center;
    text-shadow: 0 0 15px rgba(0,229,255,0.6);
    margin-bottom: 5px;
}
.subtext {
    text-align: center;
    color: #cbd5e1 !important;
    font-size: 18px;
    margin-bottom: 20px;
}
.pattern-box {
    background: rgba(124,58,237,0.20);
    border: 1px solid #7c3aed;
    padding: 12px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-top: 10px;
}
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: bold;
    margin-top: 6px;
}
.normal-badge {
    background: rgba(34,197,94,0.20);
    color: #86efac;
    border: 1px solid #22c55e;
}
.low-badge {
    background: rgba(59,130,246,0.20);
    color: #93c5fd;
    border: 1px solid #3b82f6;
}
.medium-badge {
    background: rgba(234,179,8,0.20);
    color: #fde047;
    border: 1px solid #eab308;
}
.high-badge {
    background: rgba(239,68,68,0.20);
    color: #fca5a5;
    border: 1px solid #ef4444;
}
.info-strip {
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.25);
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 14px;
}
hr {
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# Helper Functions
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
        return "System is stable. No action needed."
    elif severity == "Low":
        return "Check the affected subsystem."
    elif severity == "Medium":
        return "Run detailed diagnostics and corrective maintenance."
    return "CRITICAL: Immediate intervention required!"


def card(title, value):
    st.markdown(f"""
    <div class="metric-card">
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)


def status_box(status, message):
    if status == "Reliable":
        css_class = "green-box"
    elif status == "Warning":
        css_class = "yellow-box"
    else:
        css_class = "red-box"

    st.markdown(f"""
    <div class="result-box {css_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)


def severity_badge(severity):
    badge_class = {
        "Normal": "normal-badge",
        "Low": "low-badge",
        "Medium": "medium-badge",
        "High": "high-badge"
    }.get(severity, "normal-badge")

    st.markdown(
        f'<div class="badge {badge_class}">{severity} Severity</div>',
        unsafe_allow_html=True
    )


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("⚛️ Quantum Panel")
    st.markdown("### Project Modules")
    st.write("• Fault Input")
    st.write("• Error Identification")
    st.write("• Quantum Classification")
    st.write("• Fidelity Validation")
    st.write("• Final Diagnosis")

    st.markdown("### Components")
    st.write("Bit 1 → Sensor")
    st.write("Bit 2 → Actuator")
    st.write("Bit 3 → Communication")

    st.markdown("### Backend")
    st.write("• Simulator: AerSimulator")
    st.write("• Algorithm: Deutsch–Jozsa")
    st.write("• Validation: Fidelity")

    st.markdown("### Noise Model")
    st.write("• Optional noisy execution")
    st.write("• Random fidelity degradation")
    st.write("• Simulated uncertainty")


# ----------------------------
# Hero Section
# ----------------------------
st.markdown('<div class="glow-title">⚛️ Quantum Multi-Fault Detection Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Deutsch–Jozsa Algorithm with Fidelity-Based Validation</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="info-strip">Input subsystem faults, run quantum classification, and observe how noise affects fidelity and decision confidence.</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ----------------------------
# Input Section
# ----------------------------
left, right = st.columns(2)

with left:
    st.subheader("🧩 Fault Input")
    sensor = st.checkbox("Sensor Fault")
    actuator = st.checkbox("Actuator Fault")
    communication = st.checkbox("Communication Fault")

with right:
    st.subheader("🧠 Manual Override")
    manual_input = st.text_input("Enter 3-bit binary pattern manually", value="")

noise_col1, noise_col2 = st.columns(2)

with noise_col1:
    noise_mode = st.checkbox("Enable Noise Simulation")

with noise_col2:
    noise_strength = st.slider("Noise Strength", 0.00, 0.30, 0.15, 0.01)

generated_pattern = (
    ("1" if sensor else "0") +
    ("1" if actuator else "0") +
    ("1" if communication else "0")
)

binary_pattern = generated_pattern

if manual_input:
    if len(manual_input) == 3 and all(bit in "01" for bit in manual_input):
        binary_pattern = manual_input
    else:
        st.error("Enter valid 3-bit binary (only 0 and 1)")

st.subheader("🔢 Active Binary Pattern")
st.markdown(f'<div class="pattern-box">{binary_pattern}</div>', unsafe_allow_html=True)


# ----------------------------
# Run Button
# ----------------------------
if st.button("🚀 Run Simulator"):
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

    fidelity = compute_simple_fidelity(
        expected_label=expected_type,
        predicted_label=predicted_type,
        noise=noise_mode,
        severity=severity,
        noise_strength=noise_strength
    )

    status = validate_fidelity(fidelity)
    decision = final_decision(predicted_type, fidelity)
    advice = recommendation(severity)

    counts_df = pd.DataFrame({
        "State": list(counts.keys()),
        "Counts": list(counts.values())
    })

    # ----------------------------
    # Tabs
    # ----------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚙️ Input & Faults",
        "🧪 Simulation",
        "📊 Results",
        "✅ Diagnosis"
    ])

    with tab1:
        st.subheader("Fault Identification")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card("Fault Pattern", binary_pattern)
        with c2:
            card("Fault Count", fault_count)
        with c3:
            card("Detected Error", detected_fault)
        with c4:
            card("Expected Type", expected_type)

        st.write("")
        st.subheader("Severity")
        severity_badge(severity)

    with tab2:
        st.subheader("Quantum Simulation")
        q1, q2, q3 = st.columns(3)

        with q1:
            card("Predicted Type", predicted_type)
        with q2:
            card("Validation Status", status)
        with q3:
            card("Noise Mode", "Enabled" if noise_mode else "Disabled")

        st.write("### Measurement Counts")
        st.dataframe(counts_df, use_container_width=True)

        with st.expander("View Quantum Circuit"):
            st.text(qc.draw(output="text"))

    with tab3:
        st.subheader("Result Analytics")

        st.write("### Count Distribution")
        st.bar_chart(counts_df.set_index("State"))

        st.write("### Fidelity Confidence")
        st.progress(min(int(fidelity * 100), 100))
        st.write(f"Fidelity Score: **{fidelity:.2f}**")

        st.write("### Noise Details")
        st.write(f"Noise Enabled: **{'Yes' if noise_mode else 'No'}**")
        st.write(f"Noise Strength: **{noise_strength:.2f}**")

        fig, ax = plt.subplots()
        ax.bar(["Fidelity"], [fidelity])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Score")
        st.pyplot(fig)

    with tab4:
        st.subheader("🚨 Final Diagnosis")
        status_box(status, decision)

        st.write("### Recommendation")
        st.info(advice)

        st.write("### Summary")
        s1, s2, s3 = st.columns(3)
        with s1:
            card("Detected Error", detected_fault)
        with s2:
            card("Severity", severity)
        with s3:
            card("Fidelity", f"{fidelity:.2f}")


# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "<center><b>Built as a Quantum Fault Detection Research Simulator</b><br>"
    "Deutsch–Jozsa Algorithm • Fidelity Validation • Interactive Dashboard</center>",
    unsafe_allow_html=True
)