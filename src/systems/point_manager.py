import json, os
from config import BASE_DIR

class PointManager:
    def __init__(self):
        self.points = 0
        self.best_score = 0
        self.create_file()

    def create_file(self):
        try:
            with open(os.path.join(BASE_DIR, "points.json"), "x") as file:
                json.dump({"points": 0, "best_score": 0}, file)
        except FileExistsError: 
            self.load_from_file()

    def load_from_file(self):
        with open(os.path.join(BASE_DIR, "points.json"), "r") as file:
            data = json.load(file)
            self.points = data["points"]
            self.best_score = data["best_score"]

    def update_points(self, gained_points: int):
        self.points += gained_points
        self.best_score = max(self.best_score, gained_points)
        self.update_file()
        print(f"best: {self.best_score} points: {self.points}")

    def spend_points(self, amount: int) -> bool:
        if self.points >= amount:
            self.points -= amount
            self.update_file()
            return True
        return False

    def update_file(self):
        with open(os.path.join(BASE_DIR, "points.json"), "w") as file:
            json.dump({"points": self.points, "best_score": self.best_score}, file)