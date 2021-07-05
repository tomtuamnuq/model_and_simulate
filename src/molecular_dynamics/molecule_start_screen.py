from typing import Optional, TypedDict

import pygame

from src.molecular_dynamics.molecule_main import SimulationParameters
from src.main import do_reset
from src.molecular_dynamics.molecule_simulation import distributions
from src.utilities.pygame_button import SwitchButton, TextButton, Button
from src.utilities.pygame_simple import (
    SimplePygame,
    Color,
    check_for_continue,
    check_for_reset,
    play_music_loop,
    quit_pygame,
)


class StartMenuStatus(TypedDict):
    show_start: bool
    read_input_to: Optional[TextButton]


start_menu_status: StartMenuStatus = {"show_start": False, "read_input_to": None}


def show_start_screen(simple_pygame: SimplePygame) -> SimulationParameters:
    start_menu_status["show_start"] = True
    play_music_loop("menu_dark")
    col_w, row_h, simulation_parameters, buttons = add_menu_items(simple_pygame)
    menu_texts = create_menu_texts(col_w, row_h)
    for text, args in menu_texts:
        simple_pygame.add_text(text, *args)

    while start_menu_status["show_start"]:
        read_input_mode = True if start_menu_status["read_input_to"] else False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(event.pos)
            elif read_input_mode:
                text_input_button = start_menu_status["read_input_to"]
                if event.type == pygame.TEXTINPUT:
                    try:
                        number = int(event.text)
                    except ValueError:
                        number = None
                    if number is not None:
                        text_input_button.append_text(str(number))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        text_input_button.finish_input()
                    elif event.key == pygame.K_BACKSPACE:
                        text_input_button.backspace()
            if not check_for_continue(event):
                quit_pygame()
                exit()
            elif check_for_reset(event):
                do_reset()

        simple_pygame.loop(mouse_pos=pygame.mouse.get_pos())
    simple_pygame.all_texts.clear()
    return simulation_parameters


def add_menu_items(
    simple_pygame: SimplePygame,
) -> tuple[int, int, SimulationParameters, list[Button]]:
    simulation_parameters = SimulationParameters()
    menu_items = simple_pygame.all_sprites
    width, height = pygame.display.get_window_size()
    col_w, row_h = round(width / 8), round(height / 8)
    buttons_h: dict[SwitchButton, float] = {
        SwitchButton(
            (col_w, row_h),
            (x * col_w, row_h),
            text=str(v),
            in_and_active_color=(Color.HGREEN, Color.SILVER),
        ): v
        for x, v in zip((1, 2, 3), (0.1, 0.01, 0.001))
    }
    default_button_on(buttons_h, simulation_parameters.time_step)

    def on_click_listener_h(clicked_button: SwitchButton):
        """The callback function for step size buttons."""
        simulation_parameters.time_step = buttons_h[clicked_button]
        simple_pygame.play_effect("hit_low")
        disable_other_buttons(clicked_button, list(buttons_h.keys()))

    add_switch_buttons(buttons_h.keys(), menu_items, on_click_listener_h)
    buttons_distributions: dict[SwitchButton, str] = {
        SwitchButton(
            (col_w, row_h),
            (x * col_w, y * row_h),
            text=v,
            in_and_active_color=(Color.RED, Color.SILVER),
        ): v
        for x, y, v in zip((0, 1, 0, 1, 0, 1), (4, 4, 5, 5, 6, 6), distributions.keys())
    }
    default_button_on(buttons_distributions, simulation_parameters.distribution)

    def on_click_listener_distribution(clicked_button: SwitchButton):
        """The callback function for distribution buttons."""
        simulation_parameters.distribution = buttons_distributions[clicked_button]
        simple_pygame.play_effect("hit_low")
        disable_other_buttons(clicked_button, list(buttons_distributions.keys()))

    add_switch_buttons(buttons_distributions.keys(), menu_items, on_click_listener_distribution)

    def on_click_listener_start(*args):
        """The callback function for start button."""
        start_menu_status["show_start"] = False

    button_start = SwitchButton((col_w * 2, row_h), (6 * col_w, row_h), text="Start")
    add_switch_buttons([button_start], menu_items, on_click_listener_start)

    buttons_text_input: dict[TextButton, str] = {
        TextButton(
            (col_w * 2, row_h), (5 * col_w, y * row_h), str(getattr(simulation_parameters, attr))
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
        active_text_input = start_menu_status["read_input_to"]
        if active_text_input:
            active_text_input.finish_input()
        start_menu_status["read_input_to"] = text_button

    def on_finish_input_listener(text_button: TextButton):
        """The callback function for finish input."""
        simulation_par = buttons_text_input[text_button]
        value = int(text_button.text)
        value = (
            (min(-value, value), max(-value, value))
            if simulation_par == "init_vel_range"
            else value
        )
        setattr(simulation_parameters, simulation_par, value)
        start_menu_status["read_input_to"] = None

    for button in buttons_text_input.keys():
        button.add_on_start_listener(on_start_input_listener)
        button.add_on_finish_listener(on_finish_input_listener)
        menu_items.add(button)
    buttons = (
        list(buttons_h.keys())
        + list(buttons_distributions.keys())
        + [button_start]
        + list(buttons_text_input.keys())
    )
    return col_w, row_h, simulation_parameters, buttons


def disable_other_buttons(clicked_button: SwitchButton, buttons: list[SwitchButton]):
    for other_button in buttons:
        if other_button != clicked_button:
            other_button.on = False
        else:
            # keep button active
            if not clicked_button.on:
                clicked_button.on = True


def default_button_on(buttons: dict, default):
    """Activate one button with default value."""
    for button, value in buttons.items():
        if value == default:
            button.on = True
            return


def add_switch_buttons(buttons, menu_items: pygame.sprite.Group, on_click_listener: callable):
    """Add on click callback function and buttons."""
    for button in buttons:
        button.add_on_click_listener(on_click_listener)
        menu_items.add(button)


def create_menu_texts(col_w: int, row_h: int) -> list:
    """Gets the raw texts for the start menu. This texts are just drawn, with no logic."""
    bigger_text = 25
    menu_texts = [
        ("step size dt", (0, row_h, 20, Color.HGREEN)),
        ("position distribution", (0, 3.5 * row_h, bigger_text, Color.RED)),
        ("Press ESC to quit or SPACE to reset simulation", (5, 5)),
    ]
    y = 3
    for text, limit in zip(("Rows", "Columns", "Num Molecules", "Sigma", "Init velocity"),
                           (99, 99, 999, 9, 99)):
        menu_texts.append((text,(4 * col_w, y * row_h + row_h / 2)))
        menu_texts.append(("<= " + str(limit), (7 * col_w, y*row_h + row_h/2)))
        y += 1
    return menu_texts
