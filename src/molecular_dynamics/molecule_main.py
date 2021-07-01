import dataclasses
from dataclasses import dataclass
import pygame
from .molecule_simulation import MoleculeSimulation
from .visualization import Molecule
from src.utilities.coordinate_mapper import CoordinateMapper2D
from src.utilities.pygame_simple import SimplePygame
from ..utilities.pygame_button import SwitchButton


@dataclass
class SimulationParameters:
    """Class for keeping track of the simulation parameters in menu."""

    num_molecules: int = 500
    num_rows: int = 15
    num_columns: int = 15
    sigma: float = 1
    distribution: str = "gumbel"
    time_step: float = 0.01
    init_vel_range: tuple[int, int] = -10, 10


def molecule_main():
    simple_pygame = SimplePygame("Molecule Simulation")
    simulation_parameters = show_start_screen(simple_pygame)
    simple_pygame.play_music_loop("sim_psy")
    simulation = MoleculeSimulation(*dataclasses.astuple(simulation_parameters))
    width, height = pygame.display.get_window_size()
    display_dim = ((0, width), (0, height))
    coord_mapper = CoordinateMapper2D(*simulation.dim, *display_dim)
    molecule_sprites = simple_pygame.all_sprites
    molecule_sprites.empty()
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        vel = simulation.velocities[molecule]
        molecule_sprites.add(Molecule(coord_mapper, simulation_parameters.sigma, pos, vel))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    simple_pygame.play_effect("hit_low")
        simulation.do_step()
        simple_pygame.loop()

    simple_pygame.quit()


def show_start_screen(simple_pygame: SimplePygame) -> SimulationParameters:
    simple_pygame.play_music_loop("menu_dark")
    simulation_parameters = SimulationParameters()
    menu_items = simple_pygame.all_sprites
    width, height = pygame.display.get_window_size()
    col_w, row_h = round(width / 8), round(height / 8)
    buttons_h: dict[SwitchButton, float] = {
        SwitchButton((col_w, row_h), (x * col_w, row_h), text=str(v)): v
        for x, v in zip((2, 3, 4), (0.1, 0.01, 0.001))
    }

    def on_click_listener_h(clicked_button: SwitchButton):
        simulation_parameters.time_step = buttons_h[clicked_button]
        simple_pygame.play_effect("hit_low")
        for other_button in buttons_h.keys():
            if other_button != clicked_button:
                other_button.on = False

    for button in buttons_h.keys():
        button.add_on_click_listener(on_click_listener_h)
        menu_items.add(button)

    menu_texts = {"h delta_t": (col_w, row_h, 30), "position distribution": (col_w,3 * row_h)}
    y = 2
    for text in ["Rows", "Columns", "Num Molecules", "Sigma", "Init vel range"]:
        menu_texts[text] = 4*col_w, y * row_h
        y += 1
    for text, args in menu_texts.items():
        simple_pygame.add_text(text, *args)
    show_start = True
    while show_start:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                simple_pygame.quit()
                exit()

        simple_pygame.loop(eventlist=eventlist, mouse_pos=pygame.mouse.get_pos())

    return simulation_parameters
