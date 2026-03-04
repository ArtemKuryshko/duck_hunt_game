import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE ="Duck Hunt"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets") 
BG_PATH = os.path.join(ASSETS_DIR, "images","backgrounds", "Background.png")
TREES_PATH = os.path.join(ASSETS_DIR, "images","backgrounds", "Trees.png")
GRASS_PATH = os.path.join(ASSETS_DIR, "images","backgrounds", "Grass.png")
SCOREBOARD_PATH = os.path.join(ASSETS_DIR, "images","interface", "Scoreboard.png")
