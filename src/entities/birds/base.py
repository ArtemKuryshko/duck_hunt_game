from abc import ABC
from typing import Dict, List
import pygame
from systems.trajectory_creator import BirdTrajectory
from entities.effects.default_explosion import DefaultExplosion


class BaseBird(pygame.sprite.Sprite, ABC):
    def __init__(self, x: int, y: int, animations: Dict[str, List[pygame.Surface]], speed: float):
        super().__init__()

        self.animations = animations
        self.current_frame = 0
        self.current_direction = "Side"  # перший дефолтний ключ

        self.x = x
        self.y = y

        self.health = 0
        self.damage = 0
        self.kill_points = 0
        self.isAlive = True
        self.was_shot = False
        self.points_handled = False
        self.flipped = False  # чи летить ліворуч
        self.down = False

        self.image = self.animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))

        self.speed = speed
        self.trajectory = BirdTrajectory(
            speed=self.speed,
            spawn_point=(self.x, self.y),
        )
        self.x, self.y = self.trajectory.get_position()

    def get_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0 and self.isAlive:
            self.isAlive = False
            self.was_shot = True
            self.current_frame = 0

    def move(self):
        self.trajectory.update()
        self.x, self.y = self.trajectory.get_position()
        self.rect.center = (int(self.x), int(self.y))

    def _get_direction_from_angle(self, angle: float) -> tuple[str, bool]:
        abs_angle = abs(angle)

        # Вертикальний рух — "Up"
        if 67.5 <= abs_angle <= 112.5:
            return "Up", angle < 0, False  # від'ємний кут = вниз, але спрайт той самий

        # Діагональний рух — "Diagonal"
        if 20.5 < abs_angle < 69.5 or 110.5 < abs_angle < 159.5:
            flipped = angle > 90 or angle < -90  # летить ліворуч
            down = angle < -20.5  # від'ємний кут = вниз
            return "Diagonal", flipped, down

        # Горизонтальний рух — "Side"
        flipped = abs_angle > 90  # летить ліворуч
        return "Side", flipped, False

    def animate(self):
        if self.damage == 0 and self.was_shot:
            frames = self.animations.get("Dead", [])
            if frames:
                frame_idx = min(self.current_frame // 10, len(frames) - 1)
                self.image = frames[frame_idx]
                self.current_frame += 1
                self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            return
        angle = self.trajectory.get_rotation_angle()
        new_direction, self.flipped, self.down = self._get_direction_from_angle(angle)
        self.current_direction = new_direction

        frames = self.animations.get(self.current_direction, [])
        if not frames:
            return

        self.current_frame = (self.current_frame + 1) % (len(frames) * 10)
        frame_image = frames[self.current_frame // 10]

        if self.flipped:
            frame_image = pygame.transform.flip(frame_image, True, False)

        if self.down:
            frame_image = pygame.transform.rotate(frame_image, 90 if self.flipped else -90)

        self.image = frame_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt: int):
        if self.health <= 0 and self.isAlive:
            self.isAlive = False
            self.was_shot = True
            self.current_frame = 0

        if self.isAlive:
            self.animate()
            self.move()
        elif self.was_shot and self.damage == 0:
            self.animate()
            # Падіння вниз при влучанні
            self.y += 0.4 * dt
            self.rect.center = (int(self.x), int(self.y))
        elif self.was_shot and self.damage > 0:
            return DefaultExplosion(self.x, self.y, size=400)
