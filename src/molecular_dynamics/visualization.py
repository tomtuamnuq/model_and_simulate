import numpy as np
import pygame
from src.utilities.coordinate_mapper import CoordinateMapper2D
from src.utilities.pygame_utils import Color


class Molecule(pygame.sprite.Sprite):
    def __init__(self, mapper: CoordinateMapper2D, sigma: float, pos: np.ndarray, vel: np.ndarray):
        super(Molecule, self).__init__()
        self.mapper = mapper
        self.image = pygame.Surface((2 * sigma, 2 * sigma))
        self.image.fill(Color.WHITE.value)
        self.image.set_colorkey(Color.WHITE.value)
        pygame.draw.circle(self.image, Color.HGREEN.value, [sigma, sigma], sigma)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.vel = vel

    def update(self):
        rect_pos = self.mapper.map_coordinates(self.pos)
        self.rect.x = rect_pos[0]
        self.rect.y = rect_pos[1]
