import pygame
from settings import Settings


class MusicPlayer:
    SONG_END_EVENT = pygame.USEREVENT + 1
    def __init__(self):
        self.currently_playing = None

    def load_play_music(self, music_path, num_loops=-1, sound=False):
        if self.currently_playing != music_path:
            self.currently_playing = music_path
            pygame.mixer_music.load(music_path)
            if sound:
                pygame.mixer_music.set_volume(Settings.effects_volume/100)
            else:
                pygame.mixer_music.set_volume(Settings.music_volume/100)
            pygame.mixer_music.play(num_loops)
            pygame.mixer_music.set_endevent(MusicPlayer.SONG_END_EVENT)
    
    # def load_play_sound(self, sound_path):
    #     if self.current_sound != sound_path:
    #         self.current_sound = sound_path
    #         temp = pygame.mixer.Sound(sound_path)
    #         temp.set_volume(Settings.effects_volume/100)
    #         temp.play()
    #         pygame.mixer.set_endevent(MusicPlayer.SONG_END_EVENT)
            

    @staticmethod
    def pause():
        pygame.mixer_music.pause()

    @staticmethod
    def resume():
        pygame.mixer_music.play(-1)
    
    # @staticmethod
    # def get_end_event():
    #     return pygame.mixer_music.get_endevent()
