from .base import BaseWeapon

class LightRifle(BaseWeapon):
    def __init__(self):
        super().__init__("Light Rifle", 12, 1.0, 0.2)

    def shoot(self, mouse_pos: tuple, birds: list):
        effect = super().shoot(mouse_pos, birds)
        if effect:
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 1
                    break
            return effect
        return None
