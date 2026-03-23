import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HEART_PATH,
    GREY_HEART_PATH,
    CROSSHAIR_PATH,
)


class UISystem:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.heart_full = pygame.image.load(HEART_PATH).convert_alpha()
        self.heart_empty = pygame.image.load(GREY_HEART_PATH).convert_alpha()
        self.crosshair = pygame.image.load(CROSSHAIR_PATH).convert_alpha()

        # Scale icons
        icon_size = (20, 20)
        self.heart_full = pygame.transform.scale(self.heart_full, icon_size)
        self.heart_empty = pygame.transform.scale(self.heart_empty, icon_size)
        self.crosshair = pygame.transform.scale(self.crosshair, (50, 50))

    def draw_health_ui(self, screen: pygame.Surface, health: int):
        for i in range(3):
            x_pos = 375 + (i * 20)
            y_pos = 545
            if i < health:
                screen.blit(self.heart_full, (x_pos, y_pos))
            else:
                screen.blit(self.heart_empty, (x_pos, y_pos))

    def draw_game_ui(self, screen: pygame.Surface, score: int, health: int):
        # Draw score
        score_text = self.font.render(f"{score}", False, (255, 255, 255))
        screen.blit(score_text, (240, 540))

        self.draw_health_ui(screen, health)

    def draw_crosshair(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        # Center the crosshair on the mouse position
        rect = self.crosshair.get_rect(center=pos)
        screen.blit(self.crosshair, rect)

    def draw_main_menu(self, screen: pygame.Surface):
        msg = self.font.render("GAME OVER - Press SPACE to Restart", True, (255, 0, 0))
        screen.blit(msg, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
