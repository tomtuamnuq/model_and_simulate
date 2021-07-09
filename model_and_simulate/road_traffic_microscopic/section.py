"""Module for classes `Section` and `Cell`."""
from __future__ import annotations
import math


class Section:
    """Describes a road section with cells of equal size placed at equal intervals."""

    def __init__(self, length: float, velocity_max: int, density_max: float):
        self._length = length
        self._velocity_max = velocity_max
        self._density_max = density_max
        self._cells = self._init_cells()

    def _init_cells(self) -> list[Cell]:
        number_of_cells = int(math.ceil(self._density_max * self._length))
        cell_size = self._length / number_of_cells
        cells = [Cell(i, cell_size) for i in range(number_of_cells)]
        return cells

    @property
    def cells(self) -> list[Cell]:
        """The list of equidistant cells all of same size with ascending numbering."""
        return self._cells

    @property
    def length(self) -> float:
        """The total length."""
        return self._length

    @property
    def max_cell_number(self) -> int:
        """The number of the last cell in this road section."""
        return len(self._cells) - 1

    def get_cell(self, number: int) -> Cell:
        """Returns the cell with position `number` mod `self.max_cell_number`+1 in `self.cells`."""
        if number > self.max_cell_number:
            number = number % (self.max_cell_number + 1)
        return self._cells[number]


class Cell:
    """A line item."""

    def __init__(self, number: int, size: float):
        self._number = number
        self._size = size
        self._empty = True  # type: bool

    @property
    def size(self) -> float:
        """The length of this cell."""
        return self._size

    @property
    def number(self) -> int:
        """The number of this line item."""
        return self._number

    @property
    def position(self) -> float:
        """The position of this line item."""
        return self._size * self._number

    def is_empty(self) -> bool:
        """Returns true if this cell is free."""
        return self._empty

    def make_empty(self) -> None:
        """Makes the cell free."""
        self._empty = True

    def make_occupied(self) -> None:
        """Places something on this cell."""
        self._empty = False
