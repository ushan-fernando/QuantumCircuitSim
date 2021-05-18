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
q.addGate("CNOT",1,1,[0])
q.runCircuit()

"""
Below code implements the following circuit:
|0> ---|X|----o---
              |
|0> ---|X|----o---
              |
|0> ---------|X|--
"""
q = QuantumCircuit(3)
q.addColumn()
q.addGate("X",0,0)
q.addGate("X",0,1)
q.addColumn()
q.addGate("Toffoli",1,2,[0,1])
q.runCircuit()