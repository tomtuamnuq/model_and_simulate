"""Module with function to set parameters and run the molecule simulation."""
import dataclasses

import pygame
from .molecule_simulation import MoleculeSimulation, SimulationParameters
from .molecule_sprite import Molecule
from model_and_simulate.utilities.coordinate_mapper import CoordinateMapper2D
from model_and_simulate.utilities.pygame_simple import (
    SimplePygame,
    check_for_quit,
    check_for_reset,
    play_music_loop,
)
from .molecule_start_screen import show_start_screen


def molecule_main() -> bool:
    """Performs the simulation and returns reset signal."""
    simple_pygame = SimplePygame("Molecule Simulation")

    simulation_parameters, running, reset = show_start_screen(simple_pygame)
    if running:
        simulation = initialize(simple_pygame, simulation_parameters)
    else:
        simulation = None
    while running:
        running, reset = do_simulation_loop(simple_pygame, simulation)
    return reset


def initialize(simple_pygame: SimplePygame, simulation_parameters: SimulationParameters):
    """Setup the simulation and pygame visualization."""
    music = "sim_bass" if simulation_parameters.time_step < 0.01 else "sim_psy"
    play_music_loop(music)
    simulation = MoleculeSimulation(*dataclasses.astuple(simulation_parameters))
    width, height = pygame.display.get_window_size()
    display_dim = ((0, width), (0, height))
    coord_mapper = CoordinateMapper2D(*simulation.dim, *display_dim)
    molecule_sprites = simple_pygame.all_sprites
    molecule_sprites.empty()
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        molecule_sprites.add(Molecule(coord_mapper, simulation_parameters.sigma, pos))
    return simulation


def do_simulation_loop(simple_pygame, simulation) -> tuple[bool, bool]:
    """Performs one loop of event checking, simulation calculation, and pygame drawing."""
    running, reset = True, False
    for event in pygame.event.get():
        if check_for_quit(event):
            running = False
        elif check_for_reset(event):
            running = False
            reset = True
    simulation.do_step()
    simple_pygame.loop()
    return running, reset
