# snake.py
import pygame
import settings

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        cx, cy = settings.COLS // 2, settings.ROWS // 2
        # body[0] is the head
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        # Key presses waiting to be used. A queue lets quick double-taps
        # (like UP then LEFT) both count instead of the second being lost.
        self.turns = []
        self.grow_pending = 0

    def turn(self, new_dir):
        last = self.turns[-1] if self.turns else self.direction
        # Can't reverse straight into yourself, and ignore repeats.
        if new_dir == last or (new_dir[0] == -last[0] and new_dir[1] == -last[1]):
            return
        if len(self.turns) < 3:
            self.turns.append(new_dir)

    def next_head(self):
        if self.turns:
            self.direction = self.turns.pop(0)
        hx, hy = self.body[0]
        return (hx + self.direction[0], hy + self.direction[1])

    def move(self, new_head):
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def hits_itself(self, pos):
        # The tail moves away this step unless we're growing, so it's safe.
        body = self.body if self.grow_pending else self.body[:-1]
        return pos in body

    def draw(self, screen):
        c = settings.CELL
        for i, (x, y) in enumerate(self.body):
            color = settings.snake_head_color if i == 0 else settings.snake_color
            rect = pygame.Rect(x * c + 1, y * c + 1 + settings.TOP_BAR, c - 2, c - 2)
            pygame.draw.rect(screen, color, rect, border_radius=6)

        # Eyes on the head, looking the way we're going
        hx, hy = self.body[0]
        dx, dy = self.direction
        center_x = hx * c + c // 2
        center_y = hy * c + c // 2 + settings.TOP_BAR
        # two eyes placed sideways to the direction of travel
        side_x, side_y = -dy, dx
        for s in (-1, 1):
            ex = center_x + dx * 4 + side_x * 5 * s
            ey = center_y + dy * 4 + side_y * 5 * s
            pygame.draw.circle(screen, (255, 255, 255), (ex, ey), 3)
            pygame.draw.circle(screen, (0, 0, 0), (ex + dx, ey + dy), 1)
