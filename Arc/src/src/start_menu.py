import pygame
from state import State
from cloud import Cloud
from button import Button, ButtonGroup
from sprite import Sprite, AnimatedSprite
from settings import Settings
from music_player import MusicPlayer


class StartMenu(State):
    """Main class that calls everything else"""

    def __init__(self, music_player: MusicPlayer) -> None:
        """Initializes StartMenu"""
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/start_menu/'
        self.global_img_path = 'images/'
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        pygame.display.set_caption('Start Menu')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_img_path}main.png'))
        self.create_game()

    def create_game(self):
        """creates all game objects"""
        self.background = self.get_background()
        self.waterfall = self.get_waterfall()
        self.clouds = self.get_clouds()
        self.buttons = self.get_buttons()

        self.menu_sound = pygame.mixer.Sound('sounds/click.wav')
        self.menu_sound.set_volume(Settings.effects_volume/100)

    def get_waterfall(self):
        """gets animated waterfall"""
        waterfall = AnimatedSprite(
            390, 350, f'{self.img_path}waterfall/', animation_speed=150)
        waterfall.resize(60, 415)
        return waterfall

    def get_background(self) -> Sprite:
        """Creates background as Sprite"""
        bg_image = pygame.image.load(f"{self.img_path}backgroundMain.png")
        background = Sprite(0, 0, bg_image)
        background.resize(800, 600)
        return background

    def get_clouds(self, sway_distance: float = 1.5,
                   sway_speed: float = 0.025) -> pygame.sprite.Group:
        """Creates a group of clouds"""
        # load images
        large_cloud_img = pygame.image.load(f'{self.img_path}large_cloud.png')
        small_cloud_img = pygame.image.load(f'{self.img_path}small_cloud.png')
        small_cloud_mirrored = pygame.transform.flip(
            small_cloud_img, True, False)

        # add all clouds to a sprite group
        clouds = pygame.sprite.Group()

        clouds.add(Cloud(large_cloud_img, -170, 140,
                   sway_distance, sway_speed).resize(650, 650))
        clouds.add(Cloud(large_cloud_img, 500, 190,
                   sway_distance, sway_speed).resize(500, 450))
        clouds.add(Cloud(large_cloud_img, 380, 145,
                   sway_distance, sway_speed).resize(800, 760))
        clouds.add(Cloud(large_cloud_img, -290, 190,
                   sway_distance, sway_speed).resize(760, 760))
        clouds.add(Cloud(small_cloud_img, 525, 30,
                   sway_distance, sway_speed).resize(150, 100))
        clouds.add(Cloud(small_cloud_mirrored, 60, 50,
                   sway_distance, sway_speed).resize(200, 170))

        return clouds

    def get_buttons(self) -> ButtonGroup:
        """Creates a group of buttons"""
        def arcade_action():
            print('arcade')
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound('sounds/arcade_door.wav')
            )
            self.next_state = 'ARCADE'
            self.done = True

        def settings_action():
            print('settings')
            self.next_state = 'SETTINGS'
            self.done = True

        def credits_action():
            print('credits')
            self.next_state = 'CREDITS'
            self.done = True

        buttons = ButtonGroup()
        buttons.add(Button(410, 125, 'ENTER ARCADE', pygame.font.Font(
            'fonts/Stardew_Valley.ttf', 50), arcade_action))
        buttons.add(Button(410, 165, 'SETTINGS', pygame.font.Font(
            'fonts/Stardew_Valley.ttf', 40), settings_action))
        buttons.add(Button(410, 205, 'CREDITS', pygame.font.Font(
            'fonts/Stardew_Valley.ttf', 30), credits_action))

        return buttons

    def do_event(self, event):
        self.buttons.do_event(event, self.menu_sound)

    def draw(self, screen):
        self.background.draw(screen)
        self.waterfall.draw(screen)
        self.clouds.draw(screen)
        self.buttons.draw(screen)

    def update(self):
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.waterfall.update()
        self.clouds.update()
        self.buttons.update()


def main() -> None:
    """Main function"""
    from main import main
    main('START')


if __name__ == '__main__':
    main()
