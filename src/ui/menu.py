import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState, ASSETS_DIR
from ui.button import Button

class Menu:
    def __init__(self):
        # Using a bold monospace font for pixel-like appearance
        font_name = "monospace"
        self.font = pygame.font.SysFont(font_name, 35, bold=True)
        self.title_font = pygame.font.SysFont(font_name, 90, bold=True)
        
        button_width = 250
        button_height = 70
        start_x = (SCREEN_WIDTH - button_width) // 2
        
        self.play_button = Button("PLAY GAME", start_x, 280, button_width, button_height, self.font, (34, 177, 76), (50, 220, 100))
        self.shop_button = Button("D-SHOP", start_x, 380, button_width, button_height, self.font, (63, 72, 204), (100, 110, 255))
        
        icon_path = os.path.join(ASSETS_DIR, "images", "interface", "DuckIcon.png")
        self.duck_icon = pygame.image.load(icon_path).convert_alpha()
        self.duck_icon = pygame.transform.scale(self.duck_icon, (80, 80))

    def handle_events(self, event: pygame.event.Event) -> GameState:
        if self.play_button.is_clicked(event):
            return GameState.GAME
        if self.shop_button.is_clicked(event):
            return GameState.SHOP
        return GameState.MAIN_MENU

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.update(mouse_pos)
        self.shop_button.update(mouse_pos)

    def draw(self, screen: pygame.Surface):
        # Slightly darkened overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110)) 
        screen.blit(overlay, (0, 0))

        # Title with shadow
        title_text = "DUCK HUNT"
        # Render without anti-aliasing for pixel look
        shadow_surf = self.title_font.render(title_text, False, (0, 0, 0))
        title_surf = self.title_font.render(title_text, False, (255, 255, 0))
        
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 140))
        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 6, 146))
        
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(title_surf, title_rect)
        
        # Decoration
        screen.blit(self.duck_icon, (title_rect.left - 100, title_rect.centery - 40))
        screen.blit(pygame.transform.flip(self.duck_icon, True, False), (title_rect.right + 20, title_rect.centery - 40))

        self.play_button.draw(screen)
        self.shop_button.draw(screen)
