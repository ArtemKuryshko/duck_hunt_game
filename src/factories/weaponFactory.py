
from entities.weapons.concrete_weapons import Pistol, Revolver, Shotgun, LightRifle, AutomaticRifle

class WeaponFactory:
    @staticmethod
    def create_weapon(weapon_type: str):
        weapons = {
            "pistol": Pistol,
            "revolver": Revolver,
            "shotgun": Shotgun,
            "light rifle": LightRifle,
            "automatic rifle": AutomaticRifle
        }
        
        weapon_class = weapons.get(weapon_type.lower())
        if weapon_class:
            return weapon_class()
        raise ValueError(f"Unknown weapon type: {weapon_type}")