import pygame
import sys
from config import *

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.background = pygame.image.load(BG_PATH).convert()
        self.trees = pygame.image.load(TREES_PATH).convert_alpha()
        self.grass = pygame.image.load(GRASS_PATH).convert_alpha()

    def process_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.trees, (0, 0))
        self.screen.blit(self.grass, (0, 0))
        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS) # Контроль кадрів через константу
        
        pygame.quit()
        sys.exit()