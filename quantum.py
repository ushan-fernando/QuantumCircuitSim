import numpy as np
import matplotlib.pyplot as plt
import itertools

# Constant values for the matrices representing single qubit gates
identity = np.array([[1+0j,0+0j],[0+0j,1+0j]])
pauliX = np.array([[0+0j,1+0j],[1+0j,0+0j]])
pauliY = np.array([[0+0j,0-1j],[0+1j,0+0j]])
pauliZ = np.array([[1+0j,0+0j],[0+0j,-1+0j]])
hadamard = 1/np.sqrt(2) * np.array([[1+0j,1+0j],[1+0j,-1+0j]])

class Qubit:
    '''
    Class used to represent a Qubit

    Attributes
    ------------
    value: numpy array
        the value of the qubit. It is initialised to represent |0>
    '''
    def __init__(self):
        self.value = np.array([[1+0j],[0+0j]])

def possibleStates(numberOfQubits):
    '''
    Returns the possible binary states for a given number of qubits
    eg: for 2 qubits the possible states are |00>, |01>, |10>, |11>

    Parameters
    ------------
    numberOfQubits: int
        The number of qubits to calculate the possible states for
    '''
    states = [''.join(i) for i in itertools.product('01',repeat=numberOfQubits)]
    return states

def multiKroneckerProduct(*args):
    '''
    Returns the kronecker product of all the given arguments
    eg: arguments are [I,X,X,H,I] where I = identity, X = pauliX, H = hadamard
        returns I ⊗ X ⊗ X ⊗ H ⊗ I
    
    Parameters
    ------------
    *args: int, numpy array
    '''
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
    '''
    Returns the probability of the states
    
    Parameters
    ------------
    states: numpy array
        array of final states after applying all the gates
    '''
    for i in range(len(states)):
        states[i] = np.abs(states[i])**2
    return states

