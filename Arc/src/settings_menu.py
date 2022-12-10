import pygame
from state import State
from button import Button, ButtonGroup
from sprite import Sprite
from settings import Settings, Keybinding
from music_player import MusicPlayer


class SettingsMenu(State):
    """Main class that calls everything else"""

    def __init__(self, music_player: MusicPlayer) -> None:
        """Initializes SettingsMenu"""
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/settings_menu/'
        self.global_path = 'images/'
        self.default_color = Settings.settings_menu_text_color
        self.key_color = Settings.settings_menu_key_color
        self.default_font = Settings.settings_menu_font
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        self.binds_list = ['W', 'S', 'A', 'D', 'ESC', 'SPACE']

        # pygame.display.set_caption('Settings')
        # pygame.display.set_icon(pygame.image.load(
        #     f'{self.global_path}main.png'))
        self.create_game()

    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.menu_items = self.get_menu_items()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume / 100)

    def get_menu_items(self):
        font = pygame.font.Font(self.default_font, 30)
        kfont = pygame.font.Font(self.default_font, 22)
        menu_items = pygame.sprite.Group()
        menu_items.add(Sprite(250, 190, font.render(
            'MUSIC VOLUME', True, self.default_color)))
        menu_items.add(Sprite(250, 240, font.render(
            'EFFECTS VOLUME', True, self.default_color)))
        menu_items.add(Sprite(250, 285, font.render(
            'KEY BINDINGS:', True, self.default_color)))
        menu_items.add(Sprite(250, 320, kfont.render(
            'ESCAPE KEY:', True, self.default_color)))
        menu_items.add(Sprite(250, 350, kfont.render(
            'ENTER KEY:', True, self.default_color)))
        menu_items.add(Sprite(250, 380, kfont.render(
            'UP KEY:', True, self.default_color)))
        menu_items.add(Sprite(420, 320, kfont.render(
            'DOWN KEY:', True, self.default_color)))
        menu_items.add(Sprite(420, 350, kfont.render(
            'LEFT KEY:', True, self.default_color)))
        menu_items.add(Sprite(420, 380, kfont.render(
            'RIGHT KEY:', True, self.default_color)))
        return menu_items

    def get_background(self) -> Sprite:
        """Creates background as Sprite"""
        bg_image = pygame.image.load(
            f"{self.img_path}settings_menu_background.png")
        background = Sprite(0, 0, bg_image)
        background.resize(Settings.window_width, Settings.window_height)
        return background

    def get_buttons(self) -> ButtonGroup:
        """Creates a group of buttons"""

        # Action for left arrow for music volume
        def music_action_down():
            if Settings.music_volume > 0:
                Settings.music_volume -= 5
                # self.music_int -= 1
                pygame.mixer.music.set_volume(Settings.music_volume / 100)
                self.menu_sound.play()

        # Action for right arrow for music volume
        def music_action_up():
            if Settings.music_volume < 100:
                Settings.music_volume += 5
                # self.music_int += 1
                pygame.mixer.music.set_volume(Settings.music_volume / 100)
                self.menu_sound.play()

        # Action for left arrow for effects volume
        def effects_action_down():
            if Settings.effects_volume > 0:
                Settings.effects_volume -= 5
                # self.effects_int -= 1
                self.menu_sound.set_volume(Settings.effects_volume / 100)
                self.menu_sound.play()

        # Action for right arrow for effects volume
        def effects_action_up():
            if Settings.effects_volume < 100:
                Settings.effects_volume += 5
                # self.effects_int += 1
                self.menu_sound.set_volume(Settings.effects_volume / 100)
                self.menu_sound.play()

        def back_action():
            self.next_state = 'PREVIOUS'
            self.done = True

        def key_bind_default():
            Settings.default_bindings = True
            self.binds_list[0] = 'W'
            self.binds_list[1] = 'S'
            self.binds_list[2] = 'A'
            self.binds_list[3] = 'D'
            self.binds_list[5] = 'SPACE'

        def key_bind_alternate():
            Settings.default_bindings = False
            self.binds_list[0] = 'UP'
            self.binds_list[1] = 'DOWN'
            self.binds_list[2] = 'LEFT'
            self.binds_list[3] = 'RIGHT'
            self.binds_list[5] = 'RETURN'

        buttons = ButtonGroup()
        buttons.add(
            Button(490, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_down).rotate(180)
        )
        buttons.add(
            Button(550, 205, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   music_action_up)
        )
        buttons.add(
            Button(490, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_down).rotate(180)
        )
        buttons.add(
            Button(550, 250, '>', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   effects_action_up)
        )
        buttons.add(
            Button(520, 290, 'DEFAULT', pygame.font.Font('fonts/Stardew_Valley.ttf', 15),
                   key_bind_default, '#ac8269')
        )
        buttons.add(
            Button(520, 305, 'ALTERNATE', pygame.font.Font('fonts/Stardew_Valley.ttf', 15),
                   key_bind_alternate, '#ac8269')
        )
        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   back_action)
        )

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event)

    def draw_changing_texts(self, screen):
        font = pygame.font.Font('fonts/Stardew_Valley.ttf', 30)
        kfont = pygame.font.Font('fonts/Stardew_Valley.ttf', 20)
        # render fonts
        music_vol_render = font.render(
            str(Settings.music_volume), True, self.default_color)
        effects_vol_render = font.render(
            str(Settings.effects_volume), True, self.default_color)
        up_bind = kfont.render(
            self.binds_list[0], True, self.key_color)
        down_bind = kfont.render(
            self.binds_list[1], True, self.key_color)
        left_bind = kfont.render(
            self.binds_list[2], True, self.key_color)
        right_bind = kfont.render(
            self.binds_list[3], True, self.key_color)
        esc_bind = kfont.render(
            self.binds_list[4], True, self.key_color)
        ret_bind = kfont.render(
            self.binds_list[5], True, self.key_color)


        # get rects for blitting
        music_vol_rect = music_vol_render.get_rect(center=(520, 205))
        effects_vol_rect = effects_vol_render.get_rect(center=(520, 250))
        up_bind_rect = up_bind.get_rect(center=(375, 390))
        down_bind_rect = down_bind.get_rect(center=(545, 330))
        left_bind_rect = left_bind.get_rect(center=(545, 360))
        right_bind_rect = right_bind.get_rect(center=(545, 390))
        esc_bind_rect = esc_bind.get_rect(center=(375, 330))
        ret_bind_rect = ret_bind.get_rect(center=(375, 360))

        # blit renders to screen
        screen.blit(music_vol_render, music_vol_rect)
        screen.blit(effects_vol_render, effects_vol_rect)
        screen.blit(up_bind, up_bind_rect)
        screen.blit(down_bind, down_bind_rect)
        screen.blit(left_bind, left_bind_rect)
        screen.blit(right_bind, right_bind_rect)
        screen.blit(esc_bind, esc_bind_rect)
        screen.blit(ret_bind, ret_bind_rect)

    def draw(self, screen):
        self.background.draw(screen)
        self.buttons.draw(screen)
        self.menu_items.draw(screen)
        self.draw_changing_texts(screen)

    def update(self):
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.buttons.update()


def main() -> None:
    """Main function"""
    from main import main
    main('SETTINGS')


if __name__ == '__main__':
    main()
