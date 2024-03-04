import pygame
import math


class Player(pygame.Rect):

    color = (255, 255, 255)
    speed = 5
    score = 0
    is_reset = False

    def __init__(self, position_x, position_y, height, width):
        super().__init__(position_x, position_y, height, width)
        self.centerx = position_x
        self.centery = position_y
        self.init_pos_y = self.centery

    def display(self, window_screen):
        pygame.draw.rect(window_screen, self.color, self)

    def bounce_in(self, field):
        buffer = 5
        if self.top <= field.top:
            self.top = field.top + buffer
        if self.bottom >= field.bottom:
            self.bottom = field.bottom - buffer

    def add_score(self, number):
        self.score += number

    def max_score(self, number):
        return self.score >= number

    def reset_position_animation(self):
        threshold = 2.0  # A small threshold for equality checks
        if abs(self.centery - self.init_pos_y) > threshold:
            vector_y = self.init_pos_y - self.centery
            normalized = vector_y / math.sqrt(pow(vector_y, 2))
            if abs(vector_y) > 10:
                normalized *= 10
            self.move_ip(0, normalized)
        else:
            self.is_reset = False

    def reset_score(self):
        self.score = 0
