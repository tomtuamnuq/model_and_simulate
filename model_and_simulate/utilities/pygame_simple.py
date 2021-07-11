"""Contains utility classes and functions for handling pygame."""
from enum import Enum
from os import path

import pygame as pg
import pygame.display

FONT_NAME = "arial"


class Color(Enum):
    """Color names with RGB values."""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (197, 201, 107)
    DGREEN = (33, 82, 24)
    HGREEN = (71, 237, 38)
    BROWN = (102, 9, 11)
    BLUE = (67, 177, 224)
    SILVER = (192, 192, 192)
    LIGHTGREY = (119, 136, 153)
    PERU = (205, 133, 63)
    GOLD = (255, 215, 0)
    AQUA = (0, 255, 255)
    AQUAMARINE = (127, 255, 212)


sound_music = {
    "menu_light": "looperman-l-3186957-0226264-temptation-playground-trippy-bells.wav",
    "menu_dark": "looperman-l-1564425-0238646-goa-trance-gated-vox.wav",
    "sim_bass": "looperman-l-1564425-0236875-brisk-bass-sequence.wav",
    "sim_psy": "looperman-l-2872083-0220408-k-o-r-g-2.wav",
}

sound_effects = {
    "jump": "172205__leszek-szary__jumping.wav",
    "hit_low": "254532__michael-kur95__hit-02.wav",
    "hit_high": "456168__tissman__hit3.wav",
}
sound_dir = path.join(path.dirname(__file__), "sound")
sound_dir_music = path.join(sound_dir, "music")
sound_dir_effects = path.join(sound_dir, "effects")


def play_music_loop(sound: str) -> None:
    """Play a sound with key in `sound_loops`."""
    filename = sound_music[sound]
    pg.mixer.music.load(path.join(sound_dir_music, filename))
    pg.mixer.music.play(loops=-1)


def quit_pygame() -> None:
    """End the pygame engine."""
    pg.mixer.music.fadeout(500)
    pg.quit()


def check_for_quit(event: pg.event.Event) -> bool:
    """Check if the user wants to end the simulation."""
    if event.type == pg.QUIT:
        return True
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            return True

    return False


def check_for_reset(event: pg.event.Event) -> bool:
    """Check if the user wants to reset the simulation."""
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
            return True
    return False


def get_window_resolution() -> [int, int]:
    """Returns the current width and height of the pygame display."""
    return pygame.display.get_window_size()


class SimplePygame:
    """Performs basic pygame steps."""

    def __init__(self, caption: str, width: int = 800, height: int = 600) -> None:
        pg.init()
        pg.mixer.init()
        pg.mixer.music.set_volume(0.3)
        self._screen = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        self._clock = pg.time.Clock()
        self._all_sprites = pg.sprite.Group()
        self._font = pg.font.match_font(FONT_NAME)
        self._sound_effects = {
            key: pg.mixer.Sound(path.join(sound_dir_effects, value))
            for key, value in sound_effects.items()
        }
        self._all_texts = []
        self._frames_per_second = 30

    @property
    def frames_per_second(self) -> int:
        """The frames per second for pygame clock."""
        return self._frames_per_second

    @frames_per_second.setter
    def frames_per_second(self, fps: int) -> None:
        """Sets fps if fps > 0."""
        if fps > 0:
            self._frames_per_second = fps

    @property
    def all_texts(self) -> list[tuple[str, tuple[float, float], int, Color]]:
        """List of texts to display in every loop. Contains tuples with
        text, pos_x, pos_y, text_size, color."""
        return self._all_texts

    def set_text(self, text_number: int, text: str):
        """Sets a specific text in `self.all_texts`"""
        _, pos, size, color = self.all_texts[text_number]
        self.all_texts[text_number] = text, pos, size, color

    def add_text(self, text: str, x: float, y: float, size: int = 22, color: Color = Color.WHITE):
        """Add a text to display in every loop.

        Args:
            text (str): The text to display.
            x (int): The x coordinate of the upper left.
            y (Union[int, float]): The y coordinate of the upper left.
            size (int): The size of the text.
            color (src.utilities.pygame_simple.Color): The color of the text.
        """
        self._all_texts.append((text, (int(x), int(y)), size, color.value))

    @property
    def all_sprites(self) -> pg.sprite.Group:
        """All sprites to consider in every loop. Add sprites to this group."""
        return self._all_sprites

    def loop(self, **update_kwargs) -> None:
        """Perform one loop of pygame. This updates and draws all sprites and texts."""
        self._screen.fill(Color.BLACK.value)
        self._all_sprites.update(**update_kwargs)
        self._all_sprites.draw(self._screen)
        for text_args in self._all_texts:
            self.draw_text(*text_args)
        pg.display.flip()
        self._clock.tick(self.frames_per_second)

    def play_effect(self, effect: str) -> None:
        """Play a sound effect with key in `sound_effects`."""
        self._sound_effects[effect].play()

    def draw_text(
        self,
        text: str,
        pos: tuple[float, float],
        size: int = 22,
        color: tuple[int, int, int] = Color.WHITE.value,
    ) -> None:
        """

        Args:
            text (str): The text to draw at pos.
            pos (tuple[int, int]): x and y coordinates.
            size (int): Size of the text to draw.
                Defaults to 22.
            color (tuple[int, int, int]): RGB color values.
                Defaults to white.
        """
        font = pg.font.Font(self._font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = pos
        self._screen.blit(text_surface, text_rect)
