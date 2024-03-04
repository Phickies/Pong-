import pygame


class Text:

    def __init__(self):
        pass

    @staticmethod
    def display(self, content, window_screen, position_x, position_y, size, color: tuple):
        text = pygame.font.Font("data/PixeloidSans-mLxMm.ttf", size).render(content, False, color)
        window_screen.blit(text, (position_x, position_y))

