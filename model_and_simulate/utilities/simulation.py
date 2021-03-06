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
    get_window_resolution,
)


class Simulation(ABC):
    """Abstract base class for doing a simulation on a 2D area."""

    @property
    @abstractmethod
    def dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Coordinate ranges of simulated 2D area."""

    @abstractmethod
    def do_step(self) -> None:
        """Perform one step of the simulation logic."""


class SimulationVisualization(ABC):
    """Abstract base class to visualize a `Simulation` with pygame."""

    def __init__(self, title: str):
        self.simple_pygame = SimplePygame(title)
        self.simulation = None
        self.simulation_parameters = None
        self.coord_mapper = None

    @abstractmethod
    def initialize_simulation(self) -> Simulation:
        """Creates the simulation object and sets it up."""
        pass

    @abstractmethod
    def initialize_visualization(self) -> None:
        """Sets the pygame visualization up."""
        pass

    @abstractmethod
    def update_visualization(self) -> None:
        """Update the pygame visualization stuff."""
        pass

    @abstractmethod
    def show_start_screen(self) -> tuple[SimulationParameters, bool, bool, bool]:
        """Displays the start screen and collects the simulation parameters
        as well as quit, reset, and back_to_start control signals."""
        pass

    def main(self) -> tuple[bool, bool]:
        """Performs the simulation and returns reset and go back to start signals."""
        self.simulation_parameters, running, reset, back_to_main_menu = self.show_start_screen()
        if back_to_main_menu:
            return reset, True
        if running:
            self.initialize()
        while running:
            running, reset = self.do_simulation_loop()
        return reset, False

    def initialize(self) -> None:
        """Init the simulation and pygame visualization."""
        self.simulation = self.initialize_simulation()
        width, height = get_window_resolution()
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
        self.update_visualization()
        self.simple_pygame.loop()
        return running, reset


@dataclass
class SimulationParameters(ABC):
    """Abstract base class to use for simulation parameter setting in menus."""

    pass
