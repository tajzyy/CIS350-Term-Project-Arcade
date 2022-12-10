from abc import abstractmethod
import pygame
from sprite import Sprite, AnimatedSprite
from settings import Settings


class AnimatedPlayer(AnimatedSprite):
    def __init__(self, x: int, y: int,
                 base_path: str, move_speed: float,
                 animation_speed: float, color=None):
        super().__init__(x, y, base_path, animation_speed, color=color)
        self.allow_player_movement = True
        self.move_speed = move_speed
        self.movement = (0, 0)

    def get_direction(self) -> str:
        if not self.allow_player_movement:
            return
        direction = None
        keys = pygame.key.get_pressed()
        if Settings.default_bindings:
            if keys[Settings.main_keybinding.up]:
                direction = 'up'
            elif keys[Settings.main_keybinding.down]:
                direction = 'down'
            elif keys[Settings.main_keybinding.left]:
                direction = 'left'
            elif keys[Settings.main_keybinding.right]:
                direction = 'right'
        else:
            if keys[Settings.alternate_keybinding.up]:
                direction = 'up'
            elif keys[Settings.alternate_keybinding.down]:
                direction = 'down'
            elif keys[Settings.alternate_keybinding.left]:
                direction = 'left'
            elif keys[Settings.alternate_keybinding.right]:
                direction = 'right'
        return direction

    def check_out_of_bounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width

    @abstractmethod
    def do_movement(self) -> None:
        pass

    def update(self) -> None:
        self.rect.left += self.movement[0]
        self.rect.top += self.movement[1]
        self.check_out_of_bounds()
        super().update()

# copy of AnimatedPlayer except for single img


class StaticPlayer(Sprite):
    def __init__(self, x: int, y: int,
                 img: pygame.Surface, move_speed: float,
                 color=None) -> None:
        super().__init__(x, y, img, color)
        self.allow_player_movement = True
        self.move_speed = move_speed
        self.movement = (0, 0)

    def get_direction(self) -> str:
        if not self.allow_player_movement:
            return
        direction = None
        keys = pygame.key.get_pressed()
        if Settings.default_bindings:
            if keys[Settings.main_keybinding.up]:
                direction = 'up'
            elif keys[Settings.main_keybinding.down]:
                direction = 'down'
            elif keys[Settings.main_keybinding.left]:
                direction = 'left'
            elif keys[Settings.main_keybinding.right]:
                direction = 'right'
        else:
            if keys[Settings.alternate_keybinding.up]:
                direction = 'up'
            elif keys[Settings.alternate_keybinding.down]:
                direction = 'down'
            elif keys[Settings.alternate_keybinding.left]:
                direction = 'left'
            elif keys[Settings.alternate_keybinding.right]:
                direction = 'right'
        return direction

    def check_out_of_bounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width

    @abstractmethod
    def do_movement(self) -> None:
        pass

    def update(self) -> None:
        self.rect.left += self.movement[0]
        self.rect.top += self.movement[1]
        self.check_out_of_bounds()
        super().update()
