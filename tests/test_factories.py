from unittest.mock import Mock

import pytest

from entities.weapons import AutomaticRifle, LightRifle, Pistol, Revolver, Shotgun
from factories.duckFactory import DuckFactory
from factories.weaponFactory import WeaponFactory


pytestmark = [pytest.mark.unit]


@pytest.fixture
def reset_duck_factory_cache():
    DuckFactory._resources.clear()
    yield
    DuckFactory._resources.clear()


@pytest.mark.systems
@pytest.mark.parametrize(
    ("weapon_name", "expected_class"),
    [
        ("pistol", Pistol),
        ("Pistol", Pistol),
        ("REVOLVER", Revolver),
        ("shotgun", Shotgun),
        ("Light Rifle", LightRifle),
        ("automatic rifle", AutomaticRifle),
    ],
)
def test_weapon_factory_creates_expected_weapon_case_insensitively(weapon_name, expected_class):
    weapon = WeaponFactory.create_weapon(weapon_name)

    assert isinstance(weapon, expected_class)


@pytest.mark.systems
def test_weapon_factory_rejects_unknown_weapon_type():
    with pytest.raises(ValueError, match="Unknown weapon type: Laser"):
        WeaponFactory.create_weapon("Laser")


@pytest.mark.systems
def test_duck_factory_loads_and_groups_animation_frames(monkeypatch, reset_duck_factory_cache):
    file_names = [
        "Diagonal_2.png",
        "Up_1.png",
        "Dead.png",
        "Side_1.png",
        "README.txt",
        "Diagonal_1.png",
    ]
    loaded_paths = []
    scaled_images = []

    class FakeImage:
        def __init__(self, source_path):
            self.source_path = source_path

        def convert_alpha(self):
            loaded_paths.append(self.source_path)
            return self

    def fake_load(image_path):
        return FakeImage(image_path)

    def fake_scale(image, size):
        scaled = {"path": image.source_path, "size": size}
        scaled_images.append(scaled)
        return scaled

    monkeypatch.setattr("factories.duckFactory.listdir", lambda _: file_names)
    monkeypatch.setattr("factories.duckFactory.pygame.image.load", fake_load)
    monkeypatch.setattr("factories.duckFactory.pygame.transform.smoothscale", fake_scale)

    animations = DuckFactory.load_duck_animations("WhiteDuck")

    assert list(animations) == ["Side", "Up", "Diagonal", "Dead"]
    assert [frame["path"].split("/")[-1] for frame in animations["Side"]] == ["Side_1.png"]
    assert [frame["path"].split("/")[-1] for frame in animations["Up"]] == ["Up_1.png"]
    assert [frame["path"].split("/")[-1] for frame in animations["Diagonal"]] == ["Diagonal_1.png", "Diagonal_2.png"]
    assert [frame["path"].split("/")[-1] for frame in animations["Dead"]] == ["Dead.png"]
    assert all(frame["size"] == (150, 150) for frame in scaled_images)
    assert all("README.txt" not in path for path in loaded_paths)


@pytest.mark.systems
def test_duck_factory_uses_cached_animations(monkeypatch, reset_duck_factory_cache):
    listdir = Mock(return_value=["Side_1.png"])

    class FakeImage:
        def convert_alpha(self):
            return self

    monkeypatch.setattr("factories.duckFactory.listdir", listdir)
    monkeypatch.setattr("factories.duckFactory.pygame.image.load", lambda _: FakeImage())
    monkeypatch.setattr("factories.duckFactory.pygame.transform.smoothscale", lambda image, size: (image, size))

    first = DuckFactory.load_duck_animations("GreenDuck")
    second = DuckFactory.load_duck_animations("GreenDuck")

    assert first is second
    listdir.assert_called_once()


@pytest.mark.systems
@pytest.mark.parametrize("duck_type", ["WhiteDuck", "BadCrow", "GreenDuck"])
def test_duck_factory_creates_expected_duck_type(monkeypatch, duck_type):
    animations = {"Side": [], "Up": [], "Diagonal": [], "Dead": []}
    monkeypatch.setattr(DuckFactory, "load_duck_animations", lambda _: animations)

    class FakeBird:
        def __init__(self, x, y, loaded_animations):
            self.x = x
            self.y = y
            self.animations = loaded_animations

    monkeypatch.setattr("factories.duckFactory.WhiteDuck", FakeBird)
    monkeypatch.setattr("factories.duckFactory.BadCrow", FakeBird)
    monkeypatch.setattr("factories.duckFactory.GreenDuck", FakeBird)

    bird = DuckFactory.create_duck(duck_type, 10, 20)

    assert isinstance(bird, FakeBird)
    assert bird.x == 10
    assert bird.y == 20
    assert bird.animations is animations


@pytest.mark.systems
def test_duck_factory_rejects_unknown_duck_type(monkeypatch):
    monkeypatch.setattr(DuckFactory, "load_duck_animations", lambda _: {})

    with pytest.raises(ValueError, match="Unknown duck type: Eagle"):
        DuckFactory.create_duck("Eagle", 0, 0)
