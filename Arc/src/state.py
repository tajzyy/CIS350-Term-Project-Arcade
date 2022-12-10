"""Stores basic state information for every game
TODO: Actually implement this into the code
Also, i'm not sure if the functions that do nothing
are supposed to be finished
"""

from abc import abstractmethod
import pygame


class State:
    """Stores basic state information for every game"""

    def __init__(self):
        """Initalizes State"""
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)
        self.music_player = None

    # def startup(self, persistent):
    #     self.persist = persistent

    @abstractmethod
    def do_event(self, event):
        """Accepts and deals with inputs"""

    @abstractmethod
    def update(self, delta_time):
        """Updates all game objects"""

    @abstractmethod
    def draw(self, surface):
        """Draw all game objects"""
