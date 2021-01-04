from quantum import QuantumCircuit

"""
Below code implements the following circuit:
|0> ---|H|-----
|0> ---|X|-----
"""

q = QuantumCircuit(2)
q.applyGate('H',0)
q.applyGate('X',1)
answer = q.runCircuit()
print(answer)