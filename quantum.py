import numpy as np
import matplotlib.pyplot as plt
import itertools

# Define a qubit object which initialises the qubit |0>
class Qubit:
    def __init__(self):
        self.value = np.array([[1+0j],[0+0j]])

# Generate the binary permutations based on number of qubits
# This is used to generate the measurement possibilities
# e.g. For 2 qubits the possible outcomes after measuring can be 00, 01, 10, 11
def possibleStates(numberOfQubits):
    states = [''.join(i) for i in itertools.product('01',repeat=numberOfQubits)]
    return states

# Calculates the kronecker product ⊗ of all the arguments given
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

# Calculates the probability of measuring each of the states as given by the function possibleStates
def calcProbability(states):
    for i in range(len(states)):
        states[i] = np.abs(states[i])**2
    return states

# Quantum Circuit object which the user will use to add gates and perform the computation
class QuantumCircuit:
    # Initialises the quantum circuit by:
    # -Setting number of qubits 
    # -Making a list of qubit objects with a length given by number of quibits
    # -Initialises the list of columns
    def __init__(self,numberOfQubits):
        self.numberOfQubits = numberOfQubits
        self.qubits = [Qubit() for _ in range(numberOfQubits)]
        self.columns = []

    # Adds a new column to the circuit
    # visual below:
    #        c1   c2
    # |0> -- X -- H --
    # |0> -- X -- Z --
    # |0> ------------
    # A new column is initialised with all identity gates
    def addColumn(self):
        identity = np.array([[1+0j,0+0j],[0+0j,1+0j]])
        self.columns.append([identity for _ in range(self.numberOfQubits)])
    
    # Add a gate to a given column and qubit
    # Current gates supported are:
    # Pauli Gates, Hadamard, and CNOT
    def addGate(self,gate,columnNumber,qubitNumber,control=None):
        # For single qubit gates we just add the gate matrix to the corresponding position in column array
        if control == None:
            if gate == 'X':
                pauliX = np.array([[0+0j,1+0j],[1+0j,0+0j]])
                self.columns[columnNumber][qubitNumber] = pauliX
            elif gate == 'Y':
                pauliY = np.array([[0+0j,0-1j],[0+1j,0+0j]])
                self.columns[columnNumber][qubitNumber] = pauliY
            elif gate == 'Z':
                pauliZ = np.array([[1+0j,0+0j],[0+0j,-1+0j]])
                self.columns[columnNumber][qubitNumber] = pauliZ
            elif gate == 'H':
                hadamard = 1/np.sqrt(2) * np.array([[1+0j,1+0j],[1+0j,-1+0j]])
                self.columns[columnNumber][qubitNumber] = hadamard
            else:
                raise Exception("Given Gate Doesn't Exist")
        
        # For controlled gates such as CNOT we need to calculate its matrix representation given the
        # control and target qubit. Then we add the matrix to the corresponding position in the column array
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

    # Calculates the final state of the quamtum circuit after applying all the gates
    # It then calculates the probabilities of measuring each state and shows a visulisation
    # graph using matplotlib
    def runCircuit(self):
        states = multiKroneckerProduct(*self.qubits)
        for i in range(len(self.columns)):
            states = np.dot(multiKroneckerProduct(*self.columns[i]),states)
        possibilities = possibleStates(self.numberOfQubits)
        prob = calcProbability(states).flatten()
        self.visualize(possibilities,prob.real)
    
    # Visualisation of probabilities of measuring the states
    def visualize(self,possibilities,probalities):
        plt.title("Quantum Circuit Simulation")
        plt.bar(range(2**self.numberOfQubits),probalities)
        plt.xticks(range(2**self.numberOfQubits),possibilities)
        plt.ylim(-0,1)
        plt.grid(True)
        plt.ylabel(r'$P(|\psi\rangle)$')
        plt.xlabel(r'$|\psi\rangle$')
        plt.show()






