"""Module with pygame Button classes."""
from abc import ABC, abstractmethod
import pygame as pg
from pygame.sprite import Sprite

from .pygame_simple import Color


class Button(Sprite, ABC):
    """Abstract base class for pygame buttons."""

    font_antialias: bool = True
    font_name: str = "arial"
    inner_surface_offset_factor: float = 1 / 5

    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[int, int],
        text: str,
        text_color: Color,
        in_and_active_color: tuple[Color, Color],
        off_on_color: tuple[Color, Color],
    ) -> None:
        """
        Create a colored button with hover effects and text.
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
        self._on_hover_listeners = []  # type: list[callable]
        self.text = text

    def _draw_outer_color(self, active: bool) -> None:
        color = self._active_color if active else self._inactive_color
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

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """Check the button logic in every loop."""
        active = self.check_active(mouse_pos)
        if active:
            for listener in self._on_hover_listeners:
                listener(self)
        self._draw_outer_color(active)
        self._draw_inner_color()
        self._draw_text()
        self.image.blit(self._inner_surface, self._offset)

    def add_on_hover_listener(self, listener: callable) -> None:
        """Listener to call when mouse is over the outer rectangle."""
        self._on_hover_listeners.append(listener)

    def clear_on_hover_listeners(self) -> None:
        """Removes all added on click listeners."""
        self._on_hover_listeners.clear()

    def check_active(self, pos: tuple[int, int]) -> bool:
        """Checks if pos is in outer rectangle."""
        return self._rect.collidepoint(pos)

    def check_pos_collision(self, pos: tuple[float, float]) -> bool:
        """Checks if pos is in inner rectangle."""
        return self._inner_rect.collidepoint(pos)

    @property
    def rect(self) -> pg.Rect:
        """The rectangle which defines positions."""
        return self._rect

    @property
    def image(self) -> pg.Surface:
        """The surface that gets blit on the screen."""
        return self._image

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
        self._one_line = font.size(text)[0] <= self._inner_rect.width

    @abstractmethod
    def check_click(self, pos: tuple[float, float]):
        """Define what happens when a user hits the button."""
        pass


class SwitchButton(Button):
    """A clickable on/off button with out-and inner color and text for pygame."""

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
        Create a switch button with hover effects and text.
        Args:
            size (Tuple[int, int]): width and height.
            pos (Tuple[int, int]): x and y coordinates.
            text (str): Text to display.
            in_and_active_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Outercolors for hovering effect.
            off_on_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Innercolors for enabling.
        """
        Button.__init__(self, size, pos, text, text_color, in_and_active_color, off_on_color)
        self._on_click_listeners = []  # type: list[callable]

    @property
    def on(self) -> bool:
        """Status of this button."""
        return self._on

    @on.setter
    def on(self, on: bool) -> None:
        """Setter for on."""
        self._on = on

    def add_on_click_listener(self, listener: callable) -> None:
        """Listener to call when button is clicked."""
        self._on_click_listeners.append(listener)

    def check_click(self, mouse_pos: tuple[float, float]):
        """Checks if clicked and switches the status, starts on click event."""
        if self.check_pos_collision(mouse_pos):
            self._on_clicked()

    def _on_clicked(self) -> None:
        self._on = not self._on
        for listener in self._on_click_listeners:
            listener(self)

    def clear_on_click_listeners(self) -> None:
        """Removes all added on click listeners."""
        self._on_click_listeners.clear()


class TextButton(Button):
    """A clickable button with out-and inner color and text input functionality for pygame.
    The button can initiate start and finish events. It starts the input event if clicked and
    a finish event if the maximum length of input is reached."""

    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[int, int],
        text: str = "",
        max_length: int = 0,
        text_color: Color = Color.BLACK,
        in_and_active_color: tuple[Color, Color] = (Color.AQUAMARINE, Color.AQUA),
        off_on_color: tuple[Color, Color] = (Color.LIGHTGREY, Color.WHITE),
    ) -> None:
        """
        Create a text input button with hover effects.
        Args:
            size (Tuple[int, int]): width and height.
            pos (Tuple[int, int]): x and y coordinates.
            text (str): Text to display.
            max_length (int): Maximum length of text. It is at least len(text).
            in_and_active_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Outercolors for hovering effect.
            off_on_color (Tuple[pygame_simple.Color, pygame_simple.Color]):
                Innercolors tho show whether text input is on or off.
        """
        self._max_length = max(len(text), max_length)
        Button.__init__(self, size, pos, text, text_color, in_and_active_color, off_on_color)
        self._on_start_listeners = []  # type: list[callable]
        self._on_finish_listeners = []  # type: list[callable]

    def check_click(self, mouse_pos: tuple[float, float]):
        """Checks if clicked, starts input event."""
        if not self._on and self.check_pos_collision(mouse_pos):
            self._on = True
            for listener in self._on_start_listeners:
                listener(self)

    def append_text(self, letter: str) -> None:
        """Adds the letter to the button text and starts finish event if `max_length` reached."""
        self.text = self._text + letter
        if len(self._text) == self._max_length:
            self.finish_input()

    def backspace(self) -> None:
        """Removes the last letter of the button text."""
        self.text = self._text[:-1]

    @Button.text.setter
    def text(self, text: str) -> None:
        """Setter for text. It respects `self._max_length`."""
        text = text[: self._max_length]
        Button.text.fset(self, text)  # call parent property setter

    def finish_input(self):
        """Finish the text input."""
        self._on = False
        for listener in self._on_finish_listeners:
            listener(self)

    def add_on_start_listener(self, listener: callable) -> None:
        """Adds function to call when text input starts."""
        self._on_start_listeners.append(listener)

    def add_on_finish_listener(self, listener: callable) -> None:
        """Adds function to call when text input is finished."""
        self._on_finish_listeners.append(listener)

    def clear_on_start_listeners(self) -> None:
        """Removes all added on start listeners."""
        self._on_start_listeners.clear()

    def clear_on_finish_listeners(self) -> None:
        """Removes all added on finish listeners."""
        self._on_finish_listeners.clear()
