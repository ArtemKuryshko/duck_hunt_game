import pytest
from unittest.mock import MagicMock, patch
import pygame
from core.game import Game
from config import GameState


@pytest.fixture
def mock_pygame(monkeypatch):
    """Mocks all necessary pygame modules and functions to avoid window creation."""
    mock_display = MagicMock()
    monkeypatch.setattr("pygame.display.set_mode", lambda _: mock_display)
    monkeypatch.setattr("pygame.display.set_caption", lambda _: None)
    monkeypatch.setattr("pygame.display.flip", lambda: None)
    monkeypatch.setattr("pygame.init", lambda: None)
    monkeypatch.setattr("pygame.quit", lambda: None)

    # Mock image loading to return a Surface
    mock_surf = MagicMock(spec=pygame.Surface)
    mock_surf.convert.return_value = mock_surf
    mock_surf.convert_alpha.return_value = mock_surf
    monkeypatch.setattr("pygame.image.load", lambda _: mock_surf)

    # Mock Font
    mock_font = MagicMock(spec=pygame.font.Font)
    monkeypatch.setattr("pygame.font.Font", lambda *args: mock_font)

    # Mock Clock
    mock_clock = MagicMock(spec=pygame.time.Clock)
    mock_clock.get_time.return_value = 16
    monkeypatch.setattr("pygame.time.Clock", lambda: mock_clock)

    # Mock mouse
    monkeypatch.setattr("pygame.mouse.set_visible", lambda _: None)
    monkeypatch.setattr("pygame.mouse.get_pos", lambda: (400, 300))

    return mock_display


@pytest.fixture
def game(mock_pygame, monkeypatch):
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


@pytest.mark.unit
class TestGame:
    def test_initialization(self, game):
        assert game.state == GameState.MAIN_MENU
        assert game.is_running is True
        assert game.current_weapon is not None
        assert isinstance(game.effects, pygame.sprite.Group)

    def test_game_over(self, game):
        game.state = GameState.GAME
        game.score_system.score = 100

        game.game_over()

        assert game.state == GameState.MAIN_MENU
        game.point_manager.update_points.assert_called_with(100)
        game.score_system.reset.assert_called_once()
        game.level_manager.birds.clear.assert_called_once()

    def test_process_events_quit(self, game, monkeypatch):
        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        monkeypatch.setattr("pygame.event.get", lambda: [mock_event])

        game.process_events()
        assert game.is_running is False

    def test_process_events_game_shoot(self, game, monkeypatch):
        game.state = GameState.GAME
        mock_event = MagicMock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        monkeypatch.setattr("pygame.event.get", lambda: [mock_event])

        game.process_events()
        game.current_weapon.shoot.assert_called_once()

    def test_process_events_game_reload(self, game, monkeypatch):
        game.state = GameState.GAME
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_r
        monkeypatch.setattr("pygame.event.get", lambda: [mock_event])

        game.process_events()
        game.current_weapon.start_reload.assert_called_once()

    def test_process_events_menu_to_game_transition(self, game, monkeypatch):
        game.state = GameState.MAIN_MENU
        game.menu.handle_events.return_value = GameState.GAME

        mock_event = MagicMock()
        mock_event.type = pygame.USEREVENT  # Arbitrary event
        monkeypatch.setattr("pygame.event.get", lambda: [mock_event])

        game.process_events()

        assert game.state == GameState.GAME
        game.score_system.reset.assert_called_once()

    def test_update_calls_systems(self, game):
        game.state = GameState.GAME
        game.clock.get_time.return_value = 16

        game.update()

        game.level_manager.update.assert_called_with(16)
        game.current_weapon.update.assert_called_with(16)

    @patch("sys.exit")
    def test_run_loop_termination(self, mock_exit, game, monkeypatch):
        # Force the loop to run once and then stop
        game.is_running = True

        # We need to mock process_events to set is_running = False
        def mock_process():
            game.is_running = False

        monkeypatch.setattr(game, "process_events", mock_process)
        monkeypatch.setattr(game, "update", MagicMock())
        monkeypatch.setattr(game, "draw", MagicMock())

        game.run()

        assert mock_exit.called
