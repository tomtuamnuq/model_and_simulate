"""Module for the traffic simulation menu."""
from typing import Optional, TypedDict
import pygame

from .traffic_simulation import SimulationParameters
from model_and_simulate.utilities.pygame_button import SwitchButton, TextButton, Button
from model_and_simulate.utilities.pygame_simple import (
    SimplePygame,
    Color,
    check_for_quit,
    check_for_reset,
    play_music_loop,
)


class StartMenuStatus(TypedDict):
    """Typing class to check menu status variables."""

    show_start: bool
    read_input_to: Optional[TextButton]
    music: str


start_menu_status: StartMenuStatus = {
    "show_start": False,
    "read_input_to": None,
    "music": "menu_light",
}


def show_start_screen(simple_pygame: SimplePygame) -> tuple[SimulationParameters, bool, bool]:
    """Invokes menu creation and runs the pygame loop."""
    buttons, simulation_parameters = initialize_menu(simple_pygame)
    running, reset = True, False
    # TODO create menu
    # while start_menu_status["show_start"] and running:  # show_start set by callback functions
    #     running, reset = do_start_screen_loop(buttons, simple_pygame)
    # simple_pygame.all_texts.clear()
    return simulation_parameters, running, reset


def initialize_menu(simple_pygame: SimplePygame):
    """Invoke buttons and texts creation."""
    start_menu_status["show_start"] = True
    play_music_loop(start_menu_status["music"])
    start_menu_status["music"] = "menu_dark"
    col_w, row_h, simulation_parameters, buttons = _create_menu_items(simple_pygame)
    # menu_texts = _create_menu_texts(col_w, row_h)
    # for text, args in menu_texts:
    #     simple_pygame.add_text(text, *args)
    return buttons, simulation_parameters


def _create_menu_items(
    simple_pygame: SimplePygame,
) -> tuple[int, int, SimulationParameters, list[Button]]:

    simulation_parameters = SimulationParameters()
    menu_items = simple_pygame.all_sprites
    width, height = pygame.display.get_window_size()
    col_w, row_h = round(width / 8), round(height / 8)
    buttons = []  # TODO create Buttons
    return col_w, row_h, simulation_parameters, buttons
