from .base import BaseBird
from typing import Dict, List
import pygame

class BadCrow(BaseBird):
    SPEED = 0.002
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__(x, y, animations, speed=self.SPEED)
        self.health = 1
        self.damage = 1
