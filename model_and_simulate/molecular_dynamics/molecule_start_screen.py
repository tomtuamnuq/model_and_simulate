"""Module for the molecule simulation menu."""
import pygame

from .molecule_simulation import distributions, MoleculeParameters
from model_and_simulate.utilities.pygame_button import SwitchButton, TextButton, Button
from model_and_simulate.utilities.pygame_simple import Color
from model_and_simulate.utilities.start_screen import StartScreen


class MoleculeStartScreen(StartScreen):
    """The start screen for `MoleculeSimulation`."""

    def create_menu_items(self) -> tuple[int, int, MoleculeParameters, list[Button]]:
        """Creates the GUI buttons with MoleculeParameter logic."""

        simulation_parameters = MoleculeParameters()
        width, height = pygame.display.get_window_size()
        col_w, row_h = round(width / 8), round(height / 8)
        menu_items, buttons = self.create_default_items(col_w, row_h)
        buttons_h: dict[SwitchButton, float] = {
            SwitchButton(
                (col_w, row_h),
                (x * col_w, row_h),
                text=str(v),
                in_and_active_color=(Color.HGREEN, Color.SILVER),
            ): v
            for x, v in zip((1, 2, 3), (0.1, 0.01, 0.001))
        }
        self.default_button_on(buttons_h, simulation_parameters.time_step)

        def on_click_listener_h(clicked_button: SwitchButton):
            """The callback function for step size buttons."""
            simulation_parameters.time_step = buttons_h[clicked_button]
            self.simple_pygame.play_effect("hit_low")
            self.disable_other_buttons(clicked_button, list(buttons_h.keys()))

        self.add_switch_buttons(buttons_h.keys(), menu_items, on_click_listener_h)
        buttons_distributions: dict[SwitchButton, str] = {
            SwitchButton(
                (col_w, row_h),
                (x * col_w, y * row_h),
                text=v,
                in_and_active_color=(Color.RED, Color.SILVER),
            ): v
            for x, y, v in zip((0, 1, 0, 1, 0, 1), (4, 4, 5, 5, 6, 6), distributions.keys())
        }
        self.default_button_on(buttons_distributions, simulation_parameters.distribution)

        def on_click_listener_distribution(clicked_button: SwitchButton):
            """The callback function for distribution buttons."""
            simulation_parameters.distribution = buttons_distributions[clicked_button]
            self.simple_pygame.play_effect("hit_low")
            self.disable_other_buttons(clicked_button, list(buttons_distributions.keys()))

        self.add_switch_buttons(
            buttons_distributions.keys(), menu_items, on_click_listener_distribution
        )

        buttons_text_input: dict[TextButton, str] = {
            TextButton(
                (col_w * 2, row_h),
                (5 * col_w, y * row_h),
                str(getattr(simulation_parameters, attr)),
            ): attr
            for y, attr in zip(
                range(3, 7),
                ("num_rows", "num_columns", "num_molecules", "sigma"),
            )
        }
        init_vel = simulation_parameters.init_vel_range[1]
        buttons_text_input[
            TextButton((col_w * 2, row_h), (5 * col_w, 7 * row_h), text=str(init_vel))
        ] = "init_vel_range"

        def on_start_input_listener(text_button: TextButton):
            """The callback function for start input event."""
            if self.read_input_to is not None:
                self.read_input_to.finish_input()
            self.read_input_to = text_button

        def on_finish_input_listener(text_button: TextButton):
            """The callback function for finish input."""
            simulation_par = buttons_text_input[text_button]
            old_value = getattr(simulation_parameters, simulation_par)
            if simulation_par == "init_vel_range":
                if text_button.text == "":
                    text_button.text = str(old_value[1])
                else:
                    user_value = int(text_button.text)
                    value = (min(-user_value, user_value), max(-user_value, user_value))
                    setattr(simulation_parameters, simulation_par, value)
            else:
                if text_button.text == "" or int(text_button.text) == 0:
                    text_button.text = str(old_value)
                else:
                    setattr(simulation_parameters, simulation_par, int(text_button.text))

            self.read_input_to = None

        on_hover_text = "Click and use BACKSPACE or ENTER"

        def on_hover_text_listener(*args):
            """The callback function for hovering text input buttons."""
            self.simple_pygame.draw_text(on_hover_text, (4 * col_w, 2.5 * row_h))

        for button in buttons_text_input.keys():
            button.add_on_start_listener(on_start_input_listener)
            button.add_on_finish_listener(on_finish_input_listener)
            button.add_on_hover_listener(on_hover_text_listener)
            menu_items.add(button)
        buttons += (
            list(buttons_h.keys())
            + list(buttons_distributions.keys())
            + list(buttons_text_input.keys())
        )
        return col_w, row_h, simulation_parameters, buttons

    @staticmethod
    def create_menu_texts(col_w: int, row_h: int) -> list:
        """Gets the raw texts for the start menu. This texts are just drawn, with no logic."""
        bigger_text = 25
        menu_texts = [
            ("step size dt", (0, row_h, 20, Color.HGREEN)),
            ("position distribution", (0, 3.5 * row_h, bigger_text, Color.RED)),
            ("Press ESC to quit or SPACE to reset simulation", (5, 5)),
        ]
        y = 3
        for text, limit in zip(
            ("Rows", "Columns", "Num Molecules", "Sigma", "Init velocity"), (99, 99, 999, 9, 99)
        ):
            menu_texts.append((text, (4 * col_w, y * row_h + row_h / 2)))
            menu_texts.append(("<= " + str(limit), (7 * col_w, y * row_h + row_h / 2)))
            y += 1
        return menu_texts
