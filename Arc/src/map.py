"""TODO: Make a map for pacman
The actual map doesn't need to be customizable or in a class,
but there needs to be a map class to draw and create the map
https://github.com/StanislavPetrovV/DOOM-style-Game/blob/main/map.py
for example
"""
from copy import deepcopy
from settings import Settings
import pygame
# 28 x 30
minimap = [
    '================================',
    '=o............................o=',
    '=.=========.========.=========.=',
    '=.=    =................=    =.=',
    '=.======.==.========.==.======.=',
    '=........==....==....==........=',
    '===.====.=====.==.=====.====.===',
    '  =.=  =.===== == =====.=  =.=  ',
    '  =.=  =.==          ==.=  =.=  ',
    '  =.=  =.== ===  === ==.=  =.=  ',
    '===.====.== =      = ==.====.===',
    '   ......   =      =   ......   ',
    '===.==.=.== = GGGG = ==.====.===',
    '  =.==.=.== =      = ==.====.=  ',
    '  =......== ======== ==......=  ',
    '  =.====.==    P     ==.==.=.=  ',
    '  =.=  =.===== == =====.==.=.=  ',
    '===.====.=====.==.=====.==.=====',
    '=........==....==....==........=',
    '=.======.==.========.==.======.=',
    '=.=    =.==.=      =.==.=    =.=',
    '=o======.==.========.==.======o=',
    '=..............................=',
    '================================',
]


class Map:
    def __init__(self, layout_text=minimap):
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.tile_width = Settings.window_width // self.width
        self.tile_height = Settings.window_height // self.height
        self.original_pacman_position = []
        self.original_ghost_positions = []

        self.game_objects = self.find_game_objects(layout_text)

    def find_game_objects(self, layout_text):
        game_objects: dict[str, list[tuple[int, int]]] = {
            'walls': [],
            'pacman': [],
            'ghosts': [],
            'food': [],
            'capsules': [],
            'empty': []
        }
        for x, row in enumerate(layout_text):
            for y, c in enumerate(row):
                if c == '=':
                    game_objects['walls'].append((y, x))
                elif c == '.':
                    game_objects['food'].append((y, x))
                elif c == 'P':
                    game_objects['pacman'].append((y, x))
                    self.original_pacman_position.append((y, x))
                elif c == 'G':
                    game_objects['ghosts'].append((y, x))
                    self.original_ghost_positions.append((y, x))
                elif c == 'o':
                    game_objects['capsules'].append((y, x))
                else:
                    game_objects['empty'].append((y, x))
        return game_objects

    def find_object_locations_on_screen(self, name):
        locations_on_screen = []
        for (x, y) in self.game_objects[name]:
            locations_on_screen.append(
                (x * self.tile_width, y * self.tile_height))
        return locations_on_screen

    def draw_food(self, screen):
        locations_on_screen = self.find_object_locations_on_screen('food')
        for (x, y) in locations_on_screen:
            pygame.draw.circle(
                screen,
                (255, 255, 204),
                (x + (self.tile_width*0.5),
                 y + (self.tile_height*0.5)),
                3
            )

    def draw_capsules(self, screen):
        locations_on_screen = self.find_object_locations_on_screen('capsules')
        for (x, y) in locations_on_screen:
            pygame.draw.circle(
                screen,
                (255, 255, 204),
                (x + (self.tile_width*0.5),
                 y + (self.tile_height*0.5)),
                7
            )

    def draw_walls(self, screen):
        locations_on_screen = self.find_object_locations_on_screen('walls')
        for (x, y) in locations_on_screen:
            wall_rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
            pygame.draw.rect(screen, (40, 40, 70), wall_rect)

    def draw(self, screen: pygame.Surface):

        # draw food
        self.draw_walls(screen)
        self.draw_food(screen)
        self.draw_capsules(screen)

        # draw 'dev balls'
        # pygame.draw.circle(screen, (100, 20, 20), (
        #     self.game_objects['pacman'][0][0] * self.tile_width, self.game_objects['pacman'][0][1] * self.tile_height), 5)
        # for i, _ in enumerate(self.game_objects['ghosts']):
        #     pygame.draw.circle(screen, (100, 20, 20), (
        #         self.game_objects['ghosts'][i][0] * self.tile_width, self.game_objects['ghosts'][i][1] * self.tile_height), 5)
    
    def set_object_location_from_list(self, name, coordinate_list: list[tuple[int, int]]):
        for i, (x, y) in enumerate(coordinate_list):
            self.game_objects[name][i] = (x//self.tile_width, y//self.tile_height)
    
    def delete_object(self, screen_coords, name):
        x, y = screen_coords
        self.game_objects[name].remove((x//self.tile_width, y//self.tile_height))
        self.game_objects['empty'].append((x//self.tile_width, y//self.tile_height))
    
    def is_colliding(self, screen_coords, name):
        x, y = screen_coords
        return (x//self.tile_width, y//self.tile_height) in self.game_objects[name]

    def is_wall(self, screen_coordinates: tuple[int, int]):
        """Returns if a given screen location is a wall based on tile size"""
        return (screen_coordinates[0]//self.tile_width, screen_coordinates[1]//self.tile_height) in self.game_objects['walls']

    def reset_positions(self):
        self.game_objects['ghosts'] = deepcopy(self.original_ghost_positions)
        self.game_objects['pacman'] = deepcopy(self.original_pacman_position)
    
    def tile_location_from_screen(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        return (screen_x//self.tile_width, screen_y//self.tile_height)

    def get_pacman_location(self):
        return self.game_objects['pacman'][0]