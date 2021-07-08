"""Module with simulation interfaces for use with pygame."""
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple
import pygame
from model_and_simulate.utilities.coordinate_mapper import CoordinateMapper2D
from model_and_simulate.utilities.pygame_simple import (
    SimplePygame,
    check_for_quit,
    check_for_reset,
)


class Simulation(ABC):
    @property
    @abstractmethod
    def dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Coordinate ranges of simulated 2D area."""

    @abstractmethod
    def do_step(self) -> None:
        """Perform one step of the simulation logic."""


class SimulationVisualization(ABC):
    def __init__(self, title: str):
        self.simple_pygame = SimplePygame(title)
        self.simulation = None
        self.simulation_parameters = None
        self.coord_mapper = None

    @abstractmethod
    def initialize_simulation(self, simulation_parameters: SimulationParameters) -> Simulation:
        pass

    @abstractmethod
    def initialize_visualization(self) -> None:
        pass

    @abstractmethod
    def show_start_screen(self) -> tuple[bool, bool]:
        pass

    def main(self) -> bool:
        """Performs the simulation and returns reset signal."""
        running, reset = self.show_start_screen()
        if running:
            self.initialize()
        while running:
            running, reset = self.do_simulation_loop()
        return reset

    def initialize(self) -> None:
        """Init the simulation and pygame visualization."""
        self.simulation = self.initialize_simulation(self.simulation_parameters)
        width, height = pygame.display.get_window_size()
        display_dim = ((0, width), (0, height))
        self.coord_mapper = CoordinateMapper2D(*self.simulation.dim, *display_dim)
        self.simple_pygame.all_sprites.empty()
        self.initialize_visualization()

    def do_simulation_loop(self) -> tuple[bool, bool]:
        """Performs one loop of event checking, simulation calculation, and pygame drawing."""
        running, reset = True, False
        for event in pygame.event.get():
            if check_for_quit(event):
                running = False
            elif check_for_reset(event):
                running = False
                reset = True
        self.simulation.do_step()
        self.simple_pygame.loop()
        return running, reset


@dataclass
class SimulationParameters(ABC):
    pass
