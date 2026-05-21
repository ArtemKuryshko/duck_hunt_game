import pygame
import random
from .base import BaseWeapon
from entities.effects.shotgun_explosion import ShotgunExplosion


class Shotgun(BaseWeapon):
    def __init__(self):
        super().__init__("Shotgun", 5, 2.0, 0.8, shot_animation=ShotgunExplosion)
        self.spread_radius = 30
        self.pellets_count = 5

    def shoot(self, mouse_pos: tuple, birds: list):
        if not self.can_shoot():
            return None

        self.current_ammo -= 1
        self.last_shot_time = pygame.time.get_ticks()

        pellet_hits = []
        for _ in range(self.pellets_count):
            offset_x = random.uniform(-self.spread_radius, self.spread_radius)
            offset_y = random.uniform(-self.spread_radius, self.spread_radius)
            hit_point = (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y)
            pellet_hits.append(hit_point)

        for bird in birds:
            if not bird.isAlive:
                continue

            hits_on_this_bird = 0
            for point in pellet_hits:
                if bird.rect.collidepoint(point):
                    hits_on_this_bird += 1

            if hits_on_this_bird > 0:
                bird.health -= hits_on_this_bird

        return self.shot_animation(pellet_hits)
