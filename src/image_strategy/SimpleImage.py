from src.constants import *
import pygame
from src.image_strategy.Strategy import Strategy


class SimpleImage(Strategy):
    def __init__(self):
        self.image = pygame.Surface((25, 40))
        self.image.fill(RED)

    def get_surface(self):
        return self.image
