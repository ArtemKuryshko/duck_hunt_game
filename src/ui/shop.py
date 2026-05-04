import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState, SHOPICON_PATH, WEAPONS_PATH

class Shop:
    def __init__(self, point_manager, inventory_manager):
        self.point_manager = point_manager
        self.inventory_manager = inventory_manager
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        
        raw_icon = pygame.image.load(SHOPICON_PATH).convert_alpha()
        self.icon_size = (150, 180)
        self.shop_icon = pygame.transform.smoothscale(raw_icon, self.icon_size)
        
        self.items = [
            {"name": "Pistol", "price": 0, "image_name": "pistol.png"},
            {"name": "Revolver", "price": 100, "image_name": "revolver.png"},
            {"name": "Light rifle", "price": 200, "image_name": "light rifle.png"},
            {"name": "Shotgun", "price": 300, "image_name": "shotgun.png"},
            {"name": "Automatic rifle", "price": 500, "image_name": "autonatic rifle.png"}
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

        # Зони кліку для мишки
        self.item_rects = []
        cols = 3
        gap_x, gap_y = 40, 30
        grid_w = (cols * self.icon_size[0]) + ((cols - 1) * gap_x)
        start_x = (SCREEN_WIDTH - grid_w) // 2
        start_y = 140

        for i in range(len(self.items)):
            col = i % cols
            row = i // cols
            x = start_x + col * (self.icon_size[0] + gap_x)
            y = start_y + row * (self.icon_size[1] + gap_y)
            self.item_rects.append(pygame.Rect(x, y, self.icon_size[0], self.icon_size[1]))

    def handle_events(self, event: pygame.event.Event) -> GameState:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return GameState.MAIN_MENU
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            for i, rect in enumerate(self.item_rects):
                if rect.collidepoint(mouse_pos):
                    item = self.items[i]
                    name = item["name"]
                    price = item["price"]
                    

                    if name in self.inventory_manager.unlocked_weapons:
                        self.inventory_manager.equip_weapon(name)
                    else:
                        if self.point_manager.spend_points(price):
                            self.inventory_manager.unlock_weapon(name)
                            self.inventory_manager.equip_weapon(name)
                            
        return GameState.SHOP
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, rect in enumerate(self.item_rects):
                if rect.collidepoint(mouse_pos):
                    item = self.items[i]
                    name = item["name"]
                    price = item["price"]

                    # Логіка інвентарю та покупок
                    if name in self.inventory_manager.unlocked_weapons:
                        self.inventory_manager.equip_weapon(name)
                    else:
                        if self.point_manager.spend_points(price):
                            self.inventory_manager.unlock_weapon(name)
                            self.inventory_manager.equip_weapon(name)
        
        return GameState.SHOP

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 200))
        screen.blit(overlay, (0, 0))

        # Баланс
        balance_surf = self.font.render(f"Points: {self.point_manager.points} P", True, (255, 255, 255))
        screen.blit(balance_surf, (20, 20))

        title_surf = self.title_font.render("SHOP", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 70))
        screen.blit(title_surf, title_rect)

        for i, item in enumerate(self.items):
            rect = self.item_rects[i]
            x, y = rect.x, rect.y
            
            screen.blit(self.shop_icon, (x, y))
            
            name_surf = self.font.render(item["name"], True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(x + self.icon_size[0] // 2, y + 30))
            screen.blit(name_surf, name_rect)

            weapon_img = self.weapon_images[i]
            weapon_rect = weapon_img.get_rect(center=(x + self.icon_size[0] // 2, y + self.icon_size[1] // 2))
            screen.blit(weapon_img, weapon_rect)
            
            # Відображення статусів на основі даних з InventoryManager
            if item["name"] == self.inventory_manager.current_weapon:
                status_text = "EQUIPPED"
                status_color = (0, 255, 0)
            elif item["name"] in self.inventory_manager.unlocked_weapons:
                status_text = "OWNED"
                status_color = (200, 200, 200)
            else:
                status_text = f"{item['price']} P"
                status_color = (255, 215, 0) if self.point_manager.points >= item["price"] else (255, 50, 50)

            price_surf = self.font.render(status_text, True, status_color)
            price_rect = price_surf.get_rect(center=(x + self.icon_size[0] // 2, y + self.icon_size[1] - 30))
            screen.blit(price_surf, price_rect)

        msg_surf = self.font.render("Press ESC to go back", True, (200, 200, 200))
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(msg_surf, msg_rect)