import pytest
import pygame
from unittest.mock import MagicMock
from entities.weapons.pistol import Pistol
from entities.weapons.shotgun import Shotgun
from entities.birds.whiteDuck import WhiteDuck

@pytest.mark.unit
class TestWeapon:
    def test_initialization(self):
        pistol = Pistol()
        assert pistol.name == "Pistol"
        assert pistol.current_ammo == 8
        assert pistol.is_reloading is False

    def test_can_shoot_logic(self, monkeypatch):
        pistol = Pistol()
        pistol.shot_animation = MagicMock()
        monkeypatch.setattr("pygame.time.get_ticks", lambda: 1000)
        
        assert pistol.can_shoot() is True
        
        pistol.current_ammo = 0
        assert pistol.can_shoot() is False
        
        pistol.current_ammo = 8
        pistol.is_reloading = True
        assert pistol.can_shoot() is False

    def test_fire_rate_constraints(self, monkeypatch):
        pistol = Pistol() # fire_rate = 0.5s = 500ms
        pistol.shot_animation = MagicMock()
        ticks = [1000]
        monkeypatch.setattr("pygame.time.get_ticks", lambda: ticks[0])
        
        pistol.shoot((0,0), [])
        assert pistol.current_ammo == 7
        assert pistol.can_shoot() is False
        
        ticks[0] = 1400
        assert pistol.can_shoot() is False
        
        ticks[0] = 1600
        assert pistol.can_shoot() is True

    def test_reload_cycle(self):
        pistol = Pistol() # reload_time = 1.0s = 1000ms
        pistol.current_ammo = 0
        
        pistol.start_reload()
        assert pistol.is_reloading is True
        
        pistol.update(500)
        assert pistol.is_reloading is True
        assert pistol.current_ammo == 0
        
        pistol.update(600)
        assert pistol.is_reloading is False
        assert pistol.current_ammo == 8

@pytest.mark.unit
class TestSpecificWeapons:
    def test_pistol_hit_registration(self, mock_animations, mock_trajectory_class, monkeypatch):
        duck = WhiteDuck(100, 100, mock_animations)
        duck.rect = pygame.Rect(90, 90, 20, 20)
        
        pistol = Pistol()
        pistol.shot_animation = MagicMock()
        monkeypatch.setattr("pygame.time.get_ticks", lambda: 1000)
        
        pistol.shoot((100, 100), [duck])
        duck.update(0)
        
        assert duck.health == 0
        assert duck.isAlive is False

    def test_shotgun_spread_and_multiple_hits(self, mock_animations, mock_trajectory_class, monkeypatch):
        duck1 = WhiteDuck(100, 100, mock_animations)
        duck1.rect = pygame.Rect(90, 90, 20, 20)
        
        duck2 = WhiteDuck(110, 110, mock_animations)
        duck2.rect = pygame.Rect(100, 100, 20, 20)
        
        shotgun = Shotgun()
        shotgun.shot_animation = MagicMock()
        monkeypatch.setattr("pygame.time.get_ticks", lambda: 1000)
        monkeypatch.setattr("entities.weapons.shotgun.random.uniform", lambda a, b: 0)
        
        shotgun.shoot((100, 100), [duck1, duck2])
        duck1.update(0)
        duck2.update(0)
        
        assert duck1.health <= 0
        assert duck2.health <= 0
        assert duck1.isAlive is False
        assert duck2.isAlive is False
