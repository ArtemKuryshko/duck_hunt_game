
from .base import BaseWeapon
import pygame
import random

class Pistol(BaseWeapon):
    def __init__(self):
        super().__init__("Pistol", 8, 1.0, 0.5)

    def shoot(self, mouse_pos: tuple, birds: list):
        if super().shoot(mouse_pos, birds):
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 1
                    break
            return True
        return False

class Revolver(BaseWeapon):
    def __init__(self):
        super().__init__("Revolver", 6, 1.5, 0.8)

    def shoot(self, mouse_pos: tuple, birds: list):
        if super().shoot(mouse_pos, birds):
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 2
                    break
            return True
        return False

class LightRifle(BaseWeapon):
    def __init__(self):
        super().__init__("Light Rifle", 12, 1.0, 0.2)

    def shoot(self, mouse_pos: tuple, birds: list):
        if super().shoot(mouse_pos, birds):
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 1
                    break
            return True
        return False



class Shotgun(BaseWeapon):
    def __init__(self):
        super().__init__("Shotgun", 5, 2.0, 0.8)
        self.spread_radius = 60
        self.pellets_count = 10 

    def shoot(self, mouse_pos: tuple, birds: list):
        if not super().shoot(mouse_pos, birds):
            return False

        pellet_hits = []
        for _ in range(self.pellets_count):
            offset_x = random.uniform(-self.spread_radius, self.spread_radius)
            offset_y = random.uniform(-self.spread_radius, self.spread_radius)
            
            hit_point = (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y)
            pellet_hits.append(hit_point)

        hit_any_bird = False
        for bird in birds:
            if not bird.isAlive: continue
            
            hits_on_this_bird = 0
            for point in pellet_hits:
                if bird.rect.collidepoint(point):
                    hits_on_this_bird += 1
            
            if hits_on_this_bird > 0:
                bird.isAlive = False
                hit_any_bird = True
                
        return hit_any_bird

class AutomaticRifle(BaseWeapon):
    def __init__(self):
        super().__init__("Rifle", 16, 1.5, 0.2)

    def shoot(self, mouse_pos: tuple, birds: list):
        if super().shoot(mouse_pos, birds):
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.isAlive = False
                    break
            return True
        return False