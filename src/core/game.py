import pygame
import sys
from config import *
from factories.duckFactory import DuckFactory
from ui import Menu, Shop

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = GameState.MAIN_MENU

        self.background = pygame.image.load(BG_PATH).convert()
        self.trees = pygame.image.load(TREES_PATH).convert_alpha()
        self.grass = pygame.image.load(GRASS_PATH).convert_alpha()

        self.scoreboard = pygame.image.load(SCOREBOARD_PATH).convert_alpha()

        self.menu = Menu()
        self.shop = Shop()

    def process_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if self.state == GameState.MAIN_MENU:
                self.state = self.menu.handle_events(event)
            elif self.state == GameState.SHOP:
                self.state = self.shop.handle_events(event)
            elif self.state == GameState.GAME:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MAIN_MENU

    def update(self):
        if self.state == GameState.MAIN_MENU:
            self.menu.update()
        elif self.state == GameState.SHOP:
            self.shop.update()
        elif self.state == GameState.GAME:
            pass

    def draw_game_world(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.trees, (0, 0))
        self.screen.blit(self.grass, (0, 0))
        self.screen.blit(self.grass, (0, -20))
        self.screen.blit(self.scoreboard, (100, 490))

    def draw(self):
        self.draw_game_world()

        if self.state == GameState.MAIN_MENU:
            self.menu.draw(self.screen)
        elif self.state == GameState.SHOP:
            self.shop.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS) 

        pygame.quit()
        sys.exit()