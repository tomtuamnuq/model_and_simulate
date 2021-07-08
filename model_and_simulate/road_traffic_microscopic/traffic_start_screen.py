"""Module for the traffic simulation menu."""
import pygame

from model_and_simulate.utilities.pygame_button import Button
from model_and_simulate.utilities.start_screen import StartScreen
from .traffic_simulation import TrafficParameters


class TrafficStartScreen(StartScreen):
    """The start screen for TrafficSimulation`."""

    def create_menu_items(self) -> tuple[int, int, TrafficParameters, list[Button]]:
        """Creates the GUI buttons with `TrafficParameters` logic."""
        simulation_parameters = TrafficParameters()

        width, height = pygame.display.get_window_size()
        col_w, row_h = round(width / 8), round(height / 8)
        menu_items, buttons = self.create_default_items(col_w, row_h)
        return col_w, row_h, simulation_parameters, buttons

    @staticmethod
    def create_menu_texts(col_w: int, row_h: int) -> list:
        """Gets the raw texts for the start menu. This texts are just drawn, with no logic."""
        menu_texts = []
        return menu_texts
