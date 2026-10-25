# pipe.py
import pygame
import random
import settings

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, settings.HEIGHT - 200)
        self.width = 60
        self.passed = False

    def update(self):
        self.x -= settings.PIPE_SPEED

    def draw(self, screen):
        color = settings.pipe_color
        half = settings.PIPE_GAP // 2
        # Top pipe
        top_rect = pygame.Rect(self.x, 0, self.width,
                               self.gap_y - half)
        pygame.draw.rect(screen, color, top_rect, border_radius=6)
        # Bottom pipe
        bot_rect = pygame.Rect(self.x, self.gap_y + half,
                               self.width,
                               settings.HEIGHT - (self.gap_y + half))
        pygame.draw.rect(screen, color, bot_rect, border_radius=6)

    def collides(self, bird_rect):
        half = settings.PIPE_GAP // 2
        top = pygame.Rect(self.x, 0, self.width, self.gap_y - half)
        bot = pygame.Rect(self.x, self.gap_y + half, self.width,
                          settings.HEIGHT)
        return top.colliderect(bird_rect) or bot.colliderect(bird_rect)

    def off_screen(self):
        return self.x + self.width < 0