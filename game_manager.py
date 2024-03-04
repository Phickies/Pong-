import pygame
import sys

from field import Field
from text import Text
from player import Player
from ball import Ball

# Set up color
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 10)
light_grey = (180, 180, 180)
cyan = (50, 250, 250)


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
    game_running = False

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

        self.start_button_color = yellow
        self.connect_button_color = light_grey
        self.background_color = black

        self.start_time = pygame.time.get_ticks()
        self.prepare_time = pygame.time.get_ticks()

    def display_start_menu(self):
        self.ig_text.display(self.ig_text, "PONG", self.screen,
                             268, 100, 100, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (360, 280, 90, 30))
        self.ig_text.display(self.ig_text, "Start", self.screen,
                             360, 280, 30, self.start_button_color)
        pygame.draw.rect(self.screen, (0, 0, 0), (268, 340, 260, 20))
        self.ig_text.display(self.ig_text, "Connect to TOUCH PATCH", self.screen,
                             268, 340, 20, self.connect_button_color)

    def display_game_play(self):
        # Display countdown timer
        if self.counting_down():
            self.display_countdown()

        # Display game over texts
        if self.game_over:
            self.display_game_over_text()

        # Display player score
        self.display_player_score()

        # Display objects
        self.ball.display(self.screen)
        self.field.display(self.screen)
        self.player_1.display(self.screen)
        self.player_2.display(self.screen)

    def display_player_score(self):
        self.ig_text.display(self.ig_text, f"{self.player_1.score}", self.screen,
                             330, 5, 40, (255, 255, 255))
        self.ig_text.display(self.ig_text, f"{self.player_2.score}", self.screen,
                             450, 5, 40, (255, 255, 255))

    def display_countdown(self):
        counter = 4 - int(self.time_since_start / 1000)
        self.ig_text.display(self.ig_text, f"{counter}", self.screen,
                             175, 120, 200, (50, 50, 50))
        self.ig_text.display(self.ig_text, f"{counter}", self.screen,
                             520, 120, 200, (50, 50, 50))

    def display_game_over_text(self):
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

    def update_counting_time(self):
        current_time = pygame.time.get_ticks()
        self.time_since_start = current_time - self.start_time
        self.time_since_prepare = current_time - self.prepare_time

    def update_max_score(self):
        if self.player_1.max_score(self.mx_score-1) and self.player_2.max_score(self.mx_score-1):
            self.mx_score += 1

    def reaching_max_score(self):
        return self.player_1.max_score(self.mx_score) or self.player_2.max_score(self.mx_score)

    def counting_down(self):
        return (self.time_since_start > 1000) and (self.time_since_start < self.delay_start_time)

    def is_done_counting(self):
        return (self.time_since_start >= self.delay_start_time) and (self.time_since_prepare >= self.delay_prepare_time)

    def is_done_reset(self):
        return not self.player_1.is_reset and not self.player_2.is_reset and not self.ball.is_reset

    def is_reset(self):
        return self.player_1.is_reset or self.player_2.is_reset or self.ball.is_reset

    def ball_move(self):
        self.ball.translate()
        self.ball.bounce_off(self.player_1)
        self.ball.bounce_off(self.player_2)
        self.ball.restrict_velocity()

    def update_player_score_left(self):
        self.player_1.add_score(1)
        pygame.time.delay(self.delay_between)
        self.player_1.is_reset = True
        self.player_2.is_reset = True
        self.ball.set_reset_position_to(self.start_right)
        self.ball.reset_velocity(False)

    def update_player_score_right(self):
        self.player_2.add_score(1)
        pygame.time.delay(self.delay_between)
        self.player_1.is_reset = True
        self.player_2.is_reset = True
        self.ball.set_reset_position_to(self.start_left)
        self.ball.reset_velocity(True)

    def play_reset_position_animation(self):
        # Play reset animation
        self.player_1.reset_position_animation()
        self.player_2.reset_position_animation()
        self.ball.reset_position_animation()
        # Reset prepare time
        self.prepare_time = pygame.time.get_ticks()

    def restart_game(self):
        self.game_over = False
        self.mx_score = 5
        self.start_time = pygame.time.get_ticks()
        self.player_1.reset_score()
        self.player_2.reset_score()
        self.player_1.is_reset = True
        self.player_2.is_reset = True
        self.ball.set_reset_position_to((self.window_size[0] / 2 - 5, self.window_size[1] / 2))
        self.ball.set_start_velocity()

    def establish_connection_to_touch_patch(self):
        pass

    def display(self):

        # Display background
        self.screen.fill(self.background_color)

        if not self.game_running:
            self.display_start_menu()
        else:
            self.display_game_play()

        # Update display
        pygame.display.flip()

    def update(self):

        # Update game_over state
        self.update_max_score()
        if self.reaching_max_score():
            self.game_over = True

        # Check is game is over and is game is still running
        if not self.game_over and self.game_running:

            # Restrict controlling
            self.player_1.bounce_in(self.field)
            self.player_2.bounce_in(self.field)
            self.ball.bounce_in(self.field)

            # Update time
            self.update_counting_time()

            if self.is_done_counting() and self.is_done_reset():

                self.ball_move()

                # Update player 1 score
                if self.ball.collide(self.field.right):
                    self.update_player_score_left()

                # Update player 2 score
                elif self.ball.collide(self.field.left):
                    self.update_player_score_right()

            if self.is_reset():
                self.play_reset_position_animation()

        pygame.time.Clock().tick(60)

    def event_handle(self):

        # Key pressed Event handling
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            # Mouse press handling
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_running:
                if 360 <= event.pos[0] <= 450 and 280 <= event.pos[1] <= 310:
                    # Checking if click Start button
                    self.game_running = True
                    self.start_time = pygame.time.get_ticks()
                    self.prepare_time = pygame.time.get_ticks()
                if 268 <= event.pos[0] <= 528 and 340 <= event.pos[1] <= 360:
                    # Checking if click Connect to touch patch button
                    self.establish_connection_to_touch_patch()
                    print("Trying to connect to the touch patch")

        # Mouse hover handling
        mouse = pygame.mouse.get_pos()
        if 360 <= mouse[0] <= 450 and 280 <= mouse[1] <= 310 and not self.game_running:
            self.start_button_color = cyan
        else:
            self.start_button_color = yellow
        if 268 <= mouse[0] <= 528 and 340 <= mouse[1] <= 360 and not self.game_running:
            self.connect_button_color = white
        else:
            self.connect_button_color = light_grey

        # Restart game
        if self.game_over and self.game_running:
            if keys[pygame.K_SPACE]:
                self.restart_game()

        # Control movement of the player
        if not self.game_over and self.game_running:
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

    def run_loop(self):
        self.event_handle()
        self.update()
        self.display()
