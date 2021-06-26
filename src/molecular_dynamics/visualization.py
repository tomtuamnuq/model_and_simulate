import numpy as np
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Molecule(pygame.sprite.Sprite):
    def __init__(self, sigma: float, pos: np.ndarray, vel: np.ndarray):
        super(Molecule, self).__init__()
        self.image = pygame.Surface((2 * sigma, 2 * sigma))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, RED, [sigma, sigma], sigma)
        self.rect = self.image.get_rect()

        self.pos = pos
        self.vel = vel

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
