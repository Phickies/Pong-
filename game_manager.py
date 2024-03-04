import pygame
import sys

from field import Field
from text import Text
from player import Player
from ball import Ball


def map_value(value, from_low, from_high, to_low, to_high):
    """
    Map a value from one range to another.

    :param value: The value to be mapped.
    :param from_low: The minimum value of the original range.
    :param from_high: The maximum value of the original range.
    :param to_low: The minimum value of the target range.
    :param to_high: The maximum value of the target range.
    :return: The mapped value.
    """
    from_range = from_high - from_low
    to_range = to_high - to_low

    scaled_value = float(value - from_low) / float(from_range)

    return to_low + (scaled_value * to_range)


class GameManager:

    # Setup max score
    mx_score = 5

    # Setup background color
    background_color = (0, 0, 0)  # Black

    # Setup delay start time in millisecond
    delay_start_time = 4000
    delay_prepare_time = 1000
    delay_between = 1000
    time_since_start = 0
    time_since_prepare = 0

    # Setup ball holder position
    start_right = (715, 247)
    start_left = (75, 247)

    # Setup game state
    game_over = False

    def __init__(self, window_size):
        # Initialize Pygame
        pygame.init()

        # Setup caption
        pygame.display.set_caption("Pong")

        # Setup window
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)

        # Setup player and initiations
        self.ball = Ball(self.window_size[0]/2, self.window_size[1]/2, 10)
        self.field = Field(50, 54, 800-100, 500-100)
        self.player_1 = Player(65, 252, 10, 60)
        self.player_2 = Player(800-65, 252, 10, 60)
        self.ig_text = Text()

        self.start_time = pygame.time.get_ticks()
        self.prepare_time = pygame.time.get_ticks()

    def display(self):

        # Display background
        self.screen.fill(self.background_color)

        # Display countdown timer
        if (self.time_since_start > 1000) and (self.time_since_start < self.delay_start_time):
            counter = 4 - int(self.time_since_start / 1000)
            self.ig_text.display(self.ig_text, f"{counter}", self.screen,
                                 175, 120, 200, (50, 50, 50))
            self.ig_text.display(self.ig_text, f"{counter}", self.screen,
                                 520, 120, 200, (50, 50, 50))

        # Display game over texts
        if self.game_over:
            self.ig_text.display(self.ig_text, f"GAME OVER", self.screen,
                                 110, 120, 100, (200, 200, 200))
            self.ig_text.display(self.ig_text, f"press SPACE to restart", self.screen,
                                 280, 300, 20, (0, 255, 255))
            if self.player_1.max_score(self.mx_score):
                self.ig_text.display(self.ig_text, "You Stonk", self.screen,
                                     150, 10, 30, (0, 200, 20))
            else:
                self.ig_text.display(self.ig_text, "You Stink", self.screen,
                                     150, 10, 30, (200, 0, 0))
            if self.player_2.max_score(self.mx_score):
                self.ig_text.display(self.ig_text, "You Stonk", self.screen,
                                     505, 10, 30, (0, 200, 20))
            else:
                self.ig_text.display(self.ig_text, "You Stink", self.screen,
                                     505, 10, 30, (200, 0, 0))

        # Display player score
        self.ig_text.display(self.ig_text, f"{self.player_1.score}", self.screen,
                             330, 5, 40, (255, 255, 255))
        self.ig_text.display(self.ig_text, f"{self.player_2.score}", self.screen,
                             450, 5, 40, (255, 255, 255))

        # Display objects
        self.ball.display(self.screen)
        self.field.display(self.screen)
        self.player_1.display(self.screen)
        self.player_2.display(self.screen)

        # Update display
        pygame.display.flip()

    def update(self):

        # Update game state
        if self.player_1.max_score(self.mx_score) or self.player_2.max_score(self.mx_score):
            self.game_over = True

        if not self.game_over:

            # Restrict controlling
            self.player_1.bounce_in(self.field)
            self.player_2.bounce_in(self.field)
            self.ball.bounce_in(self.field)

            # Update time
            current_time = pygame.time.get_ticks()
            self.time_since_start = current_time - self.start_time
            self.time_since_prepare = current_time - self.prepare_time

            if (self.time_since_start >= self.delay_start_time and self.time_since_prepare >= self.delay_prepare_time and
                    not self.player_1.is_reset and not self.player_2.is_reset and not self.ball.is_reset):
                self.ball.translate()
                self.ball.bounce_off(self.player_1)
                self.ball.bounce_off(self.player_2)

                # Update player 1 score
                if self.ball.collide(self.field.right):
                    self.player_1.add_score(1)
                    pygame.time.delay(self.delay_between)
                    self.player_1.is_reset = True
                    self.player_2.is_reset = True
                    self.ball.set_reset_position_to(self.start_right)

                # Update player 2 score
                elif self.ball.collide(self.field.left):
                    self.player_2.add_score(1)
                    pygame.time.delay(self.delay_between)
                    self.player_1.is_reset = True
                    self.player_2.is_reset = True
                    self.ball.set_reset_position_to(self.start_left)

            if self.player_1.is_reset or self.player_2.is_reset or self.ball.is_reset:
                # Play reset animation
                self.player_1.reset_position_animation()
                self.player_2.reset_position_animation()
                self.ball.reset_position_animation()
                # Reset prepare time
                self.prepare_time = pygame.time.get_ticks()

        pygame.time.Clock().tick(60)

    def event_handle(self):

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        # Key pressed Event handling
        keys = pygame.key.get_pressed()

        # Restart game
        if self.game_over:
            if keys[pygame.K_SPACE]:
                self.game_over = False
                self.start_time = pygame.time.get_ticks()
                self.player_1.reset_score()
                self.player_2.reset_score()
                self.player_1.is_reset = True
                self.player_2.is_reset = True
                self.ball.set_reset_position_to((self.window_size[0] / 2 - 5, self.window_size[1] / 2))

        # Player 1 key movement
        if keys[pygame.K_w]:
            self.player_1.move_ip(0, -self.player_1.speed)
        elif keys[pygame.K_s]:
            self.player_1.move_ip(0, self.player_1.speed)

        # Player 2 key movement
        if keys[pygame.K_UP]:
            self.player_2.move_ip(0, -self.player_1.speed)
        elif keys[pygame.K_DOWN]:
            self.player_2.move_ip(0, self.player_1.speed)
