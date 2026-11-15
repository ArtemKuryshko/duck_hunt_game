import pytest
from unittest.mock import MagicMock
import pygame
from ui.button import Button
from ui.menu import Menu
from ui.ui_system import UISystem
from config import GameState


@pytest.mark.unit
class TestButton:
    def test_initialization(self, mock_font_obj):
        button = Button("Test", 10, 20, 100, 50, mock_font_obj, (255, 0, 0), (0, 255, 0))
        assert button.text == "Test"
        assert button.rect == pygame.Rect(10, 20, 100, 50)
        assert button.is_hovered is False

    def test_update_hover(self, mock_font_obj):
        button = Button("Test", 0, 0, 100, 100, mock_font_obj, (255, 0, 0), (0, 255, 0))
        button.update((50, 50))
        assert button.is_hovered is True

        button.update((150, 150))
        assert button.is_hovered is False

    def test_is_clicked(self, mock_font_obj):
        button = Button("Test", 0, 0, 100, 100, mock_font_obj, (255, 0, 0), (0, 255, 0))
        button.is_hovered = True

        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1

        assert button.is_clicked(event) is True

        button.is_hovered = False
        assert button.is_clicked(event) is False


@pytest.mark.unit
class TestMenu:
    def test_initialization(self, mock_pygame_env):
        menu = Menu()
        assert menu.play_button is not None
        assert menu.shop_button is not None

    def test_handle_events_navigation(self, mock_pygame_env):
        menu = Menu()
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1

        # Mock button click detection
        menu.play_button.is_hovered = True
        assert menu.handle_events(event) == GameState.GAME

        menu.play_button.is_hovered = False
        menu.shop_button.is_hovered = True
        assert menu.handle_events(event) == GameState.SHOP

    def test_update_calls_button_update(self, mock_pygame_env, monkeypatch):
        menu = Menu()
        monkeypatch.setattr("pygame.mouse.get_pos", lambda: (50, 50))

        # Position (50, 50) should hover play button
        menu.play_button.update = MagicMock()
        menu.shop_button.update = MagicMock()

        menu.update()
        menu.play_button.update.assert_called_with((50, 50))
        menu.shop_button.update.assert_called_with((50, 50))


@pytest.mark.unit
class TestUISystem:
    def test_draw_health_ui(self, mock_pygame_env, mock_font_obj):
        ui = UISystem(mock_font_obj)
        screen = MagicMock()

        ui.draw_health_ui(screen, 2)
        # 3 hearts total, blit called 3 times
        assert screen.blit.call_count == 3

    def test_draw_game_ui(self, mock_pygame_env, mock_font_obj):
        ui = UISystem(mock_font_obj)
        screen = MagicMock()
        weapon = MagicMock()
        weapon.is_reloading = False
        weapon.current_ammo = 5
        weapon.ammo_capacity = 8
        weapon.name = "Pistol"

        ui.draw_game_ui(screen, 100, 3, weapon)
        assert screen.blit.called
        assert mock_font_obj.render.called
