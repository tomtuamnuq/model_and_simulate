"""Contains Aizawa equations and parameters."""
import numpy as np

# parameters for aizawa equations

a = 0.95
b = 0.7
c = 0.6
d = 3.5
e = 0.25
f = 0.1


def aizawa_differential_equation(t, x: np.ndarray) -> np.ndarray:
    """Implements the coupled nonlinear systems of equations.
    Parameter t is not used but necessary for `scipy.integrate.solve_ivp`."""
    dx = x[0] * (x[2] - b) - d * x[1]
    dy = d * x[0] + x[1] * (x[2] - b)
    dz = (
        c
        + a * x[2]
        - (x[2] ** 3) / 3
        - x[0] ** 2
        + (1 + e * x[2]) * x[1] ** 2
        + f * x[2] * x[0] ** 3
    )
    return np.asarray([dx, dy, dz])
