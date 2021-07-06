"""Contains lorenz equations and parameters."""
import numpy as np

# parameters for lorenz equations
sigma = 10
B = 8 / 3
R = 28


def lorenz_differential_equation(t, x: np.ndarray) -> np.ndarray:
    """Implements the coupled nonlinear systems of equations.
        Parameter t is not used but necessary for `scipy.integrate.solve_ivp`."""
    dx = -sigma * x[0] + sigma * x[1]
    dy = R * x[0] - x[1] - x[0] * x[2]
    dz = -B * x[2] + x[0] * x[1]
    return np.asarray([dx, dy, dz])
