# bird.py
import pygame
import settings

class Bird:
    def __init__(self):
        self.x = 100
        self.y = settings.HEIGHT // 2
        self.vel = 0
        self.size = 34

    def flap(self):
        self.vel = settings.FLAP_STRENGTH

    def update(self):
        self.vel += settings.GRAVITY
        self.y += self.vel

    def draw(self, screen):
        color = settings.bird_color
        r = self.size // 2
        cx, cy = int(self.x), int(self.y)

        if settings.bird_shape == "round":
            pygame.draw.circle(screen, color, (cx, cy), r)
            # eye
            pygame.draw.circle(screen, (255,255,255),
                                (cx + r//2, cy - r//4), r//4)
            pygame.draw.circle(screen, (0,0,0),
                                (cx + r//2, cy - r//4), r//8)
            # beak
            pygame.draw.polygon(screen, (255,165,0), [
                (cx + r, cy),
                (cx + r + 10, cy + 4),
                (cx + r, cy + 8)
            ])
        else:
            rect = pygame.Rect(cx - r, cy - r, self.size, self.size)
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.circle(screen, (255,255,255),
                                (cx + r//2, cy - r//4), r//4)
            pygame.draw.circle(screen, (0,0,0),
                                (cx + r//2, cy - r//4), r//8)

    def get_rect(self):
        r = self.size // 2
        return pygame.Rect(self.x - r, self.y - r, self.size, self.size)