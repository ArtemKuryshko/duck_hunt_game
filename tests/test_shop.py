import pytest
from unittest.mock import MagicMock
import pygame
from config import GameState


@pytest.mark.unit
class TestShop:
    def test_initialization(self, shop):
        assert len(shop.items) == 5
        assert len(shop.item_rects) == 5
        assert shop.items[0]["name"] == "Pistol"

    def test_handle_events_escape(self, shop):
        event = MagicMock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = shop.handle_events(event)
        assert result == GameState.MAIN_MENU

    def test_handle_events_equip_unlocked(self, shop, inventory_manager):
        # Pistol is unlocked by default
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        # Item 0 is Pistol
        rect = shop.item_rects[0]
        event.pos = (rect.x + 5, rect.y + 5)

        inventory_manager.unlocked_weapons = ["Pistol", "Shotgun"]
        inventory_manager.current_weapon = "Pistol"

        # Click on Shotgun (index 3)
        rect_shotgun = shop.item_rects[3]
        event.pos = (rect_shotgun.x + 5, rect_shotgun.y + 5)

        shop.handle_events(event)

        assert inventory_manager.current_weapon == "Shotgun"

    def test_handle_events_buy_and_equip(self, shop, point_manager, inventory_manager):
        # Set up points
        point_manager.points = 1000
        inventory_manager.unlocked_weapons = ["Pistol"]

        # Click on Revolver (index 1, price 100)
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        rect = shop.item_rects[1]
        event.pos = (rect.x + 5, rect.y + 5)

        shop.handle_events(event)

        assert "Revolver" in inventory_manager.unlocked_weapons
        assert inventory_manager.current_weapon == "Revolver"
        assert point_manager.points == 900

    def test_handle_events_insufficient_points(self, shop, point_manager, inventory_manager):
        point_manager.points = 10
        inventory_manager.unlocked_weapons = ["Pistol"]

        # Click on Revolver (price 100)
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        rect = shop.item_rects[1]
        event.pos = (rect.x + 5, rect.y + 5)

        shop.handle_events(event)

        assert "Revolver" not in inventory_manager.unlocked_weapons
        assert inventory_manager.current_weapon == "Pistol"
        assert point_manager.points == 10

    def test_draw_calls_blit(self, shop):
        mock_screen = MagicMock()
        shop.draw(mock_screen)

        # Just verify that something was drawn
        assert mock_screen.blit.called
