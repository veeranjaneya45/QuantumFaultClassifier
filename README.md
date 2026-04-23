# ⚛️ QUANTUM MULTI-FAULT DETECTION SIMULATOR

### *Deutsch–Jozsa Algorithm + Fidelity-Based Validation*

---

---

## 🌌 PROJECT OVERVIEW

This project simulates a **Quantum Multi-Fault Detection System** using the
**Deutsch–Jozsa Algorithm** and validates the results using **Fidelity Analysis**.

It allows users to:

* Inject faults into subsystems
* Simulate quantum classification
* Analyze confidence using fidelity
* Observe system behavior under noise

---

## 🧠 CORE IDEA

> ⚡ Replace classical fault detection with **quantum-inspired classification + reliability validation**

### Flow:

```text
User Input → Fault Encoding → Quantum Circuit → Classification → Fidelity → Decision
```

---

## 🧩 SYSTEM COMPONENTS

| Bit | Subsystem     |
| --- | ------------- |
| 1   | Sensor        |
| 2   | Actuator      |
| 3   | Communication |

---

## 🔢 FAULT REPRESENTATION

| Pattern | Meaning                  |
| ------- | ------------------------ |
| 000     | No Fault                 |
| 001     | Communication Fault      |
| 010     | Actuator Fault           |
| 011     | Actuator + Communication |
| 100     | Sensor Fault             |
| 101     | Sensor + Communication   |
| 110     | Sensor + Actuator        |
| 111     | All Faults               |

---

## ⚙️ FEATURES

### 🧩 Fault Simulation

* Checkbox-based subsystem faults
* Manual binary override input

### ⚛️ Quantum Processing

* Deutsch–Jozsa Algorithm
* Balanced vs Constant classification
* Qiskit AerSimulator backend

### 🎯 Fidelity Validation

* Dynamic fidelity calculation
* Severity-based variation
* Noise-aware degradation

### 🌪️ Noise Simulation

* Adjustable noise strength
* Realistic uncertainty modeling

### 📊 Visualization

* Interactive dashboard
* Charts + metrics + circuit display

### 🚨 Decision System

* Reliable / Warning / Uncertain states
* Automated recommendation engine

---

## 🎮 LIVE DEMO

👉 https://quantumfaultclassifier.streamlit.app/

---

## 🖥️ UI PREVIEW

> ⚛️ Quantum Dashboard with futuristic styling, real-time simulation, and intelligent outputs.

---

## 🛠️ TECH STACK

| Layer           | Technology      |
| --------------- | --------------- |
| Frontend        | Streamlit       |
| Backend         | Python          |
| Quantum Engine  | Qiskit          |
| Visualization   | Matplotlib      |
| Deployment      | Streamlit Cloud |
| Version Control | Git + GitHub    |

---

## 🧪 HOW IT WORKS

### 1️⃣ Input Phase

* User selects faults or enters binary pattern

### 2️⃣ Encoding Phase

* Pattern converted to quantum input

### 3️⃣ Quantum Execution

* Oracle constructed
* Deutsch–Jozsa circuit executed

### 4️⃣ Classification

* Output → Constant or Balanced

### 5️⃣ Validation

* Fidelity score computed
* Noise applied (optional)

### 6️⃣ Decision

* Final system diagnosis generated

---

## 🎯 FIDELITY LOGIC

| Condition          | Fidelity         |
| ------------------ | ---------------- |
| Correct + No Noise | High (0.90–0.98) |
| Correct + Noise    | Medium           |
| Incorrect          | Low              |

---

## 🌐 DEPLOYMENT

Deployed using **Streamlit Community Cloud**

Steps:

1. Push code to GitHub
2. Connect repository
3. Select `app.py`
4. Deploy

---

## 🧠 FUTURE IMPROVEMENTS

* Real Quantum NoiseModel (Qiskit)
* Multi-qubit scaling (n > 3)
* PDF report export
* API integration
* Real-time IoT fault input

---

## 🎓 ACADEMIC VALUE

✔ Demonstrates quantum computing concepts
✔ Combines AI + simulation + validation
✔ Shows practical system design
✔ Includes uncertainty modeling

---

## 🏁 CONCLUSION

This project transforms fault detection into a **quantum-inspired intelligent system**
with **confidence validation and dynamic simulation**.

---

## 👨‍💻 AUTHOR

**P VEERANJANEYA REDDY**
Cyber Security Engineer | AI Developer | Systems Builder

---

## ⭐ SUPPORT

If you like this project:

⭐ Star this repo
🚀 Share with others
💡 Use it for learning

---

## ⚡ FINAL LINE

> “Not just detecting faults… but validating them with quantum confidence.”

---
