"""Module with chaos simulation class."""

from typing import Optional, Callable
import numpy as np
from numpy.random import default_rng
from scipy.integrate import solve_ivp

# SEED = 1234
rng = default_rng()  # keyword seed=SEED


class ChaosSimulation:
    """Class for the actual simulation of a chaotic system."""

    ode_method = "RK23"  # use Runge-Kutta procedure to solve differential equations

    def __init__(
        self,
        equation: Callable[[float, np.ndarray], np.ndarray],
        time_step: int = 30,
        dimensions: int = 0,
        start_point: Optional[np.ndarray] = None,
    ):
        """
        Simulates a chaotic system of ordinary differential equations.
            dimensions or start_point must be set. If start_point is given, dimension is
            calculated. Otherwise start_point is chosen randomly.
        Args:
            equation (function): The system of odes.
            time_step (int): Step to perform per iteration.
            dimensions (int): Number of dimensions for data points.
            start_point (Union[None, None]): An initial data point.
        """
        self._equation = equation
        self._time_step = time_step
        if start_point is None:
            if dimensions == 0:
                raise ValueError("An initial point or the dimensions must be set!")
            else:
                start_point = rng.random(size=dimensions)
        self._start_point = start_point
        self._dimension = len(self._start_point)
        assert self._dimension == len(equation(0, self._start_point))  # sanity check

    def run_into_chaos(self, num_initial_steps: int = 100) -> tuple[Optional[np.ndarray], int]:
        """
        Performs `num_initial_steps` of solving the system of differential equations.
        Args:
            num_initial_steps (int): Number of iterations.

        Returns:
            Tuple[numpy.ndarray, int]: The last solution of the odes and the end-time.
        """
        interim_point = self._start_point
        time_span = (0, self._time_step)
        for n in range(num_initial_steps):
            ode_solution, success = self._solve_ode(interim_point, time_span)
            if not success:
                return None, time_span[1]
            else:
                interim_point = ode_solution.T[-1]
                time_span = self._next_time_span(time_span)
        return interim_point, time_span[1]

    def get_chaotic_data(
        self, num_steps: int = 50, chaotic_point: np.ndarray = None, time_start: int = 0
    ) -> Optional[np.ndarray]:
        """
        Performs `num_steps` of simulating the system of odes and collects the data points.
            The number of data points depends on `ChaosSimulation.ode_method` and is not `num_steps`
        Args:
            num_steps (int): Number of iterations.
            chaotic_point (numpy.ndarray): An initial data point. If not given it is calculated.
            time_start (int): The end-time of the last iterations.

        Returns:
            numpy.ndarray: Array of chaotic data points.
        """
        if chaotic_point is None:
            chaotic_point, time_start = self.run_into_chaos()
        if chaotic_point is None:
            return None
        else:
            interim_point = chaotic_point
            time_span = (time_start, time_start + self._time_step)
            data = chaotic_point.reshape((*chaotic_point.shape, 1))
            for n in range(num_steps):
                ode_solution, success = self._solve_ode(interim_point, time_span)
                if success is None:
                    return None
                else:
                    data = np.concatenate((data, ode_solution), axis=1)
                    interim_point = ode_solution.T[-1]
                    time_span = self._next_time_span(time_span)
            return data

    def _next_time_span(self, time_span: tuple[int, int]) -> tuple[int, int]:
        return time_span[1], time_span[1] + self._time_step

    def _solve_ode(
        self, start_point: np.ndarray, time_span: tuple[int, int]
    ) -> tuple[np.ndarray, bool]:
        result = solve_ivp(
            self._equation, time_span, start_point, method=ChaosSimulation.ode_method
        )
        return result.y, result.success
