from abc import ABC, abstractmethod
from typing import Dict, List
import pygame

class BaseBird(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]]):
        super().__init__()

        self.animations = animations

        self.current_direction = "Up"
        self.current_frame = 0

        self.x = x
        self.y = y

        self.health = 0
        self.speed = 0

        self.image = self.animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.isAlive = True

    def get_damage(self, damage: int):
        self.health -= damage

        if self.health <= 0:
            self.isAlive = False

    def animate(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def update(self):
        if(self.isAlive):
            self.animate()
            self.move()
            

    

