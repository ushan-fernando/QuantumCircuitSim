import numpy as np
import itertools

def possibleStates(numberOfQubits):
    states = [''.join(i) for i in itertools.product('01',repeat=numberOfQubits)]
    return states

def multiKroneckerProduct(*args):
    answer = args[0].value
    for i in range(1,len(args)):
        answer = np.kron(answer,args[i].value)
    return answer

def calcProbability(states):
    for i in range(len(states)):
        states[i] = np.abs(states[i])**2
    return states

class Qubit:
    def __init__(self):
        self.value = np.array([[1+0j],[0+0j]])

class QuantumCircuit:
    def __init__(self,numberOfQubits):
        self.numberOfQubits = numberOfQubits
        self.qubits = [Qubit() for _ in range(numberOfQubits)]

    def applyGate(self,gate,qubitNumber):
        if gate == 'X':
            pauliX = np.array([[0+0j,1+0j],[1+0j,0+0j]])
            q = Qubit()
            q.value = np.dot(pauliX,self.qubits[qubitNumber].value)
            self.qubits[qubitNumber] = q
        elif gate == 'Y':
            pauliY = np.array([[0+0j,0-1j],[0+1j,0+0j]])
            q = Qubit()
            q.value = np.dot(pauliY,self.qubits[qubitNumber].value)
            self.qubits[qubitNumber] = q
        elif gate == 'Z':
            pauliZ = np.array([[1,0],[0,-1]])
            q = Qubit()
            q.value = np.dot(pauliZ,self.qubits[qubitNumber].value)
            self.qubits[qubitNumber] = q
        elif gate == 'H':
            hadamard = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
            q = Qubit()
            q.value = np.dot(hadamard,self.qubits[qubitNumber].value)
            self.qubits[qubitNumber] = q
    
    def runCircuit(self):
        states = multiKroneckerProduct(*self.qubits)
        probs = calcProbability(states).flatten()
        possibilities = possibleStates(self.numberOfQubits)
        return [i for i in zip(possibilities,probs.real)]



