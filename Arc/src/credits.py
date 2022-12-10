import pygame
from state import State
from button import Button, ButtonGroup
from sprite import Sprite
from settings import Settings
from music_player import MusicPlayer


class CreditsMenu(State):

    def __init__(self, music_player: MusicPlayer) -> None:
        
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/credits_menu/'
        self.global_path = 'images/'
        self.default_color = Settings.settings_menu_text_color
        self.default_font = Settings.settings_menu_font
        self.music_player = music_player
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Credits')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_path}main.png'))
        self.create_game()

    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.menu_items = self.get_menu_items()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

    def get_menu_items(self):
        font = pygame.font.Font(self.default_font, 30)
        menu_items = pygame.sprite.Group()
        menu_items.add(Sprite(360, 150, font.render(
            'FONTS', True, self.default_color)))
        menu_items.add(Sprite(360, 230, font.render(
            'MUSIC', True, self.default_color)))
        menu_items.add(Sprite(355, 320, font.render(
            'IMAGES', True, self.default_color)))
        menu_items.add(Sprite(280, 330, font.render(
            '', True, self.default_color)))
        menu_items.add(Sprite(280, 380, font.render(
            '', True, self.default_color)))
        return menu_items

    def get_background(self) -> Sprite:
        """Creates background as Sprite"""
        bg_image = pygame.image.load(
            f"{self.img_path}credits_menu_background.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_buttons(self) -> ButtonGroup:
        """Creates a group of buttons"""

        def back_action():
            print('back')
            self.next_state = 'START'
            self.done = True

        buttons = ButtonGroup()
    
        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font('fonts/Stardew_Valley.ttf', 40),
                   back_action)
        )

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event)

    def draw(self, screen):
        self.background.draw(screen)
        self.buttons.draw(screen)
        self.menu_items.draw(screen)

    def update(self):
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.buttons.update()


def main() -> None:
    """Main function"""
    from main import main
    main('SETTINGS')


if __name__ == '__main__':
    main()
