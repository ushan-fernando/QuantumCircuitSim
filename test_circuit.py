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


def superDenseCoding(message):
    q = QuantumCircuit(2)
    q.addColumn()
    q.addGate("H",0,0)
    q.addColumn()
    q.addGate("CNOT",1,1,0)

    if message == "00":
        q.addColumn()
        q.addColumn()
        q.addGate("CNOT",2,1,0)
        q.addColumn()
        q.addGate("H",3,0)
    elif message == "01":
        q.addColumn()
        q.addGate("X",2,0)
        q.addColumn()
        q.addGate("CNOT",3,1,0)
        q.addColumn()
        q.addGate("H",4,0)
    elif message == "10":
        q.addColumn()
        q.addGate("Z",2,0)
        q.addColumn()
        q.addGate("CNOT",3,1,0)
        q.addColumn()
        q.addGate("H",4,0)
    elif message == "11":
        q.addColumn()
        q.addGate("X",2,0)
        q.addColumn()
        q.addGate("Z",3,0)
        q.addColumn()
        q.addGate("CNOT",4,1,0)
        q.addColumn()
        q.addGate("H",5,0)
    
    return q.runCircuit()

result = superDenseCoding("10")
print(result)