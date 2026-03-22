import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState

class Shop:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 40)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        
    def handle_events(self, event: pygame.event.Event) -> GameState:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return GameState.MAIN_MENU
        return GameState.SHOP

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 200))
        screen.blit(overlay, (0, 0))

        # Title
        title_surf = self.title_font.render("SHOP", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Message
        msg_surf = self.font.render("Coming soon... Press ESC to go back", True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(msg_surf, msg_rect)
