"""Module with `Vehicle` class."""
from __future__ import annotations
from typing import Optional
from numpy.random import default_rng
from .section import Cell, Section

SEED = 1234
rng = default_rng(seed=SEED)  # keyword seed=SEED


class Vehicle:
    """This describes a stochastic cellular automata."""
    def __init__(
        self,
        ident: int,
        cell: Cell,
        position_max: int,
        velocity: int,
        velocity_max: int,
        dawdling_factor: float,
    ):
        self._ident = ident
        self._cell = cell
        self._position_max = position_max
        self._velocity = velocity
        self._successor = None  # type: Optional[Vehicle]
        self._dawdling_factor = dawdling_factor
        self._velocity_max = velocity_max

    @property
    def successor(self) -> Optional[Vehicle]:
        """The vehicle on the right side of this vehicle."""
        return self._successor

    @successor.setter
    def successor(self, successor: Vehicle) -> None:
        """Setter of successor."""
        self._successor = successor

    @property
    def ident(self) -> int:
        """The identification number."""
        return self._ident

    @property
    def position(self) -> int:
        """The current cell number in units of cells."""
        return self._cell.number

    @property
    def velocity(self) -> int:
        """The current velocity."""
        return self._velocity

    @velocity.setter
    def velocity(self, vel: int) -> None:
        """The current velocity."""
        self._velocity = vel

    def distance_to_successor(self, right_border: int) -> int:
        """Get the distance to the cell of the vehicle on the right side."""
        distance = 0 if self._successor is None else self.successor.position - self.position - 1
        if distance < 0:
            distance = right_border + distance
        return distance

    def _accelerate(self) -> None:
        self.velocity = min(self.velocity + 1, self._velocity_max)

    def _brake(self, distance: int) -> None:

        if self.velocity > distance:
            self.velocity = distance

    def _is_dawdling(self) -> bool:
        return rng.binomial(1, self._dawdling_factor) == 1

    def _dawdle(self) -> None:
        self.velocity = max(self.velocity - 1, 0)

    def update_velocity(self, right_border: int) -> None:
        """Perform rules of NaSch-Model to calculate velocity."""
        self._accelerate()
        distance = self.distance_to_successor(right_border)
        self._brake(distance)
        if self._is_dawdling():
            self._dawdle()

    def move(self, section: Section) -> None:
        """Empty the current cell and move to the next cell."""
        if self.velocity > 0:
            self._cell.make_empty()
            self._cell = section.get_cell(self.position + self.velocity)
            self._cell.place_vehicle()
