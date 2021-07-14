"""Module for the traffic simulation menu."""
import pygame

from model_and_simulate.utilities.pygame_simple import Color
from model_and_simulate.utilities.pygame_button import SwitchButton, TextButton, Button
from model_and_simulate.utilities.start_screen import SimulationStartScreen
from .traffic_simulation import TrafficParameters


class TrafficStartScreen(SimulationStartScreen):
    """The start screen for TrafficSimulation`."""

    def create_menu_items(self) -> tuple[int, int, TrafficParameters, list[Button]]:
        """Creates the GUI buttons with `TrafficParameters` logic."""
        simulation_parameters = TrafficParameters()

        width, height = pygame.display.get_window_size()
        col_w, row_h = round(width / 8), round(height / 8)
        menu_items, buttons = self.create_default_items(col_w, row_h)
        button_all_at_once = SwitchButton(
            (col_w, row_h),
            (col_w, 4 * row_h),
            text="All at once",
            in_and_active_color=(Color.RED, Color.SILVER),
        )
        button_all_at_once.on = simulation_parameters.all_vehicles_at_once

        def on_click_listener_all_at_once(*args):
            """The callback function for the switch button."""
            simulation_parameters.all_vehicles_at_once = (
                not simulation_parameters.all_vehicles_at_once
            )
            self.simple_pygame.play_effect("hit_low")

        self.add_switch_buttons([button_all_at_once], menu_items, on_click_listener_all_at_once)
        buttons.append(button_all_at_once)
        buttons_text_input: dict[TextButton, str] = {
            TextButton(
                (col_w * 2, row_h),
                (5 * col_w, y * row_h),
                str(getattr(simulation_parameters, attr) * 100)[:2],
            ): attr
            for y, attr in zip(
                range(3, 5),
                ("occupation", "dawdling_factor"),
            )
        }
        button_length = TextButton(
            (col_w * 2, row_h),
            (6 * col_w, 5 * row_h),
            str(simulation_parameters.length),
            text_color=Color.GREEN,
        )
        buttons_text_input[button_length] = "length"

        def on_start_input_listener(text_button: TextButton):
            """The callback function for start input event."""
            if self.read_input_to is not None:
                self.read_input_to.finish_input()
            self.read_input_to = text_button

        def on_finish_input_listener(text_button: TextButton):
            """The callback function for finish input."""
            simulation_par = buttons_text_input[text_button]
            old_value = getattr(simulation_parameters, simulation_par)
            if text_button.text == "":
                if simulation_par == "length":
                    text_button.text = str(old_value)
                else:
                    text_button.text = str(old_value*100)[:2]
            else:
                user_value = int(text_button.text)
                if simulation_par == "length":
                    if user_value < 300:
                        user_value = 300
                    elif user_value > 3500:
                        user_value = 3500
                    setattr(simulation_parameters, simulation_par, user_value)
                else:
                    if simulation_par == "occupation":
                        user_value = max(user_value, 10)
                    setattr(simulation_parameters, simulation_par, user_value / 100)  # percentage
                text_button.text = str(user_value)

            self.read_input_to = None

        on_hover_text = "Click and use Digits, BACKSPACE or ENTER"

        def on_hover_text_listener(*args):
            """The callback function for hovering text input buttons."""
            self.simple_pygame.draw_text(on_hover_text, (4 * col_w, 2.5 * row_h))

        for button in buttons_text_input.keys():
            button.add_on_start_listener(on_start_input_listener)
            button.add_on_finish_listener(on_finish_input_listener)
            button.add_on_hover_listener(on_hover_text_listener)
            menu_items.add(button)
        buttons += list(buttons_text_input.keys())
        return col_w, row_h, simulation_parameters, buttons

    @staticmethod
    def create_menu_texts(col_w: int, row_h: int) -> list:
        """Gets the raw texts for the start menu. This texts are just drawn, with no logic."""
        menu_texts = SimulationStartScreen.create_menu_texts(col_w, row_h)
        y = 3
        for text, limit in zip(("total density", "dawdling probability"), (10, 0)):
            menu_texts.append((text, (3.4 * col_w, y * row_h + row_h / 2)))
            menu_texts.append((f">= {limit:0>2d} %", (7 * col_w, y * row_h + row_h / 2)))
            y += 1
        menu_texts += [
            ("increment density one by one", (0, 3.5 * row_h, 25, Color.RED)),
            (f"{300} <= length <= {3500}", (4 * col_w, y * row_h + row_h / 2, 20, Color.HGREEN)),
        ]
        return menu_texts
