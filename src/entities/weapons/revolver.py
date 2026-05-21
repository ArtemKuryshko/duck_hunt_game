from .base import BaseWeapon


class Revolver(BaseWeapon):
    def __init__(self):
        super().__init__("Revolver", 6, 1.5, 0.8)

    def shoot(self, mouse_pos: tuple, birds: list):
        effect = super().shoot(mouse_pos, birds)
        if effect:
            for bird in birds:
                if bird.rect.collidepoint(mouse_pos):
                    bird.health -= 2
                    break
            return effect
        return None
