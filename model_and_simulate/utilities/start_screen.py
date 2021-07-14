"""Module for simulation menu class."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
import pygame

from .pygame_button import SwitchButton, TextButton, Button
from .pygame_simple import (
    SimplePygame,
    check_for_quit,
    check_for_reset,
    play_music_loop,
    get_window_resolution,
)
from .simulation import SimulationParameters



class SimulationStartScreen(ABC):
    """Abstract base class for pygame start screens for simulation visualizations."""

    music = "menu_light"  # type: str

    def __init__(self, simple_pygame: SimplePygame):
        self.simple_pygame = simple_pygame  # type: SimplePygame
        self.show_start = False  # type: bool
        self.read_input_to = None  # type: Optional[TextButton]
        self.buttons = None
        self.back_to_menu = False  # type: bool

    @abstractmethod
    def create_menu_items(self) -> tuple[int, int, SimulationParameters, list[Button]]:
        """Create all buttons and GUI items with logic."""
        pass

    @staticmethod
    @abstractmethod
    def create_menu_texts(col_w: int, row_h: int) -> list:
        """Create the raw texts for the start menu. This texts are just drawn, with no logic."""
        menu_texts = [
            ("Press ESC to quit or SPACE to reset simulation", (5, 5)),
        ]
        return menu_texts

    def show_start_screen(self) -> tuple[SimulationParameters, bool, bool, bool]:
        """Invokes menu creation and runs the pygame loop."""
        self.buttons, simulation_parameters = self.initialize_menu()
        running, reset, back_to_menu = True, False, False
        while (
            self.show_start and running and not self.back_to_menu
        ):  # show_start set by callback functions
            running, reset = self.do_start_screen_loop()
        self.simple_pygame.all_texts.clear()
        return simulation_parameters, running, reset, self.back_to_menu

    def initialize_menu(self) -> tuple[list[Button], SimulationParameters]:
        """Invoke buttons and texts creation."""
        self.show_start = True
        play_music_loop(SimulationStartScreen.music)
        SimulationStartScreen.music = "menu_dark"
        col_w, row_h, simulation_parameters, buttons = self.create_menu_items()
        menu_texts = self.create_menu_texts(col_w, row_h)
        for text, args in menu_texts:
            self.simple_pygame.add_text(text, *args)
        return buttons, simulation_parameters

    def do_start_screen_loop(self) -> tuple[bool, bool]:
        """Checks all user input events in this loop."""
        running, reset = True, False
        read_input_mode = False if self.read_input_to is None else True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(event.pos)
            elif read_input_mode:
                text_input_button = self.read_input_to  # type: TextButton
                if event.type == pygame.TEXTINPUT:
                    try:
                        number = int(event.text)
                    except ValueError:
                        number = None
                    if number is not None:
                        text_input_button.append_text(str(number))
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        text_input_button.finish_input()
                    elif event.key == pygame.K_BACKSPACE:
                        text_input_button.backspace()
            if check_for_quit(event):
                running = False
            elif check_for_reset(event):
                running = False
                reset = True
        self.simple_pygame.loop(mouse_pos=pygame.mouse.get_pos())
        return running, reset

    def create_default_items(self, col_w: int, row_h: int):
        """Gets all sprites list and creates a start and a back button."""
        menu_items = self.simple_pygame.all_sprites
        width, height = get_window_resolution()

        def on_click_listener_start(*args):
            """The callback function for start button."""
            self.show_start = False

        def on_click_listener_back(*args):
            """The callback function for back button."""
            self.back_to_menu = True

        default_buttons = [
            SwitchButton((col_w * 2, row_h), (width - 2 * col_w, row_h), text="Start"),
            SwitchButton((col_w * 2, row_h), (0, height - row_h), text="Back"),
        ]
        self.add_switch_buttons(default_buttons[:1], menu_items, on_click_listener_start)
        self.add_switch_buttons(default_buttons[1:], menu_items, on_click_listener_back)
        return menu_items, default_buttons

    @staticmethod
    def disable_other_buttons(clicked_button: SwitchButton, buttons: list[SwitchButton]):
        """Disable all the other buttons in the button list."""
        for other_button in buttons:
            if other_button != clicked_button:
                other_button.on = False
            else:
                # keep button active
                if not clicked_button.on:
                    clicked_button.on = True

    @staticmethod
    def default_button_on(buttons: dict, default):
        """Activate one button with default value."""
        for button, value in buttons.items():
            if value == default:
                button.on = True
                return

    @staticmethod
    def add_switch_buttons(buttons, menu_items: pygame.sprite.Group, on_click_listener: callable):
        """Add on click callback function and buttons."""
        for button in buttons:
            button.add_on_click_listener(on_click_listener)
            menu_items.add(button)
