import pygame
from state import State
from sprite import Sprite
from person import Person
from button import Button, AnimatedButton, ButtonGroup
from settings import Settings
from music_player import MusicPlayer


class ArcadeMenu(State):

    def __init__(self, music_player: MusicPlayer) -> None:

        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.img_path = 'images/arcade_menu/'
        self.global_img_path = 'images/'
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        # pygame.display.set_caption('Select Game')
        # pygame.display.set_icon(pygame.image.load(
        #     f'{self.global_img_path}main.png'))
        self.create_menu()

    def create_menu(self):
        self.background = self.get_background()
        self.buttons = self.get_buttons()
        self.people = self.get_people()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

    def get_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height),
            pygame.RESIZABLE
        )
        return screen

    def get_background(self) -> Sprite:
        bg_image = pygame.image.load(f"{self.img_path}backgroundArcade.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_people(self) -> pygame.sprite.Group:
        people = pygame.sprite.Group()

        people.add(Person(815, 80, f'{self.img_path}aubrey/', 1, 150).resize(130, 150))
        people.add(Person(905, 80, f'{self.img_path}omori/', 1, 150).resize(114, 166))

        return people
    
    def get_buttons(self) -> ButtonGroup:
        def back_action():
            self.next_state = 'PREVIOUS'
            self.done = True

        def pong_action():
            self.next_state = 'PONG'
            self.done = True

        def pacman_action():
            self.next_state = 'PACMAN'
            self.done = True

        buttons = ButtonGroup()

        buttons.add(
            Button(50, 575, 'BACK', pygame.font.Font(
                'fonts/Stardew_Valley.ttf', 40), back_action, '#6B3710'))
        buttons.add(AnimatedButton(
            225, 180, f'{self.img_path}anipong/', animation_speed=150, action=pong_action, center=False).resize(100, 100))
        buttons.add(AnimatedButton(
            450, -15, f'{self.img_path}anipac/', animation_speed=150, action=pacman_action, center=False).resize(230, 230))

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event, self.menu_sound)

    def draw(self, screen):
        self.background.draw(screen)
        self.people.draw(screen)
        self.buttons.draw(screen)

    def update(self):
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.people.update()
        self.buttons.update()


def main() -> None:
    from main import main
    main('ARCADE')


if __name__ == '__main__':
    main()
