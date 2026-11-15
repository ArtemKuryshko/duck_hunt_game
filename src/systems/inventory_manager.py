import json
import os

from config import BASE_DIR


class InventoryManager:
    def __init__(self, file_path: str | None = None):
        self.unlocked_weapons = ["Pistol"]
        self.current_weapon = "Pistol"
        self.file_path = file_path or os.path.join(BASE_DIR, "inventory.json")
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.file_path):
            self.update_file()
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise TypeError("Inventory payload must be a JSON object")
        except (json.JSONDecodeError, OSError, TypeError):
            self.unlocked_weapons = ["Pistol"]
            self.current_weapon = "Pistol"
            self.update_file()
            return

        unlocked_weapons = data.get("unlocked_weapons", ["Pistol"])
        if not isinstance(unlocked_weapons, list) or not unlocked_weapons:
            unlocked_weapons = ["Pistol"]

        self.unlocked_weapons = unlocked_weapons
        current_weapon = data.get("current_weapon", "Pistol")
        self.current_weapon = current_weapon if current_weapon in self.unlocked_weapons else "Pistol"
        self.update_file()

    def unlock_weapon(self, weapon_name: str):
        if weapon_name not in self.unlocked_weapons:
            self.unlocked_weapons.append(weapon_name)
            self.update_file()

    def equip_weapon(self, weapon_name: str):
        if weapon_name in self.unlocked_weapons:
            self.current_weapon = weapon_name
            self.update_file()

    def update_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump({
                "unlocked_weapons": self.unlocked_weapons,
                "current_weapon": self.current_weapon
            }, file)
