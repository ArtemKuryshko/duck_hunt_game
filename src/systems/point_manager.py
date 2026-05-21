import json
import os

from config import BASE_DIR


class PointManager:
    def __init__(self, file_path: str | None = None):
        self.points = 0
        self.best_score = 0
        self.file_path = file_path or os.path.join(BASE_DIR, "points.json")
        self.create_file()

    def create_file(self):
        try:
            with open(self.file_path, "x", encoding="utf-8") as file:
                json.dump({"points": 0, "best_score": 0}, file)
        except FileExistsError:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise TypeError("Points payload must be a JSON object")
        except (json.JSONDecodeError, OSError, TypeError):
            self.points = 0
            self.best_score = 0
            self.update_file()
            return

        self.points = data.get("points", 0)
        self.best_score = data.get("best_score", 0)
        self.update_file()

    def update_points(self, gained_points: int):
        self.points += gained_points
        self.best_score = max(self.best_score, gained_points)
        self.update_file()

    def spend_points(self, amount: int) -> bool:
        if self.points >= amount:
            self.points -= amount
            self.update_file()
            return True
        return False

    def update_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump({"points": self.points, "best_score": self.best_score}, file)
