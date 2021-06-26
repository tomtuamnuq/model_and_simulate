import pygame
from .simulation import Simulation
from .visualization import Molecule, BLACK, CoordinateMapper


def main():
    num_molecules = 500
    display_dim = (800, 600)
    num_rows = 15
    num_columns = 15
    sigma = 1
    distribution = "uniform"
    simulation = Simulation(num_molecules, num_rows, num_columns, sigma, distribution)
    pygame.init()
    molecule_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(display_dim)
    coord_mapper = CoordinateMapper(simulation.dim, display_dim)
    for molecule in simulation.molecules:
        pos = simulation.positions[molecule]
        vel = simulation.velocities[molecule]
        molecule_sprites.add(Molecule(coord_mapper, sigma, pos, vel))

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        simulation.do_step()
        molecule_sprites.update()
        screen.fill(BLACK)
        molecule_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
