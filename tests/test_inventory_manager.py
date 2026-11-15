import json

import pytest
from systems.inventory_manager import InventoryManager


pytestmark = [pytest.mark.systems]


@pytest.mark.io
def test_creates_inventory_file_with_defaults(inventory_file):
    manager = InventoryManager(file_path=str(inventory_file))
    assert manager.unlocked_weapons == ["Pistol"]
    assert manager.current_weapon == "Pistol"
    assert inventory_file.exists()


@pytest.mark.io
def test_unlock_weapon_persists_to_disk(inventory_file):
    manager = InventoryManager(file_path=str(inventory_file))

    manager.unlock_weapon("Shotgun")
    reloaded = InventoryManager(file_path=str(inventory_file))

    assert "Shotgun" in reloaded.unlocked_weapons


@pytest.mark.unit
def test_equip_weapon_changes_current_weapon_when_unlocked(inventory_file):
    manager = InventoryManager(file_path=str(inventory_file))
    manager.unlock_weapon("Shotgun")

    manager.equip_weapon("Shotgun")

    assert manager.current_weapon == "Shotgun"


@pytest.mark.io
@pytest.mark.parametrize(
    ("contents", "expected_unlocked", "expected_current"),
    [
        ("{", ["Pistol"], "Pistol"),
        ('{"unlocked_weapons": ["Pistol", "Shotgun"]}', ["Pistol", "Shotgun"], "Pistol"),
        ('{"current_weapon": "Shotgun"}', ["Pistol"], "Pistol"),
        ('{"unlocked_weapons": [], "current_weapon": "Shotgun"}', ["Pistol"], "Pistol"),
        ("null", ["Pistol"], "Pistol"),
    ],
)
def test_load_from_file_recovers_invalid_or_partial_data(
    inventory_file,
    contents,
    expected_unlocked,
    expected_current,
):
    inventory_file.write_text(contents, encoding="utf-8")

    manager = InventoryManager(file_path=str(inventory_file))

    assert manager.unlocked_weapons == expected_unlocked
    assert manager.current_weapon == expected_current
    assert json.loads(inventory_file.read_text(encoding="utf-8")) == {
        "unlocked_weapons": expected_unlocked,
        "current_weapon": expected_current,
    }


@pytest.mark.unit
def test_equip_weapon_ignores_locked_weapon(inventory_manager):
    inventory_manager.equip_weapon("Shotgun")

    assert inventory_manager.current_weapon == "Pistol"


@pytest.mark.unit
def test_unlock_weapon_does_not_duplicate_existing_weapon(inventory_manager):
    inventory_manager.unlock_weapon("Shotgun")
    inventory_manager.unlock_weapon("Shotgun")

    assert inventory_manager.unlocked_weapons == ["Pistol", "Shotgun"]
