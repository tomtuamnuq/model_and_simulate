from typing import Tuple

import numpy as np
from numpy.random import default_rng
from .field import Field

SEED = 1234
rng = default_rng(seed=SEED)


class Simulation:
    cut_off_factor = 4

    def __init__(
        self,
        num_molecules: int,
        num_rows: int,
        num_columns: int,
        sigma: int,
        distribution: str,
        h: float = 0.01,
        **init_kwargs,
    ) -> None:
        self._molecules = list(range(num_molecules))
        self._sigma = sigma
        self.r_c = Simulation.cut_off_factor * sigma
        self._field = Field(num_rows, num_columns, self.r_c)
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._h = h
        if distribution == "uniform":
            rng_gen = rng.uniform
            positions_x = rng_gen(low=0, high=self._field.width, size=num_molecules)
            positions_y = rng_gen(low=0, high=self._field.height, size=num_molecules)
            velocities_x = rng_gen(low=-0.1, high=0.1, size=num_molecules)
            velocities_y = rng_gen(low=-0.1, high=0.1, size=num_molecules)

        elif distribution == "exponential":
            rng_gen = rng.exponential
        elif distribution == "normal":
            rng_gen = rng.normal
        else:
            raise ValueError(f"{distribution=} is not supported!")
        self._positions = np.column_stack((positions_x, positions_y))
        self._velocities = np.column_stack((velocities_x, velocities_y))
        self._accelerations = np.zeros_like(self._positions)

    @property
    def dim(self) -> Tuple[int, int]:
        return self._field.width, self._field.height

    @property
    def molecules(self) -> list[int]:
        return self._molecules

    @property
    def positions(self) -> np.ndarray:
        return self._positions

    @property
    def velocities(self) -> np.ndarray:
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
                    for cell, displ in zip(other_cells, displacements):
                        if displ is None:
                            for v in cell:
                                self._calc_force(u, v, self._positions[v])
                        else:
                            for v in cell:
                                pos_v = self._positions[v] + displ
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
