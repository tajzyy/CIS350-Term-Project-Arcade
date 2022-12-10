"""TODO: We probably want keybindings here,
then have them either be global (like now),
or have them initialized in a class like the commented out code
Also, I'm not sure if sounds/music should be here,
maybe those should be game specific since they'll only be used in a singular game
Also, if we want to do actual resizing just have a list of some 4:3 resolutions
that you can select between
"""

import pygame


class Keybinding:
    def __init__(self, up, down, left, right, escape, enter):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.escape = escape
        self.enter = enter


class Settings:
    # global
    fps = 60
    resolutions = [(800, 600), (160, 120), (256, 192), (320, 240),
                   (320, 240), (640, 480), (960, 720), (1024, 768),
                   (1152, 864), (1280, 960)]
    aspect_ratio = 4/3
    window_size = resolutions[0]
    window_width = window_size[0]
    window_height = window_size[1]
    default_bindings = True
    main_keybinding = Keybinding(
        pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_ESCAPE, pygame.K_SPACE
    )
    alternate_keybinding = Keybinding(
        pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_ESCAPE, pygame.K_RETURN
    )
    music_volume = 20
    effects_volume = 30

    # pong
    player_buffer = 40
    background_color = pygame.Color('turquoise4')
    light_grey = (200, 200, 200)

    # start menu
    start_menu_font = 'fonts/Stardew_Valley.ttf'
    start_menu_text_color = '#DDA059'
    start_menu_hover_text_color = '#FFD921'

    # settings menu
    settings_menu_font = 'fonts/Stardew_Valley.ttf'
    settings_menu_text_color = '#A66343'
    settings_menu_key_color = '#AC8269'
    settings_menu_hover_text_color = '#FFD921'

    # pause menu
    pause_menu_font = 'fonts/Stardew_Valley.ttf'
    pause_menu_text_color = '#DDA059'
    pause_menu_hover_text_color = '#FFD921'

    # credits menu
    credits_menu_font = 'fonts/Stardew_Valley.ttf'
    credits_menu_text_color = '#A66343'
