from typing import Callable


class ScoreSystem:
    def __init__(self, on_game_over: Callable = None):
        self.score: int = 0
        self.health: int = 3
        self.on_game_over = on_game_over

    def add_score(self, amount: int):
        self.score += amount

    def deduct_health(self, damage: int = 1):
        self.health -= damage
        print("Health deducted:", damage, "Current health:", self.health)
        if self.health <= 0:
            if self.on_game_over:
                self.on_game_over()
        

    def reset(self):
        self.score = 0
        self.health = 3
