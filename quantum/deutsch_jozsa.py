from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_deutsch_jozsa_circuit(n, oracle):
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)

    for i in range(n + 1):
        qc.h(i)

    qc.compose(oracle, inplace=True)

    for i in range(n):
        qc.h(i)

    for i in range(n):
        qc.measure(i, i)

    return qc


def run_circuit(qc, shots=1024):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts()
    return counts