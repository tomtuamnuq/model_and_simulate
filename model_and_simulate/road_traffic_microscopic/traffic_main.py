"""Module with function to set parameters and run the molecule simulation."""
from .traffic_simulation import TrafficSimulation, SimulationParameters
from .traffic_start_screen import show_start_screen
from model_and_simulate.utilities.coordinate_mapper import CoordinateMapper2D
from model_and_simulate.utilities.pygame_simple import (
    SimplePygame,
    check_for_quit,
    check_for_reset,
    play_music_loop,
)

def traffic_main() -> bool:
    """Performs the simulation and returns reset signal."""
    simple_pygame = SimplePygame("Traffic Simulation")
    simulation_parameters, running, reset = show_start_screen(simple_pygame)
    if running:
        simulation = initialize(simple_pygame, simulation_parameters)
    else:
        simulation = None
    return False # TODO check for reset

def initialize(simple_pygame: SimplePygame, simulation_parameters: SimulationParameters):
    """Setup the simulation and pygame visualization."""
    music = "sim_bass" if simulation_parameters.dawdling_factor < 0.4 else "sim_psy"
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