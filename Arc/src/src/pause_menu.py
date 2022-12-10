"""TODO: Make a general pause menu for every game
Should be pretty simple, no fancy art just some buttons
for settings/quit game (go to another menu)
Code should be pretty similar to start menu for buttons
"""
import pygame
from state import State
from settings import Settings
from sprite import Sprite
from button import Button, ButtonGroup
from music_player import MusicPlayer


class PauseMenu(State):
    def __init__(self, music_player: MusicPlayer) -> None:
        """Initializes SettingsMenu"""
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/pause_menu/'
        self.global_path = 'images/'
        self.default_color = Settings.pause_menu_text_color
        self.default_font = Settings.pause_menu_font
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        pygame.display.set_caption('Pause Menu')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_path}main.png'))
        self.create_game()

    def create_game(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

    def get_background(self):
        """Creates background as Sprite"""
        bg_image = pygame.image.load(
            f"{self.img_path}Myproject-1.png")
        background = Sprite(0, 0, bg_image)
        background.resize(Settings.window_width, Settings.window_height)
        return background

    def get_buttons(self):
        def resume_action():
            print('resume')
            self.next_state = 'PREVIOUS'
            self.done = True

        def settings_action():
            print('settings')
            self.next_state = 'SETTINGS'
            self.done = True

        def quit_action():
            print('quit')
            self.next_state = 'START'
            self.done = True

        font = pygame.font.Font('fonts/Stardew_Valley.ttf', 50)
        buttons = ButtonGroup()
        buttons.add(Button(410, 125, 'RESUME', font, resume_action))
        buttons.add(Button(410, 165, 'SETTINGS', font, settings_action))
        buttons.add(Button(410, 205, 'QUIT TO MENU', font, quit_action))
        return buttons

    def do_event(self, event):
        self.buttons.do_event(event, self.menu_sound)

    def draw(self, screen):
        self.background.draw(screen)
        self.buttons.draw(screen)

    def update(self):
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.buttons.update()


def main():
    from main import main
    main('PAUSE')


if __name__ == '__main__':
    main()
