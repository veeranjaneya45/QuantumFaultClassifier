from qiskit import QuantumCircuit


def create_balanced_oracle(n):
    oracle = QuantumCircuit(n + 1)
    for qubit in range(n):
        oracle.cx(qubit, n)
    return oracle


def create_constant_oracle(n, output=0):
    oracle = QuantumCircuit(n + 1)
    if output == 1:
        oracle.x(n)
    return oracle