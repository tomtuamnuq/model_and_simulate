import pygame
from .molecule_simulation import MoleculeSimulation
from .visualization import Molecule
from src.utilities.coordinate_mapper import CoordinateMapper2D
from src.utilities.pygame_utils import SimplePygame


def molecule_main():
    simple_pygame = SimplePygame("Molecule Simulation")
    simple_pygame.play_music_loop("sim_psy")
    width, height = pygame.display.get_window_size()
    num_molecules = 500
    num_rows = 15
    num_columns = 15
    sigma = 1
    distribution = "exponential_center"
    time_step = 0.01
    init_vel_range = -0.2, 0.2
    simulation = MoleculeSimulation(
        num_molecules, num_rows, num_columns, sigma, distribution, time_step, init_vel_range
    )
    molecule_sprites = simple_pygame.all_sprites
    display_dim = ((0, width), (0, height))
    coord_mapper = CoordinateMapper2D(*simulation.dim, *display_dim)
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        vel = simulation.velocities[molecule]
        molecule_sprites.add(Molecule(coord_mapper, sigma, pos, vel))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    simple_pygame.play_effect("hit_low")
        simulation.do_step()
        simple_pygame.loop()

    simple_pygame.quit()
