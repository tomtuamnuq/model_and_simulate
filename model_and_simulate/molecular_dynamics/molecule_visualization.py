"""Module with class to start the visualization and simulation of the `MoleculeSimulation`."""
import dataclasses
from model_and_simulate.utilities.pygame_simple import play_music_loop
from model_and_simulate.utilities.simulation import (
    SimulationVisualization,
    Simulation,
    SimulationParameters,
)
from .molecule_simulation import MoleculeSimulation
from .molecule_sprite import Molecule
from .molecule_start_screen import MoleculeStartScreen


class MoleculeVisualization(SimulationVisualization):
    """A visualization of `MoleculeSimulation` in pygame."""

    def update_visualization(self) -> None:
        """Nothing to do."""
        pass

    def initialize_simulation(self) -> Simulation:
        """Creates the molecule simulation object."""
        return MoleculeSimulation(*dataclasses.astuple(self.simulation_parameters))

    def initialize_visualization(self) -> None:
        """Sets the pygame visualization up."""
        music = "sim_bass" if self.simulation_parameters.time_step < 0.01 else "sim_psy"
        play_music_loop(music)
        molecule_sprites = self.simple_pygame.all_sprites
        for molecule in self.simulation.molecules:
            pos = self.simulation.positions[molecule]
            molecule_sprites.add(Molecule(self.coord_mapper, self.simulation_parameters.sigma, pos))

    def show_start_screen(self) -> tuple[SimulationParameters, bool, bool]:
        """Calls the implementation of molecule start screen."""
        molecule_start_screen = MoleculeStartScreen(self.simple_pygame)
        return molecule_start_screen.show_start_screen()
