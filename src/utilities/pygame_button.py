"""Module with pygame Button classes."""
import pygame as pg

from .pygame_simple import Color


class SwitchButton(pg.sprite.Sprite):
    """A clickable on/off button with out-and inner color and text for pygame."""

    inner_surface_offset_factor: float = 1 / 5
    font_name: str = "arial"
    font_antialias: bool = True

    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[int, int],
        text: str = "",
        text_color: Color = Color.WHITE,
        in_and_active_color: tuple[Color, Color] = (Color.LIGHTGREY, Color.SILVER),
        off_on_color: tuple[Color, Color] = (Color.PERU, Color.GOLD),
    ) -> None:
        """
        Create a button.
        Args:
            size (Tuple[int, int]): width and height.
            pos (Tuple[int, int]): x and y coordinates.
            text (str): Text to display.
            in_and_active_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Outercolors for hovering effect.
            off_on_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Innercolors for enabling.
        """
        pg.sprite.Sprite.__init__(self)
        self._inactive_color = in_and_active_color[0].value
        self._active_color = in_and_active_color[1].value
        self._active = False
        self._off_color = off_on_color[0].value
        self._on_color = off_on_color[1].value
        self._on = False
        self._image = pg.Surface([*size])
        self._offset = (
            size[0] * SwitchButton.inner_surface_offset_factor,
            size[1] * SwitchButton.inner_surface_offset_factor,
        )
        self._inner_surface = pg.Surface(
            [
                size[0] - 2 * self._offset[0],
                size[1] - 2 * self._offset[1],
            ]
        )
        self._rect = self._image.get_rect()
        self._rect.topleft = pos
        self._inner_rect = self._inner_surface.get_rect()
        self._inner_rect.topleft = pos[0] + self._offset[0], pos[1] + self._offset[1]
        self._text_color = text_color.value
        self._one_line = True
        self._on_click_listeners = []  # type: list[callable]
        self.text = text

    @property
    def on(self) -> bool:
        return self._on

    @on.setter
    def on(self, on: bool) -> None:
        self._on = on

    @property
    def image(self) -> pg.Surface:
        """The surface that gets blit on the screen."""
        return self._image

    @property
    def rect(self) -> pg.Rect:
        """The rectangle which defines positions."""
        return self._rect

    @property
    def text(self) -> str:
        """The text to display in the inner rectangle."""
        return self._text

    @text.setter
    def text(self, text: str):
        """Set the text."""
        self._text = text
        font = pg.font.SysFont(
            SwitchButton.font_name,
            self._inner_rect.height,
        )
        self._one_line = (
            font.size(text)[0]
            <= self._inner_rect.width
        )

    def update(self, eventlist: list[pg.event], mouse_pos: tuple[int, int]) -> None:
        """Check the button logic in every loop."""
        for event in eventlist:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self._inner_rect.collidepoint(event.pos):
                    self._on_clicked()
        self._draw_outer_color(mouse_pos)
        self._draw_inner_color()
        self._draw_text()
        self.image.blit(self._inner_surface, self._offset)

    def add_on_click_listener(self, listener: callable) -> None:
        """Listener to call with on/off when button is clicked."""
        self._on_click_listeners.append(listener)

    def _on_clicked(self) -> None:
        self._on = not self._on
        for listener in self._on_click_listeners:
            listener(self)

    def _draw_outer_color(self, mouse_pos) -> None:
        color = self._active_color if self._rect.collidepoint(mouse_pos) else self._inactive_color
        self.image.fill(color)

    def _draw_inner_color(self) -> None:
        color = self._on_color if self._on else self._off_color
        self._inner_surface.fill(color)

    def _draw_text(self) -> None:
        font_height = (
            self._inner_rect.height if self._one_line else round(self._inner_rect.height / 2)
        )
        text = self._text if self._one_line else self._text[: round(len(self._text) / 2)] + "-"
        font = pg.font.SysFont(SwitchButton.font_name, font_height)
        text_surface = font.render(text, SwitchButton.font_antialias, self._text_color)
        self._inner_surface.blit(text_surface, (0, 0))
        if not self._one_line:
            text = self._text[round(len(self._text) / 2) :]
            text_surface = font.render(text, SwitchButton.font_antialias, self._text_color)
            self._inner_surface.blit(text_surface, (0, font_height))
