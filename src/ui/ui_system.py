import pygame
import os
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HEART_PATH,
    GREY_HEART_PATH,
    CROSSHAIR_PATH,
    FONT_PATH,
    WEAPONS_PATH
)


class UISystem:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.small_font = pygame.font.Font(FONT_PATH, 16)
        self.heart_full = pygame.image.load(HEART_PATH).convert_alpha()
        self.heart_empty = pygame.image.load(GREY_HEART_PATH).convert_alpha()
        self.crosshair = pygame.image.load(CROSSHAIR_PATH).convert_alpha()

        # Scale icons
        icon_size = (20, 20)
        self.heart_full = pygame.transform.scale(self.heart_full, icon_size)
        self.heart_empty = pygame.transform.scale(self.heart_empty, icon_size)
        self.crosshair = pygame.transform.scale(self.crosshair, (50, 50))

        self.weapon_images = {}
        weapon_files = {
            "Pistol": "pistol.png",
            "Revolver": "revolver.png",
            "Light Rifle": "light rifle.png",
            "Shotgun": "shotgun.png",
            "Rifle": "autonatic rifle.png"
        }

        for w_name, file_name in weapon_files.items():
            try:
                img = pygame.image.load(os.path.join(WEAPONS_PATH, file_name)).convert_alpha()
                ratio = 60 / img.get_width()
                w_height = int(img.get_height() * ratio)
                self.weapon_images[w_name] = pygame.transform.smoothscale(img, (60, w_height))
            except:
                self.weapon_images[w_name] = pygame.Surface((60, 40))

    def draw_health_ui(self, screen: pygame.Surface, health: int):
        for i in range(3):
            x_pos = 375 + (i * 20)
            y_pos = 545
            if i < health:
                screen.blit(self.heart_full, (x_pos, y_pos))
            else:
                screen.blit(self.heart_empty, (x_pos, y_pos))

    def draw_game_ui(self, screen: pygame.Surface, score: int, health: int, current_weapon):
        # Draw score
        score_text = self.font.render(f"{score}", False, (255, 255, 255))
        screen.blit(score_text, (140, 512))

        self.draw_health_ui(screen, health)
        if current_weapon.is_reloading:
            ammo_surf = self.small_font.render("......", True, (255, 0, 0))
        else:
            ammo_surf = self.small_font.render(f"{current_weapon.current_ammo} / {current_weapon.ammo_capacity}", True, (255, 255, 255))
        screen.blit(ammo_surf, (616, 530))

        if current_weapon.name in self.weapon_images:
            w_img = self.weapon_images[current_weapon.name]
            screen.blit(w_img, (550, 510))

    def draw_crosshair(self, screen: pygame.Surface):
        pos = pygame.mouse.get_pos()
        # Center the crosshair on the mouse position
        rect = self.crosshair.get_rect(center=pos)
        screen.blit(self.crosshair, rect)

    def draw_main_menu(self, screen: pygame.Surface):
        msg = self.font.render("GAME OVER - Press SPACE to Restart", True, (255, 0, 0))
        screen.blit(msg, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
