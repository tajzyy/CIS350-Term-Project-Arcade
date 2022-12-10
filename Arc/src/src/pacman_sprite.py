"""TODO: Fix collision with window borders (hitbox is wonky)
Make movements fixed to a grid (move like normal pacman)
Switch to pacman death when you touch a ghost
(check for collisions with ghosts, switching animation done in animated_sprite.py)
"""

from player import AnimatedPlayer
from settings import Settings
# from map import Map


class PacmanSprite(AnimatedPlayer):
    def __init__(self, x: int, y: int,
                 base_path: str, death_path: str,
                 move_speed: float = 2.0, animation_speed: float = 100,
                 color=None) -> None:
        super().__init__(x, y, base_path, move_speed, animation_speed, color=color)
        self.add_animation('death', death_path, animation_speed*2)
    
    def check_out_of_bounds(self):
        # use 1 because 0 can make clipping at the edge possible
        if self.rect.centerx < 1:
            self.rect.centerx = Settings.window_width
        elif self.rect.centerx >= Settings.window_width:
            self.rect.centerx = 1
        elif self.rect.centery < 1:
            self.rect.centery = Settings.window_height
        elif self.rect.centery >= Settings.window_height:
            self.rect.centery = 1

    # good I think
    def do_movement(self) -> None:
        # movement, rotation
        # x, y, '-' is up/left
        # rotation in degrees from facing right
        # counter-clockwise in degrees
        movements = {
            'up': [(0, -self.move_speed), 90],
            'down': [(0, self.move_speed), 270],
            'left': [(-self.move_speed, 0), 180],
            'right': [(self.move_speed, 0), 0]
        }

        # find direction based on keys pressed
        # sets movement and rotates pacman
        if (direction := self.get_direction()) is not None:
            self.set_animation('base')
            self.rotate(movements[direction][1])
            self.movement = movements[direction][0]

    def update(self, map):
        self.old_movement = self.movement
        self.do_movement()

        if map.is_wall((self.rect.centerx + self.movement[0], self.rect.centery + self.movement[1])):
            self.movement = (0, 0)
        super().update()
