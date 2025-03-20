from src.constants import *
import pygame
from src.image_strategy.Strategy import Strategy

class PhotoImage(Strategy):
    def __init__(self, player_image):
        self.image = pygame.transform.scale(player_image, (36, 42))
        self.image.set_colorkey(BLACK)

    def get_surface(self):
        return self.image
