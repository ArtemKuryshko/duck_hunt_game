from .base import BaseWeapon

class Pistol(BaseWeapon):
    def __init__(self):
        super().__init__("Pistol", 8, 1.0, 0.5)

    def shoot(self, mouse_pos: tuple, birds: list):
        effect = super().shoot(mouse_pos, birds)
        if effect:
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 1
                    break
            return effect
        return None
