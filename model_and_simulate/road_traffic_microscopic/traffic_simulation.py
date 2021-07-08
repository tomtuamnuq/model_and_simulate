"""Module with microscopic traffic simulation class and additional features."""
from dataclasses import dataclass
from typing import Tuple
import numpy as np
from .section import Section
from .vehicle import Vehicle


class TrafficSimulation:
    """Class for the actual simulation of vehicles on a road."""

    density_max: float = 1 / 7.5  # vehicles per meter
    velocity_max: int = 5  # maximum number of cells to move

    def __init__(
        self, length: float, occupation: float, dawdling_factor: float, all_vehicles_at_once: bool
    ):
        self._section = Section(
            length, TrafficSimulation.velocity_max, TrafficSimulation.density_max
        )
        self._vehicles = []  # type: list[Vehicle]
        self._dawdling_factor = dawdling_factor

        number_of_vehicles = np.floor(occupation * self._section.max_cell_number)
        if all_vehicles_at_once:
            self._all_vehicles_set = True
            for i in range(number_of_vehicles):
                # create Vehicles with random pos and vel
                pass
        else:
            self._all_vehicles_set = False

    @property
    def number_of_vehicles(self) -> int:
        return len(self._vehicles)

    @property
    def vehicles(self) -> list[Vehicle]:
        return self._vehicles


@dataclass
class SimulationParameters:
    """Class for keeping track of the simulation parameters in menus."""

    length: float = 2250
    occupation: float = 0.3
    dawdling_factor: float = 0.2
    all_vehicles_at_once: bool = True
