import pygame
from player import AnimatedPlayer
from settings import Settings


class Person(AnimatedPlayer):

    def __init__(self, x: int, y: int,
                 base_path: str, move_speed: float = 1.0, 
                 animation_speed: float = 100,
                 color=None) -> None:
        super().__init__(x, y, base_path, move_speed, animation_speed, color=color)

        self.original_x = x
        self.original_y = y

    def check_out_of_bounds(self):
        if self.rect.top > Settings.window_height:
            self.rect.topleft = (self.original_x, self.original_y)

    def do_movement(self) -> None:
        self.movement = (-self.move_speed, self.move_speed)

    # def check_movement(self) -> None:
    #     if self.x < 100:
    #         self.f_top -= self.move_vert
    #         self.f_left += self.move_hori
    #     elif self.x > 100:
    #         self.f_top += self.move_vert
    #         self.f_left -= self.move_hori
    
    def update(self) -> None:
        #self.check_movement()
        self.do_movement()
        super().update()
        # self.rect.top = self.f_top
        # self.rect.left = self.f_left
