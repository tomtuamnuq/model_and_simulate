"""Module with molecule simulation class and additional features."""
from dataclasses import dataclass
from typing import Tuple
import numpy as np
from numpy.random import default_rng
from .field import Field
from ..utilities.coordinate_mapper import CoordinateMapper2D

# SEED = 1234
rng = default_rng()  # keyword seed=SEED

distributions = {
    "uniform": rng.uniform,
    "cauchy_center": rng.standard_cauchy,
    "exponential_zero": rng.exponential,
    "gumbel": rng.gumbel,
    "normal_zero": rng.normal,
    "normal_center": rng.normal,
    # "logistic_center": rng.logistic,
    # "exponential_center": rng.exponential,
}  # type str[callable]


class MoleculeSimulation:
    """Class for the actual simulation of molecules."""

    cut_off_factor = 4

    def __init__(
        self,
        num_molecules: int,
        num_rows: int,
        num_columns: int,
        sigma: int,
        distribution: str,
        h: float,
        init_vel_range: Tuple[float, float],
    ) -> None:
        """
        Args:
            num_molecules (int): Number of molecules
            num_rows (int): Number of rows for field.
            num_columns (int): Number of columns for field.
            sigma (int): Radius of molecules.
            distribution (str): Distribution to draw positions initially from.
            h (float): Step size parameter delta_t.
            init_vel_range (Tuple[float, float]): Uniform distribution params
             to draw velocities initially from.
        """
        self._molecules = list(range(num_molecules))
        self._sigma = sigma
        self.r_c = MoleculeSimulation.cut_off_factor * sigma
        self._field = Field(num_rows, num_columns, self.r_c)
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._h = h
        rng_gen = distributions[distribution]
        centralize = "center" in distribution
        self._positions = self._init_positions(rng_gen, centralize)
        velocities_x = rng.uniform(
            low=init_vel_range[0], high=init_vel_range[1], size=num_molecules
        )
        velocities_y = rng.uniform(
            low=init_vel_range[0], high=init_vel_range[1], size=num_molecules
        )
        self._velocities = np.column_stack((velocities_x, velocities_y))
        self._accelerations = np.zeros_like(self._velocities)

    def _init_positions(self, rng_gen: callable, centralize: bool) -> np.ndarray:
        positions_x = rng_gen(size=len(self._molecules))
        positions_y = rng_gen(size=len(self._molecules))
        pos_range_x = min(positions_x), max(positions_x)
        pos_range_y = min(positions_y), max(positions_y)
        coord_mapper = CoordinateMapper2D(pos_range_x, pos_range_y, *self.dim)
        positions = np.column_stack((positions_x, positions_y))
        center = np.asarray([self._field.width / 2, self._field.height / 2])
        for m in self._molecules:
            positions[m] = coord_mapper.map_coordinates(positions[m])
            if centralize:
                positions[m] += center
        return positions

    @property
    def dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Coordinate ranges of simulated field."""
        return (0, self._field.width), (0, self._field.height)

    @property
    def molecules(self) -> list[int]:
        """List of molecules."""
        return self._molecules

    @property
    def positions(self) -> np.ndarray:
        """Numpy array with x-y-positions."""
        return self._positions

    @property
    def velocities(self) -> np.ndarray:
        """Numpy array with x-y-velocities."""
        return self._velocities

    def _calc_velocities(self) -> None:
        self._velocities += self._h / 2 * self._accelerations

    def _calc_positions(self) -> None:
        self._positions += self._h * self._velocities + self._h ** 2 / 2 * self._accelerations
        self._field.correct_positions(self._positions)

    def _calc_forces(self) -> None:
        for i in self._field.cell_ranges[0]:
            for j in self._field.cell_ranges[1]:
                current_cell = self._field.get_cell(i, j)
                other_cells, displacements = self._field.get_relevant_cells(i, j)
                for u in current_cell:
                    for cell, displacement in zip(other_cells, displacements):
                        if displacement is None:
                            for v in cell:
                                self._calc_force(u, v, self._positions[v])
                        else:
                            for v in cell:
                                pos_v = self._positions[v] + displacement
                                self._calc_force(u, v, pos_v)

    def _calc_force(self, u: int, v: int, pos_v: np.ndarray) -> None:
        r_uv = pos_v - self._positions[u]
        r = max(np.linalg.norm(r_uv), self._sigma)
        if r <= self.r_c:
            force = 24 * (2 * r ** (-13) - r ** (-7)) * r_uv
            self._accelerations[u] += force
            self._accelerations[v] -= force

    def do_step(self) -> None:
        """Perform one step of the simulation."""
        self._calc_positions()
        self._calc_velocities()
        self._accelerations = np.zeros_like(self._positions)
        self._field.clear_cells()
        self._field.place_into_cells(self._positions)
        self._calc_forces()
        self._calc_velocities()


@dataclass
class SimulationParameters:
    """Class for keeping track of the simulation parameters in menus."""

    num_molecules: int = 500
    num_rows: int = 15
    num_columns: int = 15
    sigma: int = 1
    distribution: str = "uniform"
    time_step: float = 0.01
    init_vel_range: tuple[int, int] = -10, 10
