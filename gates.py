import numpy as np

gate_set = {
	"h": np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)],
	               [1 / np.sqrt(2), -1 / np.sqrt(2)]], dtype=np.complex64),
	"x": np.array([[0, 1],
	               [1, 0]], dtype=np.complex64),
	"y": np.array([[0, -1j],
	               [1j, 0]], dtype=np.complex64),
	"z": np.array([[1, 0], 
	               [0, -1]], dtype=np.complex64),
	"u3": [["cos(theta/2)", "-exp(i * lambda) * sin(theta / 2)"],
		   ["exp(i * phi) * sin(theta / 2)", "exp(i * lambda + i * phi) * cos(theta / 2)"]],  # params: theta, lambda, phi
	"phase": [[1, 0],
              [0, "exp(i * theta)"]], # params: theta
	
	# Controlled X, Y, Z gates are identical to X, Y, Z, gates 
	# because the controlled application of a gate is computed by get_operator()
	"cx": np.array([[0, 1],
	               [1, 0]], dtype=np.complex64),
	"cy": np.array([[0, -1j],
	               [1j, 0]], dtype=np.complex64),
	"cz": np.array([[1, 0], 
	               [0, -1]], dtype=np.complex64)
}