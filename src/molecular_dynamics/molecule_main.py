import dataclasses
from dataclasses import dataclass
import pygame
from .molecule_simulation import MoleculeSimulation
from .visualization import Molecule
from src.utilities.coordinate_mapper import CoordinateMapper2D
from src.utilities.pygame_utils import SimplePygame


@dataclass
class SimulationParameters:
    """Class for keeping track of the simulation parameters in menu."""

    num_molecules: int = 500
    num_rows: int = 15
    num_columns: int = 15
    sigma: float = 1
    distribution: str = "gumbel"
    time_step: float = 0.01
    init_vel_range: tuple[int, int] = -10, 10


def molecule_main():
    simple_pygame = SimplePygame("Molecule Simulation")
    simulation_parameters = show_start_screen(simple_pygame)
    simulation = MoleculeSimulation(*dataclasses.astuple(simulation_parameters))
    width, height = pygame.display.get_window_size()
    display_dim = ((0, width), (0, height))
    coord_mapper = CoordinateMapper2D(*simulation.dim, *display_dim)
    molecule_sprites = simple_pygame.all_sprites
    molecule_sprites.empty()
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        vel = simulation.velocities[molecule]
        molecule_sprites.add(Molecule(coord_mapper, simulation_parameters.sigma, pos, vel))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    simple_pygame.play_effect("hit_low")
        simulation.do_step()
        simple_pygame.loop()

    simple_pygame.quit()


def show_start_screen(simple_pygame: SimplePygame) -> SimulationParameters:
    simple_pygame.play_music_loop("menu_dark")
    simulation_parameters = SimulationParameters()

    return simulation_parameters
