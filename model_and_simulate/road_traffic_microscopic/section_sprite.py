"""Module with `CellSprite` class as visualization of `Section` in pygame."""
import pygame
from .section import Section
from model_and_simulate.utilities.coordinate_mapper import CoordinateMapper2D
from model_and_simulate.utilities.pygame_simple import Color


class SectionSprite(pygame.sprite.Sprite):
    """A visualization of a `Section` as pygame Sprite."""

    inner_surface_offset_factor: float = 1 / 5

    def __init__(
        self,
        mapper: CoordinateMapper2D,
        section: Section,
        pos_y: int,
        height: float,
        empty_and_filled_color: tuple[Color, Color] = (Color.LIGHTGREY, Color.GOLD),
        one_time_drawing: bool = False,
    ):
        """
        Args:
            mapper (CoordinateMapper2D): An instance to use for position mapping.
            section (Section): The `Section` instance to visualize.
            pos_y (int): The position on the y-Axis to draw.
            height (int): The height of this section on the y-Axis.
            empty_and_filled_color (Tuple[Color, Color]): The colors to use
                for empty and filled cells. Defaults to (Color.LIGHTGREY, Color.GOLD).
            one_time_drawing (bool): Set whether the section should be redrawn in `update`.

        """
        super(SectionSprite, self).__init__()
        self.mapper = mapper
        self._section = section
        self._empty_color = empty_and_filled_color[0].value
        self._filled_color = empty_and_filled_color[1].value
        length = mapper.scale_size_x(section.length)
        self._image = pygame.Surface([length, height])
        self._rect = self._image.get_rect()
        self.rect.x = 0
        self.rect.y = pos_y
        self._bottom_offset = height * SectionSprite.inner_surface_offset_factor
        cell_size = mapper.scale_size_x(section.cell_size)
        cell_offset = cell_size * SectionSprite.inner_surface_offset_factor
        self._cell_surface = pygame.Surface(
            [cell_size - 2 * cell_offset, self._rect.height - self._bottom_offset]
        )
        self._cell_surface.fill(self._filled_color)
        self._offset = cell_offset
        self._one_time_drawing = one_time_drawing
        if one_time_drawing:
            self._draw_cells()

    def update(self):
        """Draw the occupied cells."""
        if not self._one_time_drawing:
            self._draw_cells()

    def _draw_cells(self) -> None:
        self._image.fill(self._empty_color)
        pygame.draw.rect(
            self.image,
            Color.BROWN.value,
            (0, self._rect.height - self._bottom_offset, self._rect.width, self._bottom_offset),
        )
        for cell in self._section.cells:
            if not cell.is_empty():
                offset = self.mapper.scale_size_x(cell.position) + self._offset, 0
                self._image.blit(self._cell_surface, offset)

    @property
    def rect(self) -> pygame.Rect:
        """The rectangle which defines positions."""
        return self._rect

    @property
    def image(self) -> pygame.Surface:
        """The surface that gets blit on the screen."""
        return self._image
