"""TODO: ghosts need to look in the direction they're moving
They need some kind of AI/pathfinding algorithm (probably BFS)
They'll all have the same algo, but they should ignore
tiles that have a ghost on them so that they naturally
go in different directions toward the player
"""
import random
from player import AnimatedPlayer
from settings import Settings
from map import Map


class Ghost(AnimatedPlayer):
    def __init__(self, x: int, y: int,
                 base_path: str, scared_blue_path='images/pacman/scared_ghost_blue/',
                 scared_white_path='images/pacman/scared_ghost_white/',
                 move_speed: float = 2.0, animation_speed: float = 150,
                 color=None) -> None:
        # first, calls super with all animations and sets instance variables
        super().__init__(x, y, base_path, move_speed, animation_speed, color)
        self.split_add_animations()
        self.add_animation('scared_blue', scared_blue_path, animation_speed)
        self.add_animation('scared_white', scared_white_path, animation_speed)
        self.scared = False
        self.scared_timer = 0
        self.current_direction = 'left'
        self.distance_through_tile = 0

        # this is only for random movements
        # get rid of this later
        self.temp_timer = 0

    def split_add_animations(self):
        right, down, left, up = self.split_animations('base', num_animations=4)
        self.add_animation_w_images('right', right)
        self.add_animation_w_images('down', down)
        self.add_animation_w_images('left', left)
        self.add_animation_w_images('up', up)

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

    def do_movement(self, game_map: Map) -> None:
        # if self.scared:
        #     self.do_scared()
        #     return
        movements = {
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (-self.move_speed, 0),
            'right': (self.move_speed, 0),
        }
        if self.wall_in_direction(self.current_direction, game_map, movements[self.current_direction]):
            self.movement = (0, 0)

        if self.distance_through_tile <= game_map.tile_height:
            direction = self.current_direction
            self.distance_through_tile += self.move_speed
        else:
            self.distance_through_tile = 0

            # this doesn't work right, meant to clip the ghost into the correct tile
            self.rect.topleft = (round(self.rect.topleft[0]/game_map.tile_height) * game_map.tile_height, round(self.rect.topleft[1]/game_map.tile_height) * game_map.tile_height)
            if self.scared:
                direction = self.get_scared_direction(movements, game_map)
            else:
                direction = self.get_direction(movements, game_map)
        if self.wall_in_direction(direction, game_map, movements[direction]):
            return
        self.current_direction = direction
        self.movement = movements[direction]
        self.set_animation(direction)

    def get_direction(self, movements, game_map: Map):
        start = game_map.tile_location_from_screen(self.rect.centerx, self.rect.centery)
        search = game_map.get_pacman_location()
        path_toward_pacman = self.BFS(start, search, game_map)
        if path_toward_pacman is None:
            return random.choice(list(movements.keys()))
        x1, y1 = start
        x2, y2 = path_toward_pacman[1]
        if x1 > x2:
            return 'left'
        if x1 < x2:
            return 'right'
        if y1 > y2:
            return 'up'
        return 'down'
        # self.temp_timer += 1
        # if self.temp_timer >= 25:
        #     direction = random.choice(list(movements.keys()))
        #     self.temp_timer = 0

        # return direction
    
    def get_scared_direction(self, movements, game_map):
        start = game_map.tile_location_from_screen(self.rect.centerx, self.rect.centery)
        search = (game_map.width//2, game_map.height//2)
        path_toward_pacman = self.BFS(start, search, game_map)
        if path_toward_pacman is None:
            return random.choice(list(movements.keys()))
        x1, y1 = start
        x2, y2 = path_toward_pacman[1]
        if x1 > x2:
            return 'left'
        if x1 < x2:
            return 'right'
        if y1 > y2:
            return 'up'
        return 'down'

    def BFS(self, start: tuple[int, int], search: tuple[int, int], game_map: Map):
        """inspired by 
        https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
        and work I've done in another class
        """
        # combined free spaces list
        empty = game_map.game_objects['empty']
        food = game_map.game_objects['food']
        capsules = game_map.game_objects['capsules']
        pacman = game_map.game_objects['pacman']
        ghosts = game_map.game_objects['ghosts']
        all_explorable_tiles = list(set(empty + food + capsules + pacman + ghosts))
        

        # creates a dictionary that makes each vertex have a False value (unvisited)
        visited: dict[tuple[int, int], bool] = {key: False for key in all_explorable_tiles}

        queue: list[tuple[int, int]] = []
        discovered: dict[tuple[int, int], tuple[int, int]] = {}

        queue.append(start)
        visited[start] = True
        while queue:
            (x1, y1) = queue.pop(0)

            # check all adjacent nodes
            for coordinate in ((x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1)):
                if coordinate not in all_explorable_tiles:
                    continue

                # if the vertex is not visited and the weight is not 0
                if visited[coordinate] is False:
                    queue.append(coordinate)
                    visited[coordinate] = True
                    discovered[coordinate] = (x1, y1)

                    # if we've found what we're searching
                    # for find path and return it
                    if coordinate == search:
                        path = [search]
                        while path[-1] != start:
                            path.append(discovered[path[-1]])
                        path.reverse()
                        return path
        return None

    def wall_in_direction(self, direction, game_map, movements):
        x, y = movements
        if direction == 'up':
            return game_map.is_wall((self.rect.left + 2, self.rect.top + y)) or game_map.is_wall((self.rect.right - 2, self.rect.top + y))
        elif direction == 'down':
            return game_map.is_wall((self.rect.left + 2, self.rect.bottom + y)) or game_map.is_wall((self.rect.right - 2, self.rect.bottom + y))
        elif direction == 'left':
            return game_map.is_wall((self.rect.left + x, self.rect.top + 2)) or game_map.is_wall((self.rect.left + x, self.rect.bottom - 2))
        elif direction == 'right':
            return game_map.is_wall((self.rect.right + x, self.rect.top + 2)) or game_map.is_wall((self.rect.right + x, self.rect.bottom - 2))

    def update(self, game_map):
        self.do_movement(game_map)
        if self.scared:
            self.do_scared()
        super().update()

    def do_scared(self):
        self.scared_timer += 1
        if self.scared_timer < 150:
            self.set_animation('scared_blue')
        elif self.scared_timer < 250:
            self.set_animation('scared_white')
        else:
            self.scared = False
            self.scared_timer = 0

    def do_scared_movement(self):
        pass
