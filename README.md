# QCSimulator
This project is a basic implementation of a quantum circuit simulator. The main file, simulator.py, contains a simulator class. Sample usage of this class is provided below. A dictionary of built-in gates is stored in gates.py, and parsing functionality for parametrized gates is contained in mathparser.py. 
``` 
# Initialize simulator object
sim = QuantumSimulator()
# Define the program by specifying a sequence of gates and target qubits.
program = [{ "gate": "h", "target": [0] }, 
           { "gate": "x", "target": [0, 1]},
           {"unitary": [["cos(theta/2)", "-exp(i * lambda) * sin(theta / 2)"],
			["exp(i * phi) * sin(theta / 2)", "exp(i * lambda + i * phi) * cos(theta / 2)"]], 
            "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, 
            "target": [1]}]
# Create ground state of 6-qubit quantum computer
state = sim.get_ground_state(6)
# Execute the program
final_state = sim.run_program(state, program)
# Measure the final state 10000 times and output statistics
print(sim.get_counts(final_state, 10000)) 
```

## Documentation

### Gates
The simulator can handle arbitrary 1-qubit gates and 2-qubit controlled gates (e.g., CNOT). Single qubit gates are applied to the qubit at the single specified target index, while 2-qubit controlled gates are applied to the qubit at the 2nd target index, conditioned on the qubit at the 1st target index. Gates may be specified in a variety of ways.
#### Arbitrary unitary gates:
``` 
{"unitary": [[a,b],[c,d]], "target":[x]}   # Single qubit U gate
{"unitary": [[a,b],[c,d]], "target":[x,y]}  # Controlled-U gate
{"unitary": [["cos(theta)", "-sin(theta)"],["sin(theta)", "cos(theta)"]], "params": {"theta": 1.57}, "target": [x]}   # Parametrized gate (all entries, even numerical ones, must be strings)
```
#### Built-in gates:
Currently available built-in gates are: 
- h (Hadamard)
- x, y, z (Pauli X, Y, Z, gates)
- cx, cy, cz (controlled Pauli gates, note that they are identical to the x, y, z, gates because get_operator() handles controlled gate application)
- rx, ry, rz (rotation by angle theta around the x, y, and z axes, respectively)
- phase (phase shift by angle theta)
```
{"gate": 'h', "target":[x]}   # Hadamard gate
{"gate": 'cx', "target":[x,y]}    # CNOT with control qubit x, target qubit y
{"gate": 'x', "target":[x,y]}     # Also CNOT – same as above because get_operator() treats single qubit gate with two target qubits as controlled gate
{"gate": 'rx', "params": {"theta": 1.57}, "target": [x]}    # Built-in parametrized gates
```
#### Global params for variational algorithms
Parameters can be set to a global value for variational algorithms by passing a dictionary of global variable names and their corresponding values as the last argument of run_program(), and defining the gate parameter to be the name of the global variable.
```
program = [{"gate": 'rx', "params": {"theta": 'global_1'}, "target": [x]}]
final_state = run_program(state, program, {"global_1": 0.5})
```
