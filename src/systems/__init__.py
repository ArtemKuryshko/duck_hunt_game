from .settings_manager import SettingsManager  # Тепер він ПЕРШИЙ
from .score_system import ScoreSystem
from .level_manager import LevelManager
from .point_manager import PointManager
from .inventory_manager import InventoryManager

__all__ = ["ScoreSystem", "LevelManager", "PointManager", "InventoryManager", "SettingsManager"]
