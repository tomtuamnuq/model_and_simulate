"""Module with class to start the visualization and simulation of the `TrafficSimulation`."""
import dataclasses

from model_and_simulate.utilities.pygame_simple import play_music_loop, get_window_resolution
from model_and_simulate.utilities.simulation import (
    SimulationVisualization,
    Simulation,
    SimulationParameters,
)
from .traffic_simulation import TrafficSimulation
from .traffic_start_screen import TrafficStartScreen
from .section_sprite import SectionSprite


class TrafficVisualization(SimulationVisualization):
    """A visualization of `TrafficSimulation` in pygame."""

    section_height = 8  # number of pixels per Section on y-Axis

    def __init__(self, title: str):
        super(TrafficVisualization, self).__init__(title)
        self._section_height = TrafficVisualization.section_height
        self._section_pos_y_max = get_window_resolution()[1] - 3 * self._section_height
        self._section_pos_y = self._init_section_pos_y()
        self._dynamic_section_sprite = None

    def _init_section_pos_y(self) -> int:
        return 4 * self._section_height

    def initialize_simulation(self) -> Simulation:
        """Creates the traffic simulation object."""
        return TrafficSimulation(*dataclasses.astuple(self.simulation_parameters))

    def initialize_visualization(self) -> None:
        """Sets the pygame visualization up."""
        music = "sim_bass" if self.simulation_parameters.dawdling_factor < 0.3 else "sim_psy"
        play_music_loop(music)
        self.simple_pygame.frames_per_second = 5

        self._dynamic_section_sprite = SectionSprite(
            self.coord_mapper, self.simulation.section, 0, 3 * self._section_height
        )
        self.simple_pygame.all_sprites.add(self._dynamic_section_sprite)
        self.simple_pygame.add_text("Number of vehicles", 0, self._section_pos_y_max - 10, 10)
        self.simple_pygame.add_text(
            "0",
            0,
            self._section_pos_y_max + self._section_height - 10,
        )

    def update_visualization(self) -> None:
        """TODO add docs."""
        if self._section_pos_y > self._section_pos_y_max:
            self._section_pos_y = self._init_section_pos_y()
            self.simple_pygame.all_sprites.empty()
            self.simple_pygame.all_sprites.add(self._dynamic_section_sprite)
        section_sprite = SectionSprite(
            self.coord_mapper,
            self.simulation.section,
            self._section_pos_y,
            self._section_height,
            one_time_drawing=True,
        )
        self.simple_pygame.all_sprites.add(section_sprite)
        self._section_pos_y += self._section_height
        self.simple_pygame.set_text(1, str(self.simulation.number_of_vehicles))

    def show_start_screen(self) -> tuple[SimulationParameters, bool, bool]:
        """Calls the implementation of the traffic start screen."""
        traffic_start_screen = TrafficStartScreen(self.simple_pygame)
        return traffic_start_screen.show_start_screen()
