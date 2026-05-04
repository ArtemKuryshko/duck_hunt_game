from .base import BaseBird
from typing import Dict, List
import pygame

class WhiteDuck(BaseBird):
    SPEED = 0.002

    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__(x, y, animations, speed = self.SPEED)
        self.health = 1
        self.kill_points = 10