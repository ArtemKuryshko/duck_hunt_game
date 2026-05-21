from .base import BaseWeapon


class AutomaticRifle(BaseWeapon):
    def __init__(self):
        super().__init__("Rifle", 16, 1.5, 0.2)

    def shoot(self, mouse_pos: tuple, birds: list):
        effect = super().shoot(mouse_pos, birds)
        if effect:
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health = 0
                    break
            return effect
        return None
