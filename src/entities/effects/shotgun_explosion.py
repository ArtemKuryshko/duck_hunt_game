import random
import pygame
from .default_explosion import DefaultExplosion
from .base import BaseEffect


class ShotgunExplosion(BaseEffect):
    def __init__(self, hit_points):
        # Start at the average position or first point
        if not hit_points:
            super().__init__(0, 0, 0)
            self.kill()
            return

        avg_x = sum(p[0] for p in hit_points) / len(hit_points)
        avg_y = sum(p[1] for p in hit_points) / len(hit_points)

        # Duration should be long enough to spawn all pellets
        super().__init__(avg_x, avg_y, duration=300)

        self.hit_points = hit_points
        self.current_idx = 0

        # This sprite itself is invisible, it just manages the sub-explosions
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(avg_x, avg_y))

    def update(self, dt):
        self.timer -= dt

        # Sequential spawning logic
        if self.current_idx < len(self.hit_points):
            x, y = self.hit_points[self.current_idx]

            # Randomized size for each pellet hit
            size = random.randint(25, 45)
            explosion = DefaultExplosion(x, y, size=size)

            # Add the new explosion to all groups this manager belongs to
            if self.groups():
                for group in self.groups():
                    group.add(explosion)

            self.current_idx += 1

        # Kill the manager when all pellets are spawned and its timer is out
        if self.current_idx >= len(self.hit_points) and self.timer <= 0:
            self.kill()
