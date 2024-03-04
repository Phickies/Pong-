import pygame
import math


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
        self.vx = -9
        self.vy = 3

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

    def bounce_off(self, player):
        if self.top >= player.top and self.bottom <= player.bottom:
            if (self.left <= player.right and self.vx < 0) and self.right > player.right:
                self.vx *= -1
            if (self.right >= player.left and self.vx > 0) and self.left < player.left:
                self.vx *= -1

    def collide(self, line_border_x):
        return (self.left <= line_border_x) and (self.right >= line_border_x)

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
