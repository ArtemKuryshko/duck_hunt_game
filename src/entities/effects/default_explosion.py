import pygame
from .explosion import Explosion


class DefaultExplosion(Explosion):
    def __init__(self, x, y, size=80):
        super().__init__(x, y, 450, size)

    def get_image(self):
        from config import EXPLOSION_PATH
        return pygame.image.load(EXPLOSION_PATH).convert_alpha()
