"""TODO: Actually implement this into the menu"""

import sys
import pygame
from start_menu import StartMenu
from arcade_menu import ArcadeMenu
from pong import Pong
from state_manager import StateManager
from pacman import Pacman
from settings_menu import SettingsMenu
from settings import Settings
from pause_menu import PauseMenu
from music_player import MusicPlayer
from credits_menu import CreditsMenu
from win_menu import WinMenu
from pong_intro import PongIntro


def main(state):
    pygame.init()
    screen = pygame.display.set_mode(Settings.window_size)
    music_player = MusicPlayer()

    pygame.display.set_caption('ARCADE!')
    pygame.display.set_icon(pygame.image.load(
        f'images/main.png'))

    states = {
        "START": StartMenu,
        "ARCADE" : ArcadeMenu,
        "SETTINGS": SettingsMenu,
        'CREDITS': CreditsMenu,
        'PACMAN': Pacman,
        'PAUSE': PauseMenu,
        'PONG': Pong,
        'WIN': WinMenu,
        'PONG_INTRO': PongIntro
    }

    game = StateManager(screen, states, state, music_player)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main('START')