class QuantumCircuit:
    '''
    Class used to represent the quantum circuit

    Attributes
    ------------
    numberOfQubits: int
        The number of qubits in the quantum circuit
    qubits: list with elements of type Qubit
        Contains the values of the qubits
    columns: list 
        Elements are lists which represent the columns in quantum circuit
    columnCount: list of integers
        Shows the number of columns for each qubit which is used to determine
        which column to place gates in

    Methods
    ---------
    addColumn()
        Adds a new column to the quantum circuit
    x(qubitNumber)
        Apply the X gate
    y(qubitNumber)
        Apply the Y gate
    z(qubitNumber)
        Apply the Z gate
    h(qubitNumber)
        Apply the Hadamard gate
    cnot(control, qubitNumber)
        Apply the CNOT gate
    toffoli(controlA, controlB, qubitNumber)
        Apply the Toffoli gate 
    runCircuit()
        Run the circuit to get the state probability result and visualize
    visualize(possibilities, probabilities)
        Visualise the result using matplotlib
    '''
    def __init__(self,numberOfQubits):
        self.numberOfQubits = numberOfQubits
        self.qubits = [Qubit() for _ in range(numberOfQubits)]
        self.columns = [[identity for _ in range(self.numberOfQubits)]]
        self.columnCount = [0 for _ in range(numberOfQubits)]

    def addColumn(self):
        self.columns.append([identity for _ in range(self.numberOfQubits)])

    def x(self, qubitNumber):
        columnNumber = self.columnCount[qubitNumber]
        if columnNumber == 0:
            self.columns[columnNumber][qubitNumber] = pauliX
            self.columnCount[qubitNumber] += 1
        else:
            self.addColumn()
            self.columns[columnNumber][qubitNumber] = pauliX
            self.columnCount[qubitNumber] += 1
    
    def y(self, qubitNumber):
        columnNumber = self.columnCount[qubitNumber]
        if columnNumber == 0:
            self.columns[columnNumber][qubitNumber] = pauliY
            self.columnCount[qubitNumber] += 1
        else:
            self.addColumn()
            self.columns[columnNumber][qubitNumber] = pauliY
            self.columnCount[qubitNumber] += 1
    
    def z(self, qubitNumber):
        columnNumber = self.columnCount[qubitNumber]
        if columnNumber == 0:
            self.columns[columnNumber][qubitNumber] = pauliZ
            self.columnCount[qubitNumber] += 1
        else:
            self.addColumn()
            self.columns[columnNumber][qubitNumber] = pauliZ
            self.columnCount[qubitNumber] += 1

    def h(self, qubitNumber):
        columnNumber = self.columnCount[qubitNumber]
        if columnNumber == 0:
            self.columns[columnNumber][qubitNumber] = hadamard
            self.columnCount[qubitNumber] += 1
        else:
            self.addColumn()
            self.columns[columnNumber][qubitNumber] = hadamard
            self.columnCount[qubitNumber] += 1   

    def cnot(self, control, qubitNumber):
        p0 = np.array([[1,0],[0,0]])
        p1 = np.array([[0,0],[0,1]])
        a1 = [identity for _ in range(self.numberOfQubits)]
        a2 = [identity for _ in range(self.numberOfQubits)]
        a1[control] = p0
        a2[control] = p1
        a2[qubitNumber] = pauliX
        columnNumber = None
        cnot = multiKroneckerProduct(*a1) + multiKroneckerProduct(*a2)

        if self.columnCount[control] >= self.columnCount[qubitNumber]:
            columnNumber = self.columnCount[control]
            for i in range(self.numberOfQubits):
                if (control <= i <= qubitNumber) or (qubitNumber <= i <= control):
                    self.columnCount[i] = self.columnCount[control]

        if self.columnCount[qubitNumber] >= self.columnCount[control]:
            columnNumber = self.columnCount[qubitNumber]
            for i in range(self.numberOfQubits):
                if (control <= i <= qubitNumber) or (qubitNumber <= i <= control):
                    self.columnCount[i] = self.columnCount[qubitNumber]

        if columnNumber == 0:
            self.columns[columnNumber] = [1 for _ in range(self.numberOfQubits)]
            self.columns[columnNumber][qubitNumber] = cnot
            for i in range(self.numberOfQubits):
                if (control <= i <= qubitNumber) or (qubitNumber <= i <= control):
                    self.columnCount[i] += 1
        else:
            self.addColumn()
            self.columns[columnNumber] = [1 for _ in range(self.numberOfQubits)]
            self.columns[columnNumber][qubitNumber] = cnot
            for i in range(self.numberOfQubits):
                if (control <= i <= qubitNumber) or (qubitNumber <= i <= control):
                    self.columnCount[i] += 1

    def toffoli(self, controlA, controlB, qubitNumber):
        p0 = np.array([[1,0],[0,0]])
        p1 = np.array([[0,0],[0,1]])
        combinations = [[p0,p0],[p0,p1],[p1,p0],[p1,p1]]
        a = []
        for _ in range(4):
            a.append([identity for _ in range(self.numberOfQubits)])
        for i in range(len(a)):
            a[i][controlA] = combinations[i][0]
            a[i][controlB] = combinations[i][1]
            if(i == 3):
                a[i][qubitNumber] = pauliX
        toffoli = multiKroneckerProduct(*a[0]) + multiKroneckerProduct(*a[1]) + multiKroneckerProduct(*a[2]) + multiKroneckerProduct(*a[3])
        
        columnNumber = max(self.columnCount[controlA], self.columnCount[controlB], self.columnCount[qubitNumber])
        min_val = min(controlA, controlB, qubitNumber)
        max_val = max(controlA, controlB, qubitNumber)
        for i in range(self.numberOfQubits):
            if (min_val <= i <= max_val):
                self.columnCount[i] = columnNumber
        
        if columnNumber == 0:
            self.columns[columnNumber] = [1 for _ in range(self.numberOfQubits)]
            self.columns[columnNumber][qubitNumber] = toffoli
            for i in range(self.numberOfQubits):
                if (min_val <= i <= max_val):
                    self.columnCount[i] += 1
        else:
            self.addColumn()
            self.columns[columnNumber] = [1 for _ in range(self.numberOfQubits)]
            self.columns[columnNumber][qubitNumber] = toffoli
            for i in range(self.numberOfQubits):
                if (min_val <= i <= max_val):
                    self.columnCount[i] += 1

    def runCircuit(self):
        states = multiKroneckerProduct(*self.qubits)
        for i in range(len(self.columns)):
            states = np.dot(multiKroneckerProduct(*self.columns[i]),states)
        possibilities = possibleStates(self.numberOfQubits)
        prob = calcProbability(states).flatten()
        self.visualize(possibilities,prob.real)
    
    def visualize(self,possibilities,probalities):
        plt.title("Quantum Circuit Simulation")
        plt.bar(range(2**self.numberOfQubits),probalities)
        plt.xticks(range(2**self.numberOfQubits),possibilities)
        plt.ylim(-0,1)
        plt.grid(True)
        plt.ylabel(r'$P(|\psi\rangle)$')
        plt.xlabel(r'$|\psi\rangle$')
        plt.show()






