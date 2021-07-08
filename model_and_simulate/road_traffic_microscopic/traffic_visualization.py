"""Module with class to start the visualization and simulation of the `TrafficSimulation`."""
import dataclasses
from model_and_simulate.utilities.pygame_simple import (
    play_music_loop,
)
from model_and_simulate.utilities.simulation import (
    SimulationVisualization,
    Simulation,
    SimulationParameters,
)
from .traffic_simulation import TrafficSimulation
from .traffic_start_screen import TrafficStartScreen


class TrafficVisualization(SimulationVisualization):
    """A visualization of `TrafficSimulation` in pygame."""

    def initialize_simulation(self) -> Simulation:
        """Creates the traffic simulation object."""
        return TrafficSimulation(*dataclasses.astuple(self.simulation_parameters))

    def initialize_visualization(self) -> None:
        """Sets the pygame visualization up."""
        music = "sim_bass" if self.simulation_parameters.dawdling_factor < 0.3 else "sim_psy"
        play_music_loop(music)
        vehicle_sprites = self.simple_pygame.all_sprites

    def show_start_screen(self) -> tuple[SimulationParameters, bool, bool]:
        """Calls the implementation of traffic start screen."""
        traffic_start_screen = TrafficStartScreen(self.simple_pygame)
        return traffic_start_screen.show_start_screen()
