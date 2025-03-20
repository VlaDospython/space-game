from src.constants import *
import pygame
from src.image_strategy.Strategy import Strategy


class SimpleImage(Strategy):
    def __init__(self, size: tuple, color: tuple):
        self.image = pygame.Surface(size)
        self.image.fill(color)

    def get_surface(self):
        return self.image
