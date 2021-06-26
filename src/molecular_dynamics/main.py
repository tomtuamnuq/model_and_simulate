import pygame
from .simulation import Simulation
from .visualization import Molecule, WHITE

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


def main():

    num_molecules = 300
    num_rows = 10
    num_columns = 10
    sigma = 1
    distribution = "uniform"
    simulation = Simulation(num_molecules, num_rows, num_columns, sigma, distribution)
    # pylint: disable=no-member
    pygame.init()
    molecule_sprites = pygame.sprite.Group()
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        vel = simulation.velocities[molecule]
        molecule_sprites.add(Molecule(sigma, pos, vel))

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        simulation.do_step()
        molecule_sprites.update()
        screen.fill(WHITE)
        molecule_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
