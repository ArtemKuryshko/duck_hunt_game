from .base import BaseBird
from typing import Dict, List
import pygame

class GreenDuck(BaseBird):
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__(x, y, animations)
        self.health = 2
        self.speed = 1
        self.current_direction = "Up"
        
    def move(self):
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def animate(self):
        frames = self.animations.get(self.current_direction, [])
        if frames:
            self.current_frame = (self.current_frame + 1) % (len(frames) * 10)
            self.image = frames[self.current_frame // 10]
