import pygame
from abc import ABC, abstractmethod

class BaseEffect(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, duration):
        super().__init__()
        self.timer = duration
        self.max_duration = duration
        self.alpha = 255

    @abstractmethod
    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
