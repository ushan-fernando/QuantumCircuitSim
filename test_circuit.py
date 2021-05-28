from quantum import QuantumCircuit

"""
Below code implements the following circuit:
Bell State: Quantum Entaglement
|0> ---|H|----o---
              |
|0> ---------|X|--
"""

qc = QuantumCircuit(2)
qc.h(0)
qc.cnot(0,1)
qc.runCircuit()

"""
Below code implements the following circuit:
|0> ---|X|----o---
              |
|0> ---|X|----o---
              |
|0> ---------|X|--
"""
qc = QuantumCircuit(3)
qc.x(0)
qc.x(1)
qc.toffoli(0,1,2)
qc.runCircuit()