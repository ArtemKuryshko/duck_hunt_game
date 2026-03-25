import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState, SHOPICON_PATH, WEAPONS_PATH

class Shop:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        
        raw_icon = pygame.image.load(SHOPICON_PATH).convert_alpha()
        self.icon_size = (150, 180)
        self.shop_icon = pygame.transform.smoothscale(raw_icon, self.icon_size)
        
        # Дані про предмети
        self.items = [
            {"name": "Pistol", "price": "0P", "image_name": "pistol.png"},
            {"name": "Revolver", "price": "100P", "image_name": "revolver.png"},
            {"name": "Light rifle", "price": "200P", "image_name": "light rifle.png"},
            {"name": "Shotgun", "price": "300P", "image_name": "shotgun.png"},
            {"name": "Automatic rifle", "price": "500P", "image_name": "autonatic rifle.png"}
        ]

        self.weapon_images = []
        for item in self.items:
            img_path = os.path.join(WEAPONS_PATH, item["image_name"])
            try:
                w_img = pygame.image.load(img_path).convert_alpha()
                w_width = 110 
                ratio = w_width / w_img.get_width()
                w_height = int(w_img.get_height() * ratio)
                
                scaled_weapon = pygame.transform.smoothscale(w_img, (w_width, w_height))
                self.weapon_images.append(scaled_weapon)
            except:
                self.weapon_images.append(pygame.Surface((1, 1)))

    def handle_events(self, event: pygame.event.Event) -> GameState:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return GameState.MAIN_MENU
        return GameState.SHOP

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 200))
        screen.blit(overlay, (0, 0))

        title_surf = self.title_font.render("SHOP", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 70))
        screen.blit(title_surf, title_rect)

        cols = 3
        gap_x, gap_y = 40, 30
        
        grid_w = (cols * self.icon_size[0]) + ((cols - 1) * gap_x)
        start_x = (SCREEN_WIDTH - grid_w) // 2
        start_y = 140

        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            
            x = start_x + col * (self.icon_size[0] + gap_x)
            y = start_y + row * (self.icon_size[1] + gap_y)
            
            screen.blit(self.shop_icon, (x, y))
            
            name_surf = self.font.render(item["name"], True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(x + self.icon_size[0] // 2, y + 30))
            screen.blit(name_surf, name_rect)

            weapon_img = self.weapon_images[i]
            weapon_rect = weapon_img.get_rect(center=(x + self.icon_size[0] // 2, y + self.icon_size[1] // 2))
            screen.blit(weapon_img, weapon_rect)
            
            price_surf = self.font.render(item["price"], True, (255, 215, 0))
            price_rect = price_surf.get_rect(center=(x + self.icon_size[0] // 2, y + self.icon_size[1] - 30))
            screen.blit(price_surf, price_rect)

        msg_surf = self.font.render("Press ESC to go back", True, (200, 200, 200))
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(msg_surf, msg_rect)