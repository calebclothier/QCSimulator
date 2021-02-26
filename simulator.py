import numpy as np 
import collections
from mathparser import VariableMathStringParser
from gates import gate_set


class QuantumSimulator():

	def get_ground_state(self, num_qubits):
		""" Returns vector of size 2**num_qubits with all zeroes except first element which is 1 (big endian) """
		state = np.zeros(2**num_qubits, dtype=np.complex64)
		state[0] = 1
		return state

	def get_operator(self, total_qubits, gate_unitary, target_qubits):
		""" Returns unitary operator of size 2**n x 2**n for given gate (in array form) and target qubits """
		
		if len(target_qubits) == 2:
			# Constructs 2-qubit controlled operators (e.g., CNOT) with arbitrarily separated control and target qubits
			op1 = 1
			op2 = 1
			P0x0 = np.array([[1, 0],[0, 0]])
			P1x1 = np.array([[0, 0],[0, 1]])
			for i in range(total_qubits):
				if i in target_qubits:
					if i == target_qubits[0]:
						op1 = np.kron(op1, P0x0)
						op2 = np.kron(op2, P1x1)
					else:
						op1 = np.kron(op1, np.identity(2, dtype=np.complex64))
						op2 = np.kron(op2, gate_unitary)
				else:
					op1 = np.kron(op1, np.identity(2, dtype=np.complex64))
					op2 = np.kron(op2, np.identity(2, dtype=np.complex64))
			return op1 + op2

		else:
			# Constructs arbitrary 1-qubit operators
			op = 1
			for i in range(total_qubits):
				# Kronecker product together all the individual gates
				if i in target_qubits:
					# If target qubit, use the specified unitary gate in Kronecker product
					op = np.kron(op, gate_unitary)
				else:
					# Otherwise use identity gate in Kronecker product
					op = np.kron(op, np.identity(2, dtype=np.complex64))
			return op

	def run_program(self, initial_state, program):
		""" Reads program, and for each gate:
		     - calculates matrix operator
		     - multiplies state with operator
		    Returns final state """
		total_qubits = int(np.log2(len(initial_state)))
		state = initial_state
		for inst in program:
			if "gate" in inst:
				# Use built-in gates if specified
				op = self.get_operator(total_qubits, gate_set[inst["gate"]], inst["target"])
				state = np.dot(state, op)
			else:
				# Otherwise use the unitary matrix that is given 
				if "params" in inst:
					gate = self.gate_parser(inst["unitary"], inst["params"])
					op = self.get_operator(total_qubits, gate, inst["target"])
					state = np.dot(state, op)
				else:
					op = self.get_operator(total_qubits, inst["unitary"], inst["target"])
					state = np.dot(state, op)
		return state

	def measure_all(self, state_vector):
		""" Chooses element from state_vector by sampling uniformly from [0,1],
		    dividing [0,1] into segments of length probability(x) for all possible measurement outcomes x,
		    and returning the index of the outcome whose line segment contains the random sample """

		probs = []
		# Sample randomly from interval [0, 1]
		random = np.random.uniform()
		for i in range(len(state_vector)):
			# Calculate probability amplitudes for all measurement outcomes
			probs.append(state_vector[i].real**2 + state_vector[i].imag**2)
			if i > 0:
				# Add probabilities to get cumulative distribution
				probs[i] += probs[i-1]
			if random < probs[i]:
				# Return the index range in the CDF that contains the random sample
				return i

	def get_counts(self, state_vector, num_shots):
		""" Executes measure_all in a loop num_shots times and
		    returns object with statistics in following form:
		      {
		         element_index: number_of_ocurrences,
		         element_index: number_of_ocurrences,
		         element_index: number_of_ocurrences,
		         ...
		      }
		    (only for elements which occurred - returned from measure_all) """

		total_qubits = int(np.log2(len(state_vector)))
		results = collections.defaultdict(int)

		for i in range(num_shots):
			outcome = np.binary_repr(self.measure_all(state_vector), width=total_qubits) # big endian binary rep of measurement outcome
			results[str(outcome)] += 1
		return dict(results)

	def gate_parser(self, gate_unitary, var_dict):
		parsed_gate = np.zeros((len(gate_unitary), len(gate_unitary[0])), dtype=np.complex64)
		parser = VariableMathStringParser()
		for i in range(len(gate_unitary)):
			for j in range(len(gate_unitary[0])):
				expr =  parser.eval(gate_unitary[i][j], var_dict)
				parsed_gate[i,j] = expr
		return parsed_gate


sim = QuantumSimulator()
program = [{ "gate": "h", "target": [0] }, 
  		   { "gate": "x", "target": [0, 1]},
		   {"unitary": [["cos(theta/2)", "-exp(i * lambda) * sin(theta / 2)"],
						["exp(i * phi) * sin(theta / 2)", "exp(i * lambda + i * phi) * cos(theta / 2)"]], 
			"params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, 
			"target": [1]}
]
state = sim.get_ground_state(6)
final_state = sim.run_program(state, program)
sample = sim.measure_all(final_state)
print(sim.get_counts(final_state, 10000))

