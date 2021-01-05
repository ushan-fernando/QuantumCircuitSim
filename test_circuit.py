from quantum import QuantumCircuit

"""
Below code implements the following circuit:
Bell State: Quantum Entaglement
|0> ---|H|----o---
              |
|0> ---------|X|--
"""

q = QuantumCircuit(2)
q.addColumn()
q.addGate("H",0,0)
q.addColumn()
q.addGate("CNOT",1,1,0)
answer = q.runCircuit()
print(answer)