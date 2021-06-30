"""Contains utility classes and functions for handling pygame."""
from enum import Enum
from os import path
import pygame as pg

FONT_NAME = "arial"
FPS = 30  # frames per second


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


class SimplePygame:
    """Performs basic pygame steps."""

    def __init__(self, caption: str, width: int = 800, height: int = 600) -> None:
        pg.init()
        pg.mixer.init()
        pg.mixer.music.set_volume(0.4)
        self._screen = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        self._clock = pg.time.Clock()
        self._all_sprites = pg.sprite.Group()
        self._font = pg.font.match_font(FONT_NAME)
        self._sound_effects = {
            key: pg.mixer.Sound(path.join(sound_dir_effects, value))
            for key, value in sound_effects.items()
        }

    @property
    def all_sprites(self) -> pg.sprite.Group:
        """All sprites to consider in every loop. Add sprites to this group."""
        return self._all_sprites

    def loop(self) -> None:
        """Perform one loop of pygame. This updates and draws all sprites."""
        self._all_sprites.update()
        self._screen.fill(Color.BLACK.value)
        self._all_sprites.draw(self._screen)
        self.draw_text("Test", 0, 0)
        pg.display.flip()
        self._clock.tick(FPS)

    def play_music_loop(self, sound: str) -> None:
        """Play a sound with key in `sound_loops`."""
        filename = sound_music[sound]
        pg.mixer.music.load(path.join(sound_dir_music, filename))
        pg.mixer.music.play(loops=-1)

    def play_effect(self, effect: str) -> None:
        """Play a sound effect with key in `sound_effects`."""
        self._sound_effects[effect].play()

    def quit(self) -> None:
        """End the pygame engine."""
        pg.mixer.music.fadeout(500)
        pg.quit()

    def draw_text(
        self, text: str, x: float, y: float, size: int = 22, color: Color = Color.WHITE
    ) -> None:
        color = color.value
        font = pg.font.Font(self._font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (int(x), int(y))
        self._screen.blit(text_surface, text_rect)
