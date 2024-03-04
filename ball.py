import random
import pygame
import math


def random_vx(unsigned: bool = None):
    """
    Return random number assigned for velocity x
    :param unsigned: True only return unsigned, False only return signed, default both
    :return: random value for velocity x
    """
    if unsigned is not None:
        if unsigned:
            return random.uniform(8, 11)
        else:
            return random.uniform(-11, -8)
    else:
        return random.choice([8, -8])


def random_vy(unsigned: bool = None):
    """
    Return random number assigned for velocity y
    :param unsigned: True only return unsigned, False only return signed, default both
    :return: random value for velocity y
    """
    if unsigned is not None:
        if unsigned:
            return random.uniform(2, 5)
        else:
            return random.uniform(-2, -5)
    else:
        return random.choice([2, 3, 4, 5, -2, -3, -4, -5])


class Ball(pygame.Rect):

    color = (255, 0, 0)
    is_reset = False

    def __init__(self, position_x, position_y, size):
        super().__init__(position_x, position_y, size, size)
        self.centerx = position_x
        self.centery = position_y
        self.init_pos_x = self.centerx
        self.init_pos_y = self.centery
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.vx = random.choice([-9, 9])
        self.vy = 0

    def set_start_velocity(self):
        self.vx = random.choice([-9, 9])
        self.vy = 0

    def display(self, window_screen):
        pygame.draw.rect(window_screen, self.color, self)

    def translate(self):
        self.move_ip(self.vx, self.vy)

    def bounce_in(self, field):
        if self.left <= field.left and self.vx < 0:
            self.vx *= -1
        if self.right >= field.right and self.vx > 0:
            self.vx *= -1
        if self.top <= field.top and self.vy < 0:
            self.vy *= -1
        if self.bottom >= field.bottom and self.vy > 0:
            self.vy *= -1

    def restrict_velocity(self):
        if self.vx < -11:
            self.vx = random_vx(False)
        elif self.vx > 11:
            self.vx = random_vx(True)
        if self.vy < -6:
            self.vy = random_vy(False)
        elif self.vy > 6:
            self.vy = random_vy(True)

    def bounce_off(self, player):
        if self.top >= player.top and self.bottom <= player.bottom:
            if (self.left <= player.right and self.vx < 0) and self.right > player.right:
                self.vx *= -1
                self.vx *= random.uniform(1, 1.5)
                self.vy = random_vy()
                self.vy *= random.uniform(1, 1.5)
            if (self.right >= player.left and self.vx > 0) and self.left < player.left:
                self.vx *= -1
                self.vx *= random.uniform(1, 1.5)
                self.vy = random_vy()
                self.vy *= random.uniform(1, 1.5)

    def collide(self, line_border_x):
        return (self.left <= line_border_x) and (self.right >= line_border_x)

    def reset_velocity(self, unsigned_x: bool = None, unsigned_y: bool = None):
        self.vx = random_vx(unsigned_x)
        self.vy = random_vy(unsigned_y)

    def set_reset_position_to(self, position: tuple):
        self.init_pos_x = position[0]
        self.init_pos_y = position[1]
        self.is_reset = True

    def reset_position_animation(self):
        threshold = 2.0  # A small threshold for equality checks
        if abs(self.x - self.init_pos_x) > threshold or abs(self.y - self.init_pos_y) > threshold:
            vector_x = self.init_pos_x - self.x
            vector_y = self.init_pos_y - self.y
            normalized_x = vector_x / math.sqrt(pow(vector_x, 2) + pow(vector_y, 2))
            normalized_y = vector_y / math.sqrt(pow(vector_x, 2) + pow(vector_y, 2))
            steer_x = normalized_x * 4
            steer_y = normalized_y * 4
            self.move_ip(steer_x, steer_y)
        else:
            self.is_reset = False
