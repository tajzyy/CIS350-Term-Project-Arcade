import pygame
from state import State
from button import Button, ButtonGroup
from sprite import Sprite
from settings import Settings, Keybinding
from music_player import MusicPlayer


class PongIntro(State):
    """Main class that calls everything else"""
    num_players = 0

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
        self.create_game()

    def create_game(self):
        self.buttons = self.get_buttons()
        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume / 100)

    def get_buttons(self) -> ButtonGroup:
        """Creates a group of buttons"""
        def one_player():
            self.num_players = 1
            self.menu_sound.play()
        
        def two_player():
            self.num_players = 2
            self.menu_sound.play()

        def back_action():
            self.next_state = 'PREVIOUS'
            self.done = True

        buttons = ButtonGroup()
        buttons.add(
            Button(400, 205, 'One Player', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   one_player)
        )
        buttons.add(
            Button(400, 270, 'Two Players', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   two_player)
        )
        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   back_action)
        )

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.buttons.draw(screen)

    def update(self):
        self.music_player.stop()
        self.buttons.update()


def main() -> None:
    """Main function"""
    from main import main
    main('PONG_INTRO')


if __name__ == '__main__':
    main()
