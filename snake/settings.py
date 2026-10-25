# settings.py
# Change these numbers to tweak the game.

# Grid
CELL = 24          # size of one square, in pixels
COLS = 25          # squares across
ROWS = 20          # squares down
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS + 40   # extra 40px at the top for the score bar
TOP_BAR = 40

# Speed (moves per second)
START_SPEED = 8
SPEED_UP_EVERY = 5   # speed up after every 5 apples
MAX_SPEED = 20

# Colours (R, G, B)
bg_color = (20, 24, 32)
grid_color = (28, 33, 43)
snake_color = (80, 200, 120)
snake_head_color = (120, 230, 150)
food_color = (230, 70, 70)
text_color = (240, 240, 240)
bar_color = (12, 14, 20)

# Draw faint grid lines?
SHOW_GRID = True
