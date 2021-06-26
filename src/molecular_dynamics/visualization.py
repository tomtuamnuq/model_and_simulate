from typing import Tuple

import numpy as np
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (197, 201, 107)
DGREEN = (33, 82, 24)
HGREEN = (71, 237, 38)
BROWN = (102, 9, 11)
BLUE = (67, 177, 224)


class CoordinateMapper:
    def __init__(self, simulation_dim: Tuple[int, int], display_dim: Tuple[int, int]) -> None:
        self._simulation_dim = simulation_dim
        self._display_dim = display_dim
        self._scale_matrix = self._calc_scale_matrix()

    @property
    def simulation_dim(self) -> Tuple[int, int]:
        return self._simulation_dim

    @simulation_dim.setter
    def simulation_dim(self, simulation_dim: Tuple[int, int]) -> None:
        self._simulation_dim = simulation_dim
        self._scale_matrix = self._calc_scale_matrix()

    @property
    def display_dim(self) -> Tuple[int, int]:
        return self._display_dim

    @display_dim.setter
    def display_dim(self, display_dim: Tuple[int, int]) -> None:
        self._display_dim = display_dim
        self._scale_matrix = self._calc_scale_matrix()

    def map_coordinates(self, pos_sim: np.ndarray) -> np.ndarray:
        return np.matmul(pos_sim, self._scale_matrix)

    def _calc_scale_matrix(self) -> np.ndarray:
        factor_width = self._display_dim[0] / self._simulation_dim[0]
        factor_height = self._display_dim[1] / self._simulation_dim[1]
        return np.asarray([[factor_width, 0], [0, factor_height]])


class Molecule(pygame.sprite.Sprite):
    def __init__(self, mapper: CoordinateMapper, sigma: float, pos: np.ndarray, vel: np.ndarray):
        super(Molecule, self).__init__()
        self.mapper = mapper
        self.image = pygame.Surface((2 * sigma, 2 * sigma))
        self.image.fill(RED)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, HGREEN, [sigma, sigma], sigma)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.vel = vel

    def update(self):
        rect_pos = self.mapper.map_coordinates(self.pos)
        self.rect.x = rect_pos[0]
        self.rect.y = rect_pos[1]
