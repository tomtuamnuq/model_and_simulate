"""Module for class `Field`."""
from typing import Optional

import numpy as np


class Field:
    """A 2-D area of cells to use as simulation field."""

    def __init__(self, num_rows: int, num_columns: int, cell_size: int) -> None:
        """
        Create a field with `num_rows` * `num_columns` fields of size `cell_size`.
        Args:
            num_rows (int):
            num_columns (int):
            cell_size (int):
        """
        self.width = cell_size * num_columns
        self.height = cell_size * num_rows
        self.cell_ranges = (range(1, num_rows + 1), range(1, num_columns + 1))
        self._cells = self.init_cells(num_rows, num_columns)
        self._displacements = self._init_displacements(num_rows, num_columns)
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

    def get_relevant_cells(
        self, i: int, j: int
    ) -> tuple[list[list[int]], list[Optional[np.ndarray]]]:
        """Gives the 4 cells which are right or below the specified cell and the cell itself.
        The Tuple contains the cells and optional displacement vectors for border cells."""
        if i < 1 or i > len(self._cells) - 2 or j < 1 or j > len(self._cells[1]) - 2:
            raise ValueError(f"The specified indices {i=}, {j=} are invalid.")  # TODO remove
        else:
            relevant_cells = self._cells[i][j : j + 2] + self._cells[i + 1][j - 1 : j + 2]
            displacements = (
                self._displacements[i][j : j + 2] + self._displacements[i + 1][j - 1 : j + 2]
            )
            return relevant_cells, displacements

    def get_cell(self, i: int, j: int) -> list[int]:
        """Gives the cell with the specified indices."""
        return self._cells[i][j]

    def correct_positions(self, positions: np.ndarray) -> None:
        """Move objects outside the field to the opposite position inside the field."""
        for pos in positions:
            if pos[0] < 0 or pos[0] >= self.width:
                pos[0] = pos[0] % self.width
            if pos[1] < 0 or pos[1] >= self.height:
                pos[1] = pos[1] % self.height

    def _init_displacements(
        self, num_rows: int, num_columns: int
    ) -> list[list[Optional[np.ndarray]]]:
        """Init displacement structure of the field as 2D list structure of lists.
        Border cells contain a displacement vector and other cells None.

        Args:
            num_rows (int): number of rows
            num_columns (int): number of columns

        Returns:
            list[list[list[int]]]: 2D-Area with empty lists as cells
        """
        displ = []
        for i in range(num_rows + 2):
            row = []
            if i == 0:
                d_y = -self.height
            elif i == num_rows + 1:
                d_y = self.height
            else:
                d_y = 0
            for j in range(num_columns + 2):
                if j == 0:
                    d_x = -self.width
                elif j == num_columns + 1:
                    d_x = self.width
                else:
                    d_x = 0
                d = None  # type: Optional[np.ndarray]
                if d_x != 0 or d_y != 0:
                    d = np.asarray([d_x, d_y])

                row.append(d)
            displ.append(row)

        return displ

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
