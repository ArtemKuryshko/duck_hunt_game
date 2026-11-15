import pygame
from abc import ABC, abstractmethod
from .base import BaseEffect


class Explosion(BaseEffect, ABC):
    def __init__(self, x, y, duration, size):
        super().__init__(x, y, duration)
        self.image = self.get_image()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))

    @abstractmethod
    def get_image(self) -> pygame.Surface:
        pass

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
            return

        # Simple fade out effect
        self.alpha = max(0, int((self.timer / self.max_duration) * 255))
        self.image.set_alpha(self.alpha)
