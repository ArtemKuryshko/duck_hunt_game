from systems.inventory_manager import InventoryManager


def test_creates_inventory_file_with_defaults(tmp_path):
    inventory_file = tmp_path / "inventory.json"

    manager = InventoryManager(file_path=str(inventory_file))

    assert manager.unlocked_weapons == ["Pistol"]
    assert manager.current_weapon == "Pistol"
    assert inventory_file.exists()


def test_unlock_weapon_persists_to_disk(tmp_path):
    inventory_file = tmp_path / "inventory.json"
    manager = InventoryManager(file_path=str(inventory_file))

    manager.unlock_weapon("Shotgun")
    reloaded = InventoryManager(file_path=str(inventory_file))

    assert "Shotgun" in reloaded.unlocked_weapons


def test_equip_weapon_changes_current_weapon_when_unlocked(tmp_path):
    inventory_file = tmp_path / "inventory.json"
    manager = InventoryManager(file_path=str(inventory_file))
    manager.unlock_weapon("Shotgun")

    manager.equip_weapon("Shotgun")

    assert manager.current_weapon == "Shotgun"
