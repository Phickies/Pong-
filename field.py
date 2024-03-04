import pygame


class Field(pygame.Rect):

    color = (255, 255, 255)

    def __init__(self, top_left_x, top_left_y, width, height):
        super().__init__(top_left_x, top_left_y, width, height)

    def display(self, window_screen):
        pygame.draw.rect(window_screen, self.color, self, 1)
        # Draw a line divide side
        for i in range(self.top, self.bottom, 20):
            pygame.draw.line(window_screen, self.color, (self.centerx, i), (self.centerx, i+10), 1)

