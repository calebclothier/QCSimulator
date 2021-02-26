import numpy as np

gate_set = {

	# Basic gates
	"h": np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)],
	               [1 / np.sqrt(2), -1 / np.sqrt(2)]], dtype=np.complex64),
	"x": np.array([[0, 1],
	               [1, 0]], dtype=np.complex64),
	"y": np.array([[0, -1j],
	               [1j, 0]], dtype=np.complex64),
	"z": np.array([[1, 0], 
	               [0, -1]], dtype=np.complex64),

	# Parametrized gates
	"rx": [["cos(theta / 2)", "-i * sin(theta / 2)"],
		   ["-i * sin(theta / 2)", "cos(theta / 2)"]], # Required params: theta
	"ry": [["cos(theta / 2)", "-sin(theta / 2)"],
		   ["sin(theta / 2)", "cos(theta / 2)"]], # Required params: theta
	"rz": [["exp(-i * theta / 2)", "0"],
		   ["0", "exp(i * theta / 2)"]], # Required params: theta
	"phase": [["1", "0"],
              ["0", "exp(i * theta)"]], # Required params: theta
	
	# Controlled X, Y, Z gates are identical to X, Y, Z, gates 
	# because the controlled application of a gate is computed by get_operator()
	"cx": np.array([[0, 1],
	               [1, 0]], dtype=np.complex64),
	"cy": np.array([[0, -1j],
	               [1j, 0]], dtype=np.complex64),
	"cz": np.array([[1, 0], 
	               [0, -1]], dtype=np.complex64)

}