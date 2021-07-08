"""Module for classes `Section` and `Cell`."""
from __future__ import annotations
import numpy as np


class Section:
    def __init__(self, length: float, velocity_max: int, density_max: float):
        self._length = length
        self._velocity_max = velocity_max
        self._density_max = density_max
        self._cells = self._init_cells()

    def _init_cells(self) -> list[Cell]:
        number_of_cells = np.ceil(self._density_max * self._length)
        cell_size = self._length / number_of_cells
        cells = [Cell(i, cell_size) for i in range(number_of_cells)]
        return cells, cell_size

    @property
    def cells(self) -> list[Cell]:
        return self._cells

    @property
    def length(self) -> float:
        return self._length

    @property
    def max_cell_number(self) -> int:
        return len(self._cells) - 1

    def get_cell(self, number: int) -> Cell:
        """Returns the cell with `number`."""
        if number > self.max_cell_number:
            number = number % self.max_cell_number
        return self._cells[number]


class Cell:
    def __init__(self, number: int, size: float):
        self._number = number
        self._size = size
        self._empty = True  # type: bool

    @property
    def size(self) -> float:
        return self._size

    @property
    def number(self) -> int:
        return self._number

    @property
    def position(self) -> float:
        return self._size * self._number

    def is_empty(self) -> bool:
        return self._empty

    def make_empty(self) -> None:
        self._empty = True

    def make_occupied(self) -> None:
        self._empty = False
