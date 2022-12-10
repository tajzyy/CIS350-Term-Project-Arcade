"""TODO: There's a bunch of TODO's already here if you wanna look"""
import sys
import random
import pygame
from player import StaticPlayer
from state import State
from settings import Settings
from sprite import Sprite


class Ball(StaticPlayer):
    """Handles all ball movements and scoring"""

    def __init__(self, x: int, y: int, img: pygame.Surface,
                 move_speed: int = 8,
                 color: pygame.Color = pygame.Color(0, 0, 0),
                 paddles: pygame.sprite.Group = None) -> None:
        """Initializes Ball"""
        super().__init__(x, y, img, move_speed, color)
        self.movement = (0, 0)
        self.paddles = paddles
        self.score_timer = pygame.time.get_ticks()
        self.score_sound = None
        self.active = False

    def do_movement(self) -> None:
        collision = self.get_collision()
        # https://www.geeksforgeeks.org/python-tuple-multiplication/
        self.movement = tuple(
            ele1 * ele2 for ele1, ele2 in zip(self.movement, collision)
        )

    def check_x_collision(self, players_hit):
        for p in players_hit:
            if p.side == 'left' and self.movement[0] < 0:
                return True
            if p.side == 'right' and self.movement[0] > 0:
                return True
        return False

    def check_y_collision(self, players_hit):
        if (self.rect.top <= 0
                or self.rect.bottom >= Settings.window_height):
            return True
        for p in players_hit:
            # hit bottom of player
            if (self.rect.bottom >= p.rect.top
                    and self.rect.bottom <= p.rect.bottom
                    and self.movement[1] > 0):
                return True
            # hit top of player
            if (self.rect.top <= p.rect.bottom
                    and self.rect.top >= p.rect.top
                    and self.movement[1] < 0):
                return True
        return False

    def get_collision(self):
        players_hit = pygame.sprite.spritecollide(
            self, self.paddles, False
        )
        x = -1 if self.check_x_collision(players_hit) else 1
        y = -1 if self.check_y_collision(players_hit) else 1
        if x == -1:
            y = 1
        return (x, y)

    def update(self) -> None:
        """Handles ball movements/collisions"""
        self.do_movement()
        self.update_score()
        super().update()

    def reset_ball(self) -> None:
        """Moves ball back to center and sends to random side"""
        self.score_timer = pygame.time.get_ticks()
        self.rect.center = (Settings.window_width//2,
                            Settings.window_height//2)
        self.movement = (0, 0)
        self.active = False
        # pygame.mixer.Sound.play(self.score_sound)
    
    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3
        if not self.active:
            if current_time - self.score_timer <= 700:
                countdown_number = 3

            elif current_time - self.score_timer <= 1400:
                countdown_number = 2
            
            elif current_time - self.score_timer <= 2100:
                countdown_number = 1
            
            elif current_time - self.score_timer >= 2100:
                self.movement = (self.move_speed * random.choice((-1, 1)),
                         self.move_speed * random.choice((-1, 1)))
                self.active = True
        
            font = pygame.font.Font('fonts/pacman_font.ttf', 20)
            time_counter_render = font.render(f'{countdown_number}', True, (255, 255, 255))
            time_counter_rect = time_counter_render.get_rect(center = (self.rect.centerx, self.rect.centery - 50))
            return time_counter_render, time_counter_rect
        return None, None
        

    def update_score(self) -> None:
        """updates player score and resets ball to middle"""
        # scoring
        for p in self.paddles:
            if self.rect.left <= 0 and p.side == 'right':
                self.reset_ball()
                p.score += 1
            elif (self.rect.right >= Settings.window_width
                    and p.side == 'left'):
                self.reset_ball()
                p.score += 1

class Paddle(StaticPlayer):
    """Controls all player movements"""

    def __init__(self, x: int, y: int, img: pygame.Surface, side: str,
                 move_speed: int = 5,
                 color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        """Initializes Player"""
        super().__init__(x, y, img, move_speed, color)
        self.score = 0
        self.side = side

    def get_direction(self, balls) -> str:
        return super().get_direction()

    def do_movement(self, balls) -> None:
        movements = {
            'stop': (0, 0),
            'up': (0, -self.move_speed),
            'down': (0, self.move_speed),
            'left': (0, 0),
            'right': (0, 0),
        }
        direction = self.get_direction(balls)
        if direction is None:
            direction = 'stop'
        self.movement = movements[direction]

    def update(self, balls) -> None:
        """Moves the player"""
        self.do_movement(balls)
        super().update()


class Opponent(Paddle):
    """AI for pong"""

    def __init__(self, x: int, y: int, img: pygame.Surface, side: str,
                 move_speed: int = 5, color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(x, y, img, side, move_speed, color)

    def get_direction(self, balls) -> str:
        first_ball = balls.sprites()[0]
        if self.rect.top < first_ball.rect.y:
            return 'down'
        if self.rect.bottom > first_ball.rect.y:
            return 'up'
        return 'stop'


class Pong(State):
    def __init__(self, music_player):
        super().__init__()

        # initialize pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # create game objects
        self.img_path = 'images/pong/'
        self.global_img_path = 'images/'
        self.clock = pygame.time.Clock()
        self.music_player = music_player
        pygame.display.set_caption('Pong')
        pygame.display.set_icon(pygame.image.load(
            f'{self.global_img_path}main.png'))
        self.create_game()

    def create_game(self):
        self.paddles = self.get_paddles()
        self.balls = self.get_balls()
        self.goal_score = 10

    def get_paddles(self) -> pygame.sprite.Group:
        paddle_img = pygame.image.load(f'{self.img_path}paddle.png')
        paddles = pygame.sprite.Group()
        paddles.add(Paddle(40, Settings.window_height//2,
                    paddle_img, 'left', color=(255, 255, 255)).resize(20, 120))
        paddles.add(Opponent(Settings.window_width - 40,
                    Settings.window_height//2, paddle_img, 'right', color=(255, 255, 255)).resize(20, 120))
        return paddles

    def get_balls(self) -> pygame.sprite.Group:
        ball_img = pygame.image.load(f'{self.img_path}ball1.png')
        balls = pygame.sprite.Group()
        balls.add(
            Ball(
                Settings.window_width//2,
                Settings.window_height//2,
                ball_img, color=(255, 255, 255), paddles=self.paddles
            ).resize(40, 40))
        return balls

    def draw_scores(self, screen) -> None:
        left_paddle = None
        right_paddle = None
        for p in self.paddles.sprites():
            if p.side == 'left':
                left_paddle = p
            elif p.side == 'right':
                right_paddle = p

        font = pygame.font.Font(f'fonts/pacman_font.ttf', 30)
        left_score_render = font.render(f'{left_paddle.score}', True, Settings.light_grey)
        right_score_render = font.render(f'{right_paddle.score}', True, Settings.light_grey)

        left_score_rect = left_score_render.get_rect(center=(200, 50))
        right_score_rect = right_score_render.get_rect(center=(600, 50))

        screen.blit(left_score_render, left_score_rect)
        screen.blit(right_score_render, right_score_rect)

    def update_scores(self, screen) -> None:
        if (win := self.check_win()) is not None:
            self.win_game(win, screen)

    def win_game(self, winner, screen):
        pause_font = pygame.font.Font(None, 150)
        p_num = 1 if winner.side == 'left' else 2
        win_text = pause_font.render(
            f'Player {p_num} wins!', False, 'grey67'
        )
        screen.blit(win_text, (0, Settings.window_height//2))

    def check_win(self) -> Paddle:
        for p in self.paddles:
            if p.score >= self.goal_score:
                return p
        return None

    def draw(self, screen) -> None:
        screen.fill((0, 0, 0))
        self.draw_line(screen)
        self.paddles.draw(screen)
        self.balls.draw(screen)
        self.draw_scores(screen)
        self.update_scores(screen)
        self.draw_timer(screen)
    
    def draw_timer(self, screen):
        for b in self.balls:
            timer_render, timer_rect = b.restart_counter()
            if timer_render is None or timer_rect is None:
                continue
            screen.blit(timer_render, timer_rect)

    def draw_line(self, screen):
        pygame.draw.aaline(
            screen,
            (255, 255, 255),
            (Settings.window_width//2, 0),
            (Settings.window_width//2, Settings.window_height)
        )

    def update(self) -> None:
        self.music_player.load_play_music('music/runescape_dream.wav')
        self.paddles.update(self.balls)
        self.balls.update()
        self.check_win()
    
    # def reset_ball(self):
    #     self.current_time = self.clock.tick()
    #     for b in self.balls:
    #         b.reset_ball()
        
    #     if 
    #         self.movement = (self.move_speed * random.choice((-1, 1)),
    #                      self.move_speed * random.choice((-1, 1)))


def main() -> None:
    """Main function"""
    from main import main
    main('PONG')


if __name__ == "__main__":
    main()
