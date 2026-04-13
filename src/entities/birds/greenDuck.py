from .base import BaseBird
from typing import Dict, List
import pygame

class GreenDuck(BaseBird):
    SPEED = 0.0035
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__(x, y, animations, speed=self.SPEED)
        self.health = 2
        self.kill_points = 30

    
