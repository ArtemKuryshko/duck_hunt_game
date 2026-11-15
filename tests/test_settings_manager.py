import json
from unittest.mock import patch

import pytest
from systems.settings_manager import SettingsManager


pytestmark = [pytest.mark.systems]


@pytest.mark.io
def test_uses_default_difficulty_and_creates_file(settings_file):
    manager = SettingsManager(file_path=str(settings_file))
    assert manager.difficulty == "easy"
    assert json.loads(settings_file.read_text(encoding="utf-8")) == {"difficulty": "easy"}


@pytest.mark.io
@pytest.mark.parametrize(
    "contents",
    ["{", '{"difficulty": "nightmare"}', "null"],
)
def test_invalid_or_unsupported_file_contents_fall_back_to_easy(settings_file, contents):
    settings_file.write_text(contents, encoding="utf-8")

    manager = SettingsManager(file_path=str(settings_file))

    assert manager.difficulty == "easy"


@pytest.mark.unit
def test_cli_argument_overrides_loaded_value(settings_file):
    settings_file.write_text('{"difficulty": "easy"}', encoding="utf-8")

    manager = SettingsManager(file_path=str(settings_file), argv=["--difficulty", "hard"])

    assert manager.difficulty == "hard"


@pytest.mark.unit
def test_parse_cli_arguments_uses_argparse_result(settings_file):
    with patch("systems.settings_manager.argparse.ArgumentParser.parse_args") as parse_args:
        parse_args.return_value = type("Args", (), {"difficulty": "medium"})()
        manager = SettingsManager(file_path=str(settings_file), argv=[])

    assert manager.difficulty == "medium"
    parse_args.assert_called_once_with([])
