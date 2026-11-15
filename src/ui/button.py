import pygame


class Button:
    def __init__(self, text: str, x: int, y: int, width: int, height: int, font: pygame.font.Font, color: tuple, hover_color: tuple):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

        self.border_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

    def draw(self, screen: pygame.Surface):
        current_color = self.hover_color if self.is_hovered else self.color

        # Retro shadow
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(5, 5)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect)

        # Main button
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 4)

        # Render without anti-aliasing for pixel look
        text_surf = self.font.render(self.text, False, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos: tuple):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
