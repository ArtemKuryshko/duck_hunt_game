import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from factories.duckFactory import DuckFactory
from entities.birds.base import BaseBird
from typing import List, Callable

class LevelManager:
    def __init__(self, score_system, on_bird_escape: Callable):
        self.score_system = score_system
        self.on_bird_escape = on_bird_escape
        self.birds: List[BaseBird] = []
        self.spawn_timer = 0
        self.spawn_interval = 2000 # 2 seconds

    def spawn_bird(self):
        x = random.randint(100, SCREEN_WIDTH - 200)
        y = SCREEN_HEIGHT
        duck_type = random.choice(["WhiteDuck", "GreenDuck", "BadCrow"])
        bird = DuckFactory.create_duck(duck_type, x, y)
        self.birds.append(bird)

    def update(self, dt: int):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_bird()
            self.spawn_timer = 0

        for bird in self.birds[:]:
            bird.update()
            
            # Check if bird is dead
            if not bird.isAlive:
                self.score_system.add_score(10)
                self.birds.remove(bird)
                continue

            # Check if bird flew off-screen
            if bird.y < -150:
                self.on_bird_escape()
                self.birds.remove(bird)

    def draw(self, screen: pygame.Surface):
        for bird in self.birds:
            screen.blit(bird.image, bird.rect)
