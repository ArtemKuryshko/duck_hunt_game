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

from core.game import Game
from ui.shop import Shop
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
def mock_surf():
    surf = MagicMock(spec=pygame.Surface)
    surf.get_rect.return_value = pygame.Rect(0, 0, 150, 150)
    surf.get_width.return_value = 150
    surf.get_height.return_value = 150
    surf.convert.return_value = surf
    surf.convert_alpha.return_value = surf
    return surf


@pytest.fixture
def mock_font_obj():
    font = MagicMock(spec=pygame.font.Font)
    font.render.return_value = pygame.Surface((10, 10))
    return font


@pytest.fixture
def mock_pygame_env(monkeypatch, mock_surf, mock_font_obj):
    """Mocks common pygame modules to avoid window creation and hardware dependency."""
    # Display
    mock_display = MagicMock()
    monkeypatch.setattr("pygame.display.set_mode", lambda _: mock_display)
    monkeypatch.setattr("pygame.display.set_caption", lambda _: None)
    monkeypatch.setattr("pygame.display.flip", lambda: None)

    # Init/Quit
    monkeypatch.setattr("pygame.init", lambda: None)
    monkeypatch.setattr("pygame.quit", lambda: None)

    # Images
    monkeypatch.setattr("pygame.image.load", lambda _: mock_surf)
    monkeypatch.setattr("pygame.transform.scale", lambda img, size: img)
    monkeypatch.setattr("pygame.transform.smoothscale", lambda img, size: img)

    # Fonts
    monkeypatch.setattr("pygame.font.Font", lambda *args: mock_font_obj)
    monkeypatch.setattr("pygame.font.SysFont", lambda *args, **kwargs: mock_font_obj)

    # Clock
    mock_clock = MagicMock(spec=pygame.time.Clock)
    mock_clock.get_time.return_value = 16
    monkeypatch.setattr("pygame.time.Clock", lambda: mock_clock)

    # Mouse
    monkeypatch.setattr("pygame.mouse.set_visible", lambda _: None)
    monkeypatch.setattr("pygame.mouse.get_pos", lambda: (400, 300))

    return mock_display


@pytest.fixture
def mock_animations(mock_surf):
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


@pytest.fixture
def shop(mock_pygame_env, point_manager, inventory_manager):
    """Creates a Shop instance with mocked dependencies."""
    return Shop(point_manager, inventory_manager)


@pytest.fixture
def game(mock_pygame_env, monkeypatch):
    """Creates a Game instance with mocked internal systems."""
    # Mock UI and Systems to avoid side effects (file I/O, complex logic)
    systems = [
        "Menu", "Shop", "UISystem", "ScoreSystem",
        "LevelManager", "PointManager", "InventoryManager", "SettingsManager"
    ]
    for system in systems:
        monkeypatch.setattr(f"core.game.{system}", MagicMock())

    # Mock WeaponFactory
    mock_weapon = MagicMock()
    monkeypatch.setattr("core.game.WeaponFactory.create_weapon", lambda _: mock_weapon)

    return Game()
