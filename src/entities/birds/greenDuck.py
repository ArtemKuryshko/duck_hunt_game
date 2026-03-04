from .base import BaseBird
from typing import Dict, List
import pygame
class GreenDuck(BaseBird):
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__(x, y, animations)

        self.health = 2
        self.speed = 1
        
    def move(self):
        pass
    def animate(self):
        pass