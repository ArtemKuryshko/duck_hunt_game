import os
from enum import Enum, auto


class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SHOP = auto()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Duck Hunt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "assets"))
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "pixelify.ttf")
BG_PATH = os.path.join(ASSETS_DIR, "images", "backgrounds", "Background.png")
TREES_PATH = os.path.join(ASSETS_DIR, "images", "backgrounds", "Trees.png")
GRASS_PATH = os.path.join(ASSETS_DIR, "images", "backgrounds", "Grass.png")
ANIMATIONS_PATH = os.path.join(ASSETS_DIR, "images", "models", "birds")
SCOREBOARD_PATH = os.path.join(ASSETS_DIR, "images", "interface", "Scoreboard.png")
HEART_PATH = os.path.join(ASSETS_DIR, "images", "interface", "HeartIcon.png")
GREY_HEART_PATH = os.path.join(ASSETS_DIR, "images", "interface", "GreyHeartIcon.png")
CROSSHAIR_PATH = os.path.join(ASSETS_DIR, "images", "interface", "Crosshair.png")
