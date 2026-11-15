import argparse
import json
import os

from config import BASE_DIR


class SettingsManager:
    VALID_DIFFICULTIES = ("easy", "medium", "hard")

    def __init__(self, file_path: str | None = None, argv: list[str] | None = None):
        self.file_path = file_path or os.path.join(BASE_DIR, "settings.json")
        self.difficulty = "easy"
        self.load_settings()
        if argv is not None:
            self.parse_cli_arguments(argv)

    def load_settings(self):
        if not os.path.exists(self.file_path):
            self.create_settings()

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                settings = json.load(file)
                if not isinstance(settings, dict):
                    raise TypeError("Settings payload must be a JSON object")
                difficulty = settings.get("difficulty", "easy")
                self.difficulty = difficulty if difficulty in self.VALID_DIFFICULTIES else "easy"
        except (json.JSONDecodeError, IOError, TypeError):
            self.difficulty = "easy"

    def create_settings(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump({"difficulty": self.difficulty}, file, indent=4)

    def parse_cli_arguments(self, argv: list[str] | None = None):
        parser = argparse.ArgumentParser(description="Duck Hunt Game Configurations")

        parser.add_argument(
            "-d", "--difficulty",
            choices=self.VALID_DIFFICULTIES,
            help="Тимчасово змінити складність гри на один запуск",
        )

        args = parser.parse_args(argv)

        if args.difficulty:
            print(f"[CLI] Складність змінено через термінал на: {args.difficulty.upper()}")
            self.difficulty = args.difficulty
