import pygame

from src.molecular_dynamics.molecule_main import SimulationParameters, check_for_continue
from src.molecular_dynamics.molecule_simulation import distributions
from src.utilities.pygame_button import SwitchButton
from src.utilities.pygame_simple import SimplePygame, Color
global show_start
def show_start_screen(simple_pygame: SimplePygame) -> SimulationParameters:
    global show_start
    show_start = True
    simple_pygame.play_music_loop("menu_dark")
    col_w, row_h, simulation_parameters = add_menu_items(simple_pygame)
    menu_texts = create_menu_texts(col_w, row_h)
    for text, args in menu_texts.items():
        simple_pygame.add_text(text, *args)

    while show_start:
        eventlist = pygame.event.get()
        for event in eventlist:
            if not check_for_continue(event):
                simple_pygame.quit()
                exit()

        simple_pygame.loop(eventlist=eventlist, mouse_pos=pygame.mouse.get_pos())
    simple_pygame.all_texts.clear()
    return simulation_parameters


def add_menu_items(simple_pygame: SimplePygame) -> tuple[int, int, SimulationParameters]:
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
    check_for_default(buttons_h, simulation_parameters.time_step)

    def on_click_listener_h(clicked_button: SwitchButton):
        """The callback function for step size buttons."""
        simulation_parameters.time_step = buttons_h[clicked_button]
        simple_pygame.play_effect("hit_low")
        for other_button in buttons_h.keys():
            if other_button != clicked_button:
                other_button.on = False

    add_buttons(buttons_h.keys(), menu_items, on_click_listener_h)
    buttons_distributions: dict[SwitchButton, str] = {
        SwitchButton(
            (col_w, row_h),
            (x * col_w, y * row_h),
            text=v,
            in_and_active_color=(Color.RED, Color.SILVER),
        ): v
        for x, y, v in zip((0, 1, 0, 1, 0, 1), (4, 4, 5, 5, 6, 6), distributions.keys())
    }
    check_for_default(buttons_distributions, simulation_parameters.distribution)

    def on_click_listener_distribution(clicked_button: SwitchButton):
        """The callback function for distribution buttons."""
        simulation_parameters.distribution = buttons_distributions[clicked_button]
        simple_pygame.play_effect("hit_low")
        for other_button in buttons_distributions.keys():
            if other_button != clicked_button:
                other_button.on = False

    add_buttons(buttons_distributions.keys(), menu_items, on_click_listener_distribution)

    def on_click_listener_start(*args):
        """The callback function for start button."""
        global show_start
        show_start = False

    button_start = SwitchButton((col_w * 2, row_h), (6 * col_w, row_h), text="Start")
    add_buttons([button_start], menu_items, on_click_listener_start)
    return col_w, row_h, simulation_parameters


def check_for_default(buttons, default):
    for button, value in buttons.items():
        if value == default:
            button.on = True


def add_buttons(buttons, menu_items: pygame.sprite.Group, on_click_listener: callable):
    """Add callback function and buttons."""
    for button in buttons:
        button.add_on_click_listener(on_click_listener)
        menu_items.add(button)


def create_menu_texts(col_w: int, row_h: int) -> dict:
    """Gets the raw texts for the start menu. This texts are just drawn, with no logic."""

    bigger_text = 25
    menu_texts = {
        "step size dt": (0, row_h, 20, Color.HGREEN),
        "position distribution": (0, 3 * row_h, bigger_text, Color.RED),
        "Press ESC to quit or SPACE to reset simulation": (5, 5),
    }
    y = 3
    for text in ["Rows", "Columns", "Num Molecules", "Sigma"]:
        menu_texts[text] = 4 * col_w, y * row_h
        y += 1
    menu_texts["Init vel range"] = 4 * col_w, y * row_h, 22, Color.BLUE
    return menu_texts
