import json

from systems.settings_manager import SettingsManager


def test_uses_default_difficulty_and_creates_file(tmp_path):
    settings_file = tmp_path / "settings.json"

    manager = SettingsManager(file_path=str(settings_file))

    assert manager.difficulty == "easy"
    assert json.loads(settings_file.read_text(encoding="utf-8")) == {"difficulty": "easy"}


def test_invalid_json_falls_back_to_easy(tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{", encoding="utf-8")

    manager = SettingsManager(file_path=str(settings_file))

    assert manager.difficulty == "easy"


def test_cli_argument_overrides_loaded_value(tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text('{"difficulty": "easy"}', encoding="utf-8")

    manager = SettingsManager(file_path=str(settings_file), argv=["--difficulty", "hard"])

    assert manager.difficulty == "hard"
