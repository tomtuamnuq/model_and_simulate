"""Module with `Molecule` class as visualization in pygame."""
import numpy as np
import pygame
from model_and_simulate.utilities.coordinate_mapper import CoordinateMapper2D
from model_and_simulate.utilities.pygame_simple import Color


class Molecule(pygame.sprite.Sprite):
    """A visualization of a single molecule as pygame Sprite."""
    colors = [c for c in Color.__members__.values()]

    def __init__(self, mapper: CoordinateMapper2D, sigma: float, pos: np.ndarray):
        """

        Args:
            mapper (CoordinateMapper2D): An instance to use for position mapping.
            sigma (float): The radius of the molecule.
            pos (np.ndarray): An array with x-y coordinates to follow.
        """
        super(Molecule, self).__init__()
        self.mapper = mapper
        self.image = pygame.Surface((2 * sigma, 2 * sigma))
        self.image.fill(Color.WHITE.value)
        self.image.set_colorkey(Color.WHITE.value)
        color = Molecule.colors[np.random.randint(0, len(Molecule.colors))]
        pygame.draw.circle(self.image, color.value, [sigma, sigma], sigma)
        self.rect = self.image.get_rect()
        self.pos = pos

    def update(self):
        """Set the position in accordance with the position in numpy array."""
        rect_pos = self.mapper.map_coordinates(self.pos)
        self.rect.x = rect_pos[0]
        self.rect.y = rect_pos[1]
