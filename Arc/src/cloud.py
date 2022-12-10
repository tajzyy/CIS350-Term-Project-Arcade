import pygame
from sprite import Sprite


class Cloud(Sprite):
    """Cloud class that makes an image sway a
    certain distance at a certain speed
    """

    def __init__(self, img: pygame.Surface, x: int, y: int,
                 sway_distance: float, sway_speed: float) -> None:
        """Initializes cloud"""
        super().__init__(x, y, img)

        self.orig_top = self.rect.top
        self.sway_distance = sway_distance
        self.sway_speed = sway_speed
        self.movement = sway_speed

        # stores as float to have a smooth animation
        self.f_top = float(self.orig_top)

    def check_sway(self) -> None:
        """Sets the movement value based on location and sway speed"""
        if self.f_top <= self.orig_top - self.sway_distance:
            self.movement += self.sway_speed
        elif self.f_top >= self.orig_top + self.sway_distance:
            self.movement += -self.sway_speed

    def update(self) -> None:
        """Updates cloud based on top as float and movement"""
        self.check_sway()
        self.f_top += self.movement
        self.rect.top = self.f_top
