"""TODO: Actually implement this into the game
Maybe have each menu extend Game and then have Game extend State
that way they'd all have the same screen/states and stuff like that
This should also store the settings if we decide to
have a class for settings instead
The self.screen here should be used for all games
"""

import sys
import pygame
from settings import Settings
from state import State
from music_player import MusicPlayer


class StateManager:
    def __init__(self, screen, states: dict[str, State], start_state: str, music_player: MusicPlayer):
        self.states = states
        self.current_state_name = start_state
        self.current_state = self.states[self.current_state_name]
        self.state_history = []
        self.screen = screen
        self.delta_time = 1
        self.done = False
        self.paused = False
        self.clock = pygame.time.Clock()
        self.music_player = music_player

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (Settings.main_keybinding.escape, Settings.alternate_keybinding.escape):
                    # self.paused = not self.paused
                    if len(self.state_history) > 0:
                        self.do_previous_state()
                    else:
                        self.store_switch_state('PAUSE')
                    # else:
                    #     self.do_previous_state()
            self.current_state.do_event(event)
    
    def play_state(self, state_name):
        self.state_history.clear()
        self.current_state = self.states[state_name](music_player=self.music_player)

    def flip_state(self):
        # self.paused = False
        if self.current_state.next_state == 'PREVIOUS':
            self.do_previous_state()
        else:
            self.store_switch_state(self.current_state.next_state)
            # self.store_switch_state(self.current_state.next_state)
            # self.state_history.clear()
            # self.play_state(self.current_state.next_state)

    def store_switch_state(self, state_name):
        if self.current_state.next_state in ('START', 'PACMAN', 'PONG'):
            self.state_history.clear()
        else:
            # self.paused = False
            self.state_history.append(self.current_state)
        self.current_state.done = False
        self.current_state = self.states[state_name](music_player=self.music_player)
            
    def do_previous_state(self):
        self.current_state = self.state_history.pop()

    def update(self, dt):
        self.current_state.update()
        if self.current_state.done:
            self.flip_state()

    def draw(self, screen):
        self.current_state.draw(screen)
        

    def run(self):
        # while not self.done:
        #     dt = self.clock.tick(self.fps)
        #     self.event_loop()
        #     self.update(dt)
        #     self.draw()
        #     if self.count <= 0:
        #         self.count += 0.025
        #     elif self.count >= 4:
        #         self.count -= 0.025
        #     pygame.display.update()
        self.current_state = self.current_state(music_player=self.music_player)
        while not self.done:
            delta_time = self.clock.tick(Settings.fps)
            self.check_events()
            self.update(delta_time)
            self.draw(self.screen)
            pygame.display.update()
