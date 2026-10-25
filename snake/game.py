# game.py
import os
import random
import sys
import pygame
import settings
from snake import Snake, UP, DOWN, LEFT, RIGHT

try:
    HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")
except NameError:   # in the browser __file__ may not exist
    HIGH_SCORE_FILE = "highscore.txt"

KEY_DIRS = {
    pygame.K_UP: UP, pygame.K_w: UP,
    pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
}


def load_high_score():
    # In the browser every visitor starts fresh (sys.platform is "emscripten"
    # there), so they don't see the best score saved on your own computer.
    if sys.platform == "emscripten":
        return 0
    try:
        with open(HIGH_SCORE_FILE) as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.high_score = load_high_score()
        self.reset()
        self.state = "start"   # "start", "playing", "paused", "over"

    def reset(self):
        self.snake = Snake()
        self.score = 0
        self.speed = settings.START_SPEED
        self.move_timer = 0.0
        self.food = self.place_food()

    def place_food(self):
        free = [(x, y) for x in range(settings.COLS) for y in range(settings.ROWS)
                if (x, y) not in self.snake.body]
        return random.choice(free) if free else None

    # ---------- input ----------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        if self.state == "start":
            if key in KEY_DIRS or key == pygame.K_SPACE:
                self.state = "playing"
                if key in KEY_DIRS:
                    self.snake.turn(KEY_DIRS[key])
        elif self.state == "playing":
            if key in KEY_DIRS:
                self.snake.turn(KEY_DIRS[key])
            elif key in (pygame.K_p, pygame.K_ESCAPE):
                self.state = "paused"
        elif self.state == "paused":
            if key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_SPACE):
                self.state = "playing"
        elif self.state == "over":
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self.reset()
                self.state = "playing"

    # ---------- update ----------
    def update(self, dt):
        if self.state != "playing":
            return
        self.move_timer += dt
        step_time = 1.0 / self.speed
        while self.move_timer >= step_time and self.state == "playing":
            self.move_timer -= step_time
            self.step()

    def step(self):
        new_head = self.snake.next_head()
        x, y = new_head
        hit_wall = not (0 <= x < settings.COLS and 0 <= y < settings.ROWS)
        if hit_wall or self.snake.hits_itself(new_head):
            self.game_over()
            return

        self.snake.move(new_head)

        if new_head == self.food:
            self.score += 1
            self.snake.grow()
            if self.score % settings.SPEED_UP_EVERY == 0:
                self.speed = min(self.speed + 1, settings.MAX_SPEED)
            self.food = self.place_food()
            if self.food is None:   # filled the whole board!
                self.game_over()

    def game_over(self):
        self.state = "over"
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    # ---------- drawing ----------
    def draw(self):
        s = self.screen
        c = settings.CELL
        s.fill(settings.bg_color)

        if settings.SHOW_GRID:
            for x in range(settings.COLS + 1):
                pygame.draw.line(s, settings.grid_color,
                                 (x * c, settings.TOP_BAR), (x * c, settings.HEIGHT))
            for y in range(settings.ROWS + 1):
                yy = y * c + settings.TOP_BAR
                pygame.draw.line(s, settings.grid_color, (0, yy), (settings.WIDTH, yy))

        if self.food:
            fx, fy = self.food
            center = (fx * c + c // 2, fy * c + c // 2 + settings.TOP_BAR)
            pygame.draw.circle(s, settings.food_color, center, c // 2 - 3)
            # little leaf
            pygame.draw.ellipse(s, (90, 180, 90),
                                (center[0], center[1] - c // 2 + 1, 7, 5))

        self.snake.draw(s)

        # Score bar
        pygame.draw.rect(s, settings.bar_color, (0, 0, settings.WIDTH, settings.TOP_BAR))
        self.text(f"Score: {self.score}", 12, 9, center=False)
        best = self.font.render(f"Best: {self.high_score}", True, settings.text_color)
        s.blit(best, (settings.WIDTH - best.get_width() - 12, 9))

        if self.state == "start":
            self.overlay("SNAKE", "Arrow keys or WASD to start")
        elif self.state == "paused":
            self.overlay("PAUSED", "Press P to keep going")
        elif self.state == "over":
            self.overlay("GAME OVER", f"Score {self.score}  -  Space to play again")

    def text(self, msg, x, y, center=True, font=None):
        surf = (font or self.font).render(msg, True, settings.text_color)
        if center:
            x -= surf.get_width() // 2
        self.screen.blit(surf, (x, y))

    def overlay(self, title, subtitle):
        shade = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        self.screen.blit(shade, (0, 0))
        mid = settings.WIDTH // 2
        self.text(title, mid, settings.HEIGHT // 2 - 50, font=self.big_font)
        self.text(subtitle, mid, settings.HEIGHT // 2 + 10)
