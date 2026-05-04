import json, os
from config import BASE_DIR


class InventoryManager:
    def __init__(self):
        self.unlocked_weapons = ["Pistol"]
        self.current_weapon = "Pistol"
        self.file_path = os.path.join(BASE_DIR, "inventory.json")
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.file_path):
            self.update_file()
        else:
            self.load_from_file()

    def load_from_file(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
            self.unlocked_weapons = data.get("unlocked_weapons", ["Pistol"])
            self.current_weapon = data.get("current_weapon", "Pistol")

    def unlock_weapon(self, weapon_name: str):
        if weapon_name not in self.unlocked_weapons:
            self.unlocked_weapons.append(weapon_name)
            self.update_file()

    def equip_weapon(self, weapon_name: str):
        if weapon_name in self.unlocked_weapons:
            self.current_weapon = weapon_name
            self.update_file()

    def update_file(self):
        with open(self.file_path, "w") as file:
            json.dump({
                "unlocked_weapons": self.unlocked_weapons,
                "current_weapon": self.current_weapon
            }, file)