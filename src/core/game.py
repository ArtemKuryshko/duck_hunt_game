import pygame
import sys
from config import (
    FONT_PATH,
    GameState,
    TITLE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TREES_PATH,
    GRASS_PATH,
    SCOREBOARD_PATH,
    FPS,
    BG_PATH,
)
from ui import Menu, Shop, UISystem
from systems import ScoreSystem, LevelManager


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

        self.font = pygame.font.Font(FONT_PATH, 30)
        self.score_system = ScoreSystem(on_game_over=self.game_over)
        self.level_manager = LevelManager(
            self.score_system, on_bird_escape=self.score_system.deduct_health
        )
        self.ui_system = UISystem(self.font)

        self.menu = Menu()
        self.shop = Shop()

    def game_over(self):
        self.state = GameState.MAIN_MENU
        self.score_system.reset()
        self.level_manager.birds.clear()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if self.state == GameState.GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for bird in self.level_manager.birds:
                        if bird.rect.collidepoint(pos):
                            bird.get_damage(1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.MAIN_MENU

            elif self.state == GameState.MAIN_MENU:
                new_state = self.menu.handle_events(event)
                if new_state == GameState.GAME and self.state != GameState.GAME:
                    self.score_system.reset()
                    self.level_manager.birds.clear()
                self.state = new_state

            elif self.state == GameState.SHOP:
                self.state = self.shop.handle_events(event)

    def update(self):
        dt = self.clock.get_time()
        if self.state == GameState.MAIN_MENU:
            self.menu.update()
        elif self.state == GameState.SHOP:
            self.shop.update()
        elif self.state == GameState.GAME:
            self.level_manager.update(dt)

    def draw_game_world(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.trees, (0, 0))

        if self.state == GameState.GAME:
            self.level_manager.draw(self.screen)

        self.screen.blit(self.grass, (0, 0))
        self.screen.blit(self.scoreboard, (100, 490))

    def draw(self):
        self.draw_game_world()

        if self.state == GameState.GAME:
            pygame.mouse.set_visible(False)
            self.ui_system.draw_game_ui(
                self.screen, self.score_system.score, self.score_system.health
            )
            self.ui_system.draw_crosshair(self.screen)
        elif self.state == GameState.MAIN_MENU:
            pygame.mouse.set_visible(True)
            self.menu.draw(self.screen)
        elif self.state == GameState.SHOP:
            pygame.mouse.set_visible(True)
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
