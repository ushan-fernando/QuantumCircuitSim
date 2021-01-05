import numpy as np
import itertools

class Qubit:
    def __init__(self):
        self.value = np.array([[1+0j],[0+0j]])

def possibleStates(numberOfQubits):
    states = [''.join(i) for i in itertools.product('01',repeat=numberOfQubits)]
    return states

def multiKroneckerProduct(*args):
    if isinstance(args[0],Qubit):
        answer = args[0].value
        for i in range(1,len(args)):
            answer = np.kron(answer,args[i].value)
        return answer
    else:
        answer = args[0]
        for i in range(1,len(args)):
            answer = np.kron(answer,args[i])
        return answer

def calcProbability(states):
    for i in range(len(states)):
        states[i] = np.abs(states[i])**2
    return states

class QuantumCircuit:
    def __init__(self,numberOfQubits):
        self.numberOfQubits = numberOfQubits
        self.qubits = [Qubit() for _ in range(numberOfQubits)]
        self.columns = []
    
    def addColumn(self):
        identity = np.array([[1+0j,0+0j],[0+0j,1+0j]])
        self.columns.append([identity for _ in range(self.numberOfQubits)])
    
    def addGate(self,gate,columnNumber,qubitNumber,control=None):
        if control == None:
            if gate == 'X':
                pauliX = np.array([[0+0j,1+0j],[1+0j,0+0j]])
                self.columns[columnNumber][qubitNumber] = pauliX
            elif gate == 'Y':
                pauliY = np.array([[0+0j,0-1j],[0+1j,0+0j]])
                self.columns[columnNumber][qubitNumber] = pauliY
            elif gate == 'Z':
                pauliZ = np.array([[1,0],[0,-1]])
                self.columns[columnNumber][qubitNumber] = pauliZ
            elif gate == 'H':
                hadamard = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
                self.columns[columnNumber][qubitNumber] = hadamard
            else:
                raise Exception("Given Gate Doesn't Exist")

        if gate == "CNOT":
            identity = np.array([[1+0j,0+0j],[0+0j,1+0j]])
            pauliX = np.array([[0+0j,1+0j],[1+0j,0+0j]])
            p0 = np.array([[1,0],[0,0]])
            p1 = np.array([[0,0],[0,1]])
            a1 = [identity for _ in range(self.numberOfQubits)]
            a2 = [identity for _ in range(self.numberOfQubits)]
            a1[control] = p0
            a2[control] = p1
            a2[qubitNumber] = pauliX
            cnot = multiKroneckerProduct(*a1) + multiKroneckerProduct(*a2)
            self.columns[columnNumber] = [1 for _ in range(self.numberOfQubits)]
            self.columns[columnNumber][qubitNumber] = cnot


    def runCircuit(self):
        states = multiKroneckerProduct(*self.qubits)
        for i in range(len(self.columns)):
            states = np.dot(multiKroneckerProduct(*self.columns[i]),states)
        possibilities = possibleStates(self.numberOfQubits)
        prob = calcProbability(states).flatten()
        return [i for i in zip(possibilities,prob.real)]





