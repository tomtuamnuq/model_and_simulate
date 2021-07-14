"""Module with simple start screen for this repository."""
from itertools import chain
from typing import Optional
from functools import partial
import pygame

from utilities.pygame_button import SwitchButton
from utilities.pygame_simple import SimplePygame, check_for_quit, get_window_resolution
from utilities.start_screen import StartScreen

import chaos.chaos_main as chaos_sim
import model_and_simulate.molecular_dynamics.molecule_visualization as molecular_sim
import road_traffic_microscopic.traffic_visualization as traffic_sim

pygame_simulations = {
    "Molecule Sim": molecular_sim.MoleculeVisualization,
    "Traffic Road": traffic_sim.TrafficVisualization,
}

matplotlib_simulations = {
    "Lorenz Chaotic": partial(chaos_sim.chaos_main, "lorenz", "k"),
    "Aizawa Chaotic": partial(chaos_sim.chaos_main, "aizawa", "c"),
}


class BaseStartScreen(StartScreen):
    """Start menu to select simulations."""

    def __init__(self):
        self.simple_pygame = SimplePygame("Model and Simulate")
        self.buttons = None  # type: Optional[list[SwitchButton]]
        self.selection = None  # type: Optional[str]

    def create_menu_items(self) -> list[SwitchButton]:
        """Create one button per simulation."""
        menu_items = self.simple_pygame.all_sprites
        width, height = get_window_resolution()
        col_w = round(width / max(len(pygame_simulations), len(matplotlib_simulations)))
        row_h = round(height / 2)
        buttons_simulations: dict[SwitchButton, str] = {
            SwitchButton(
                (col_w, row_h),
                (x * col_w, y * row_h),
                text=v,
            ): v
            for x, y, v in zip(
                chain(range(len(pygame_simulations)), range(len(matplotlib_simulations))),
                [0] * len(pygame_simulations) + [1] * len(matplotlib_simulations),
                list(pygame_simulations.keys()) + list(matplotlib_simulations.keys()),
            )
        }

        def on_click_listener_simulations(clicked_button: SwitchButton):
            """The callback function for distribution buttons."""
            self.selection = buttons_simulations[clicked_button]
            self.simple_pygame.play_effect("hit_low")

        self.add_switch_buttons(
            buttons_simulations.keys(), menu_items, on_click_listener_simulations
        )
        return list(buttons_simulations.keys())

    def show_start_screen(self) -> tuple[Optional[str], bool]:
        """Invokes menu creation and runs the pygame loop."""
        self.buttons = self.create_menu_items()
        running = True
        while running and self.selection is None:
            running = self.do_start_screen_loop()
        return self.selection, running

    def do_start_screen_loop(self) -> bool:
        """Checks all user input events in this loop."""
        running = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(event.pos)
            if check_for_quit(event):
                running = False
        self.simple_pygame.loop(mouse_pos=pygame.mouse.get_pos())
        return running

    @staticmethod
    def create_menu_texts(col_w: int, row_h: int) -> list:
        """No texts to draw."""
        pass
