import pygame
from unittest.mock import MagicMock
from pathlib import Path
import sys
from dataclasses import dataclass

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from systems.inventory_manager import InventoryManager
from systems.level_manager import LevelManager
from systems.point_manager import PointManager
from systems.score_system import ScoreSystem
from systems.settings_manager import SettingsManager
from systems.trajectory_creator import BirdTrajectory


@dataclass
class StubBird:
    x: int = 0
    y: int = 0
    isAlive: bool = True
    was_shot: bool = False
    points_handled: bool = False
    damage: int = 0
    kill_points: int = 0
    update_result: object = None

    def update(self, dt):
        return self.update_result


@pytest.fixture
def score_system():
    return ScoreSystem()


@pytest.fixture
def points_file(tmp_path):
    return tmp_path / "points.json"


@pytest.fixture
def inventory_file(tmp_path):
    return tmp_path / "inventory.json"


@pytest.fixture
def settings_file(tmp_path):
    return tmp_path / "settings.json"


@pytest.fixture
def point_manager(points_file):
    return PointManager(file_path=str(points_file))


@pytest.fixture
def inventory_manager(inventory_file):
    return InventoryManager(file_path=str(inventory_file))


@pytest.fixture
def settings_manager(settings_file):
    return SettingsManager(file_path=str(settings_file))


@pytest.fixture
def mock_settings_manager():
    return type("SettingsStub", (), {"difficulty": "medium"})()


@pytest.fixture
def stub_bird_factory():
    return StubBird


@pytest.fixture
def level_manager(score_system):
    manager = LevelManager(
        score_system=score_system,
        on_bird_escape=lambda: None,
        difficulty="easy",
    )
    return manager


@pytest.fixture
def mock_animations():
    mock_surf = MagicMock(spec=pygame.Surface)
    mock_surf.get_rect.return_value = pygame.Rect(0, 0, 150, 150)
    return {
        "Side": [mock_surf],
        "Up": [mock_surf],
        "Diagonal": [mock_surf],
        "Dead": [mock_surf]
    }


@pytest.fixture
def mock_trajectory_class(monkeypatch):
    """Consolidated fixture to mock BirdTrajectory during bird initialization."""
    mock_traj = MagicMock(spec=BirdTrajectory)
    mock_traj.get_position.return_value = (100.0, 100.0)
    mock_traj.get_rotation_angle.return_value = 0.0
    mock_traj.is_finished = False

    mock_class = MagicMock(return_value=mock_traj)
    monkeypatch.setattr("entities.birds.base.BirdTrajectory", mock_class)
    return mock_traj
