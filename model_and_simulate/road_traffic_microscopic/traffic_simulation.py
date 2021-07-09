"""Module with microscopic traffic simulation class and additional features."""
from dataclasses import dataclass
from typing import Tuple
import random
import math
from .section import Section
from .vehicle import Vehicle
from model_and_simulate.utilities.simulation import Simulation, SimulationParameters


class TrafficSimulation(Simulation):
    """Class for the actual simulation of vehicles on a road."""

    density_max: float = 1 / 7.5  # vehicles per meter
    velocity_max: int = 5  # maximum number of cells to move

    def __init__(
        self, length: float, occupation: float, dawdling_factor: float, all_vehicles_at_once: bool
    ):
        self._section = Section(
            length, TrafficSimulation.velocity_max, TrafficSimulation.density_max
        )
        self._dawdling_factor = dawdling_factor
        self._vehicles, self._number_of_vehicles = self._init_vehicles(
            all_vehicles_at_once, occupation
        )
        self._all_vehicles_set = self._check_if_all_vehicles_set()

    @property
    def dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        length = round(self._section.length)
        cell_size = round(self._section.get_cell(0).size)
        return (0, length), (0, cell_size)

    def _check_if_all_vehicles_set(self):
        return self._number_of_vehicles == len(self._vehicles)

    def _init_vehicles(
        self, all_vehicles_at_once: bool, occupation: float
    ) -> tuple[list[Vehicle], int]:
        number_of_vehicles = int(math.floor(occupation * self._section.max_cell_number))
        if all_vehicles_at_once:
            vehicles = self._place_all_vehicles(number_of_vehicles)
        else:
            vehicles = [
                Vehicle(i, self.velocity_max, self.velocity_max, self._dawdling_factor)
                for i in range(number_of_vehicles)
            ]
            number_of_vehicles = 0
            # TODO place vehicles step by step every few iterations...
        return vehicles, number_of_vehicles

    def _place_all_vehicles(self, number_of_vehicles: int) -> list[Vehicle]:
        vehicles = []
        cell_sample = random.sample(self._section.cells, number_of_vehicles)
        cell_sample = sorted(cell_sample, key=lambda elem: elem.number, reverse=True)
        successor = None
        for cell, ident in zip(cell_sample, range(number_of_vehicles - 1, -1, -1)):
            init_velocity = random.randint(0, self.velocity_max)
            vehicle = Vehicle(ident, init_velocity, self.velocity_max, self._dawdling_factor)
            vehicle.place_into_cell(cell)
            vehicle.successor = successor
            successor = vehicle
            vehicles.insert(0, vehicle)
        # set the car on the left as successor of the car on the right
        rightmost_vehicle = vehicles[-1]
        rightmost_vehicle.successor = vehicles[0]
        return vehicles

    def do_step(self) -> None:
        if not self._all_vehicles_set:
            # set another vehicle on the road
            self._all_vehicles_set = self._check_if_all_vehicles_set()
        print("##################################################")
        cell_string = ""
        cell_string_empty = ""
        for cell in self._section.cells:
            cell_string += str(cell.number) + " "
            if not cell.is_empty():
                cell_string_empty += str(cell.number) + " "
        print(cell_string)
        print(cell_string_empty)
        vehicle_string = ""
        for vehicle in self._vehicles:
            vehicle_string += str(vehicle.velocity) + " "
        print(vehicle_string)

        for vehicle in self._vehicles:
            vehicle.update_velocity(self._section.max_cell_number)
        for vehicle in self._vehicles:
            vehicle.move(self._section)



    @property
    def number_of_vehicles(self) -> int:
        """The current number of vehicles placed on `self._section`."""
        return self._number_of_vehicles

    @property
    def vehicles(self) -> list[Vehicle]:
        """The currently set vehicles."""
        return self._vehicles[: self.number_of_vehicles]

    @property
    def section(self) -> Section:
        return self._section


@dataclass
class TrafficParameters(SimulationParameters):
    """Class for keeping track of the simulation parameters in menus."""

    length: float = 2250 # 2250 default 3500 max 100 min
    occupation: float = 0.5 # 0.2 default 1 max 0.1 min
    dawdling_factor: float = 0.2 # 0.2 default 1 max and 0.1 min
    all_vehicles_at_once: bool = True # True default
