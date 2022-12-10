"""TODO: Ghosts need to move
Ghosts need to interact with pacman
Pacman hitbox is all messed up for some reason (probably in pacman_sprite.py)
Add some sounds/music
Maybe some buttons for settings/pausing?
or maybe those will be part of the eventual pause menu
"""

import pygame
from pacman_sprite import PacmanSprite
from state import State
from settings import Settings
from ghost import Ghost
from music_player import MusicPlayer
from map import Map


class Pacman(State):

    def __init__(self, music_player: MusicPlayer):
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/pacman/'
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        # self.screen = self.get_screen()
        pygame.display.set_caption('Pacman')
        self.score = 0
        self.create_game()

    def create_game(self):
        # self.music_player.load_play_music('music/pacman_beginning.wav', 1, True)
        # self.death_sound = pygame.mixer.Sound('sounds/pacman_death.wav')
        # self.death_sound.set_volume(Settings.effects_volume/100)
        self.map = self.get_map()
        self.pacman = self.get_pacman(self.map)
        self.ghosts = self.get_ghosts(self.map)
        self.play_death = False
        self.do_movement = False
        self.play_chomp = False
        self.play_intro = True

    def get_map(self):
        return Map()

    def get_pacman(self, map: Map):
        """These coordinates are some of the most disguisting code I've ever written
        places pacman at coordinate indicated on map"""
        return PacmanSprite(
            map.game_objects['pacman'][0][0] *
            map.tile_width, map.game_objects['pacman'][0][1]*map.tile_width,
            f'{self.img_path}yellow_pacman/',
            f'{self.img_path}pacman_death/',
        ).resize(map.tile_width, map.tile_height)

    def get_ghosts(self, map: Map):
        """These coordinates are some of the most disguisting code I've ever written
        places ghosts at coordinates indicated on map
        of course since it's horribly written, if there aren't 4 ghosts on the map,
        it will crash
        """
        ghosts = pygame.sprite.Group()
        blue_ghost = Ghost(
            map.game_objects['ghosts'][0][0]*map.tile_width,
            map.game_objects['ghosts'][0][1]*map.tile_width,
            f'{self.img_path}blue_ghost/')
        red_ghost = Ghost(
            map.game_objects['ghosts'][1][0]*map.tile_width,
            map.game_objects['ghosts'][1][1]*map.tile_width,
            f'{self.img_path}red_ghost/')
        orange_ghost = Ghost(
            map.game_objects['ghosts'][2][0]*map.tile_width,
            map.game_objects['ghosts'][2][1]*map.tile_width,
            f'{self.img_path}orange_ghost/')
        pink_ghost = Ghost(
            map.game_objects['ghosts'][3][0]*map.tile_width,
            map.game_objects['ghosts'][3][1]*map.tile_width,
            f'{self.img_path}pink_ghost/')

        ghosts.add(blue_ghost.resize(map.tile_width, map.tile_height))
        ghosts.add(red_ghost.resize(map.tile_width, map.tile_height))
        ghosts.add(orange_ghost.resize(map.tile_width, map.tile_height))
        ghosts.add(pink_ghost.resize(map.tile_width, map.tile_height))

        return ghosts

    # def do_event(self, event):
    #     if event.type == pygame.KEYDOWN:
    #         if event.key in (Settings.main_keybinding.escape, Settings.alternate_keybinding.escape):
    #             self.next_state = 'PAUSE'
    #             self.done = True

    def draw(self, screen) -> None:
        # self.screen.blit(self.background.image, (0, 0))
        screen.fill((0, 0, 0))
        self.map.draw(screen)
        self.pacman.draw(screen)
        self.ghosts.draw(screen)
        self.draw_scores(screen)
        # self.buttons.draw(self.screen)

    def update(self) -> None:
        if self.play_intro:
            self.music_player.load_play_music('music/pacman_beginning.wav', 1, True)
        if self.play_chomp:
            self.music_player.load_play_music('music/pacman_chomp.wav')
        if self.play_death:
            self.music_player.load_play_music('sounds/pacman_death.wav', 1, True)
        if self.do_movement:
            self.pacman.update(self.map)
            self.ghosts.update(self.map)
        

        self.update_map()
        self.check_object_collisions()
        self.check_win()

    def check_win(self):
        food = self.map.game_objects['food']
        capsules = self.map.game_objects['capsules']
        if food + capsules == []:
            self.pacman.allow_player_movement = False
            self.do_movement = False
            self.play_chomp = False
            self.music_player.load_play_music('sounds/pacman_intermission.wav', 1, True)

    def draw_scores(self, screen):
        font = pygame.font.Font('fonts/pacman_font.ttf', 20)
        score_font_render = font.render(f'SCORE: {self.score}', True, (255, 255, 255))
        score_font_rect = score_font_render.get_rect(center=(100, 10))
        screen.blit(score_font_render, score_font_rect)

        # self.buttons.update()

        # self.map.update(self.pacman, self.ghosts)
    def check_object_collisions(self):
        if self.map.is_colliding(self.pacman.rect.center, 'ghosts'):
            self.pacman.set_animation('death')
            self.pacman.movement = (0, 0)
            self.pacman.allow_player_movement = False
            self.play_chomp = False
            self.play_death = True
        elif self.map.is_colliding(self.pacman.rect.center, 'food'):
            self.map.delete_object(self.pacman.rect.center, 'food')
            self.score += 10
        elif self.map.is_colliding(self.pacman.rect.center, 'capsules'):
            self.map.delete_object(self.pacman.rect.center, 'capsules')
            self.do_ghosts_scared()
            self.score += 100

    def update_map(self):
        self.map.set_object_location_from_list(
            'pacman', [self.pacman.rect.center])
        self.map.set_object_location_from_list('ghosts', [
            ghost.rect.center for ghost in self.ghosts.sprites()])

    def do_ghosts_scared(self):
        for ghost in self.ghosts:
            ghost.scared = True

    def do_event(self, event):
        if event.type == MusicPlayer.SONG_END_EVENT:
            if self.music_player.currently_playing == 'music/pacman_beginning.wav':
                self.play_chomp = True
                self.do_movement = True
                self.play_intro = False
            elif self.music_player.currently_playing == 'sounds/pacman_death.wav':
                self.reset_positions()
            elif self.music_player.currently_playing == 'sounds/pacman_intermission.wav':
                self.create_game()

    def reset_positions(self):
        self.map.reset_positions()
        self.pacman = self.get_pacman(self.map)
        self.ghosts = self.get_ghosts(self.map)
        self.play_death = False
        self.play_intro = True
        self.pacman.allow_player_movement = True
        self.do_movement = False


def main() -> None:
    from main import main
    main('PACMAN')


if __name__ == '__main__':
    main()
