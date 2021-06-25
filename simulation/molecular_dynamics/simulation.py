# pylint: disable=invalid-name
import numpy as np


class Field:
    def __init__(self, num_rows: int, num_columns: int, cell_size: float) -> None:
        self._width = cell_size * num_columns
        self._height = cell_size * num_rows
        self._cells = self.init_cells(num_rows, num_columns)
        self._bins_x = np.linspace(0, self._width, num_columns + 1)
        self._bins_y = np.linspace(0, self._height, num_rows + 1)

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

    def get_relevant_cells(self, i: int, j: int) -> list[list[int]]:
        """Gives the 5 cells which are right below the specified indices."""
        if i < 1 or i > len(self._cells) - 2 or j < 1 or j > len(self._cells[1]) - 2:
            raise ValueError(f"The specified indices {i=}, {j=} are invalid.")

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
                cell = [(i, j)]  # type: list[int] # TODO remove i,j
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
        self, num_molecules: int, num_rows: int, num_columns: int, cutting_radius: float
    ) -> None:
        self._molecules = list(range(num_molecules))  # type: list[int]
        self._field = Field(num_rows, num_columns, cutting_radius)
        self.r_c = cutting_radius
