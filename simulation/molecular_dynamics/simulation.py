# pylint: disable=invalid-name
import itertools
import numpy as np
from numpy.random import default_rng

SEED = 1234
rng = default_rng(seed=SEED)


class Field:
    def __init__(self, num_rows: int, num_columns: int, cell_size: float) -> None:
        self.width = cell_size * num_columns
        self.height = cell_size * num_rows
        self.cell_ranges = (range(1, num_rows + 1), range(1, num_columns + 1))
        self._cells = self.init_cells(num_rows, num_columns)
        self._bins_x = np.linspace(0, self.width, num_columns + 1)
        self._bins_y = np.linspace(0, self.height, num_rows + 1)

    def clear_cells(self) -> None:
        """Make all cells empty."""
        for row in self._cells[1:-1]:
            for cell in row[1:-1]:
                cell.clear()

    def place_into_cells(self, positions: np.ndarray) -> None:
        """Populates the cells by putting the index of position into the respective bin."""
        indices_x = np.digitize(positions[:, 0], self._bins_x)
        indices_y = np.digitize(positions[:, 1], self._bins_y)
        for n in range(len(positions)):
            i = indices_y[n]
            j = indices_x[n]
            self._cells[i][j].append(n)

    def get_relevant_content(self, i: int, j: int) -> list[int]:
        """Gives the content of the next 5 cells which are right or below the specified indices."""
        if i < 1 or i > len(self._cells) - 2 or j < 1 or j > len(self._cells[1]) - 2:
            raise ValueError(f"The specified indices {i=}, {j=} are invalid.")
        else:
            relevant_cells = self._cells[i][j : j + 2] + self._cells[i + 1][j - 1 : j + 2]
            return list(itertools.chain(*relevant_cells))

    def get_cell(self, i: int, j: int) -> list[int]:
        """Gives the cell with the specified indices."""
        return self._cells[i][j]

    def correct_positions(self, positions: np.ndarray) -> None:
        for pos in positions:
            if pos[0] < 0 or pos[0] >= self.width:
                pos[0] = pos[0] % self.width
            if pos[1] < 0 or pos[1] >= self.height:
                pos[1] = pos[1] % self.height

    @staticmethod
    def init_cells(num_rows: int, num_columns: int) -> list[list[list[int]]]:
        """Init cells of the field as 2D list structure of lists.
        Border cells point to the opposite cell.

        Args:
            num_rows (int): number of rows
            num_columns (int): number of columns

        Returns:
            list[list[list[int]]]: 2D-Area with empty lists as cells
        """
        cells = []
        for i in range(num_rows + 2):
            row = []
            for j in range(num_columns + 2):
                cell = []  # type: list[int]
                row.append(cell)
            cells.append(row)
        # link border cells to opposite cells
        for i in range(num_rows + 2):
            if i == 0:
                map_i = num_rows
            elif i == num_rows + 1:
                map_i = 1
            else:
                map_i = i
            for j in range(num_columns + 2):
                if j == 0:
                    map_j = num_columns
                elif j == num_columns + 1:
                    map_j = 1
                else:
                    map_j = j

                cells[i][j] = cells[map_i][map_j]
        return cells


class Simulation:
    def __init__(
        self,
        num_molecules: int,
        num_rows: int,
        num_columns: int,
        cutting_radius: float,
        distribution: str,
        **init_kwargs,
    ) -> None:
        self._molecules = list(range(num_molecules))  # type: list[int]
        self._field = Field(num_rows, num_columns, cutting_radius)
        self._num_rows = num_rows
        self._num_columns = num_columns
        self.r_c = cutting_radius
        self._h = 0.001
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

    def _calc_velocities(self) -> None:
        self._velocities += self._h / 2 * self._accelerations

    def _calc_positions(self) -> None:
        self._positions += self._h * self._velocities + self._h ** 2 / 2 * self._accelerations
        self._field.correct_positions(self._positions)

    def _calc_forces(self) -> None:
        for i in self._field.cell_ranges[0]:
            for j in self._field.cell_ranges[1]:
                other_molecules = self._field.get_relevant_content(i, j)
                for u in self._field.get_cell(i, j):
                    for v in other_molecules:
                        if u != v:
                            self._calc_force(u, v)

    def _calc_force(self, u: int, v: int) -> None:
        r_uv = self._positions[v] - self._positions[u]
        r = np.linalg.norm(r_uv)
        if 0 < r <= self.r_c:
            force = 24 * (2 * r ** (-13) - r ** (-7)) * r_uv
            self._accelerations[u] += force
            self._accelerations[v] -= force

    def do_step(self) -> None:
        self._calc_positions()
        self._calc_velocities()
        self._accelerations = np.zeros_like(self._positions)
        self._field.clear_cells()
        self._field.place_into_cells(self._positions)
        self._calc_forces()
        self._calc_velocities()
