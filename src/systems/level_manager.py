import pygame
import random
from typing import Callable, List

from config import SCREEN_HEIGHT, SCREEN_WIDTH
from factories.duckFactory import DuckFactory
from entities.birds.base import BaseBird
from systems.settings_manager import SettingsManager


class LevelManager:
    def __init__(
        self,
        score_system,
        on_bird_escape: Callable,
        settings_manager: SettingsManager | None = None,
        difficulty: str | None = None,
    ):
        self.score_system = score_system
        self.on_bird_escape = on_bird_escape
        self.birds: List[BaseBird] = []
        self.spawn_timer = 0
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            manager = settings_manager or SettingsManager()
            self.difficulty = manager.difficulty
        self.spawn_rate = {"easy": 2000, "medium": 1500, "hard": 1000}
        self.spawn_interval = self.spawn_rate[self.difficulty]

    def spawn_bird(self):
        x = random.choice([-50, SCREEN_WIDTH + 50])
        y = random.randint(50, 450)
        duck_type = random.choices(["WhiteDuck", "GreenDuck", "BadCrow"], weights=[0.5, 0.4, 0.1])[0]
        bird = DuckFactory.create_duck(duck_type, x, y)
        self.birds.append(bird)

    def update(self, dt: int):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_bird()
            self.spawn_timer = 0

        new_effects = []
        for bird in self.birds[:]:
            effect = bird.update(dt)
            if effect:
                new_effects.append(effect)

            if not bird.isAlive:
                if bird.was_shot:
                    if not bird.points_handled:
                        if bird.damage == 0:
                            self.score_system.add_score(bird.kill_points)
                        else:
                            self.score_system.deduct_health(damage = bird.damage)
                        bird.points_handled = True
                    
                    if bird.damage > 0:
                        if bird in self.birds:
                            self.birds.remove(bird)
                        continue
                            
                    if bird.y >= SCREEN_HEIGHT - 200:
                        if bird in self.birds:
                            self.birds.remove(bird)
                else:
                    if not bird.points_handled:
                        if bird.damage > 0:
                            self.score_system.deduct_health(damage = bird.damage)
                        bird.points_handled = True
                    if bird in self.birds:
                        self.birds.remove(bird)
                continue

            OFFSCREEN_MARGIN = 50

            if (bird.x < -OFFSCREEN_MARGIN or bird.x > SCREEN_WIDTH + OFFSCREEN_MARGIN or bird.y < -OFFSCREEN_MARGIN or bird.y > SCREEN_HEIGHT + OFFSCREEN_MARGIN):
                if bird.damage == 0:
                    self.on_bird_escape()
                if bird in self.birds:
                    self.birds.remove(bird)
        
        return new_effects


    def draw(self, screen: pygame.Surface):
        for bird in self.birds:
            screen.blit(bird.image, bird.rect)
