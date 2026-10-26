# Daily Game Bot: Plan

A scheduled Claude task on my Mac runs every day around **12:10 PM**. Each run does
**one step** from this file, tests it, commits it, and pushes it to GitHub.
Netlify then updates the live site. One game takes **4 days** (4 steps).

**To steer the bot, just edit this file:** reorder the queue, add or remove games,
or change the steps. The bot always follows what this file says.

---

## Rules the bot follows

1. **One step per day.** Do the next unchecked step only, then stop.
2. **Unfinished games stay unplayable.** From Step 1 a game appears on the site as
   a "coming soon" card (`"status": "in-progress"` in `site/games.json`). It only
   becomes `"playable"` in Step 4, once it has been built and tested.
3. **Every step leaves the game working.** Before committing, run
   `python3 tools/smoke_test.py <game_folder>`. It must print `PASS`.
4. **Follow the house style** of `snake/`: `main.py` (async game loop with
   `await asyncio.sleep(0)` every frame and `import pygame` in `main.py`),
   `settings.py` (colours, sizes, speeds), and separate files for the main
   objects. Short, friendly comments that explain *why*. No popup windows
   (tkinter etc.) and no `pygame.time.set_timer`. Use `pygame.time.get_ticks()`.
   High scores are saved to `highscore.txt` on desktop only, never loaded in the
   browser (`sys.platform == "emscripten"`).
5. **Don't touch the finished games** (`snake/`, `flappy_bird/`) or anything not
   listed in the step, except this file and the README games table.
6. **If something goes wrong** (test fails and can't be fixed, push fails, files
   changed that the bot didn't make): don't push. Write what happened in the log
   below and stop.

## Steps for every game

- **Step 1: Start.** Create `<game>/` with `main.py`, `settings.py` and the
  basic screen: window, background, the player/main object drawn and moving
  with the keyboard. A start screen ("Press Space to start"). Add a
  `"status": "in-progress"` card for it to `site/games.json`, and add it to the
  README games table as "In development".
- **Step 2: Rules.** The main gameplay: the challenge (enemies, ball, falling
  pieces, whatever this game needs), collisions, and scoring.
- **Step 3: Finish.** Game over screen, restart with Space, pause with P,
  high score, difficulty that ramps up, and polish (colours, little effects).
- **Step 4: Publish.** Run `python3 tools/publish_game.py <game>`. Make the card
  picture with `python3 tools/smoke_test.py <game> --screenshot
  site/images/<game>.png` (use `--frames` to catch a nice moment). In
  `site/games.json` set `"status": "playable"` and fill in `description`,
  `tags`, `thumbnail`, `path`, `width`, `height`, `controls` and `added`
  (today's date). Mark it "Playable" in the README table. Check the site
  locally with `python3 -m http.server 8000 --directory site` (open
  `http://127.0.0.1:8000`, not localhost).

---

## Game queue

Work top to bottom. When a game's 4 steps are done, move to the next one.

| # | Game | Folder | Idea |
|---|---|---|---|
| 1 | Pong | `pong/` | Player vs computer paddle. First to 7 wins. |
| 2 | Breakout | `breakout/` | Paddle and ball, break rows of bricks, 3 lives. |
| 3 | Dino Runner | `dino_runner/` | Endless runner: jump over cacti, duck under birds. |
| 4 | 2048 | `game_2048/` | Slide tiles with the arrow keys, merge matching numbers. |
| 5 | Space Invaders | `space_invaders/` | Rows of aliens move down. Shoot them before they land. |
| 6 | Memory Match | `memory_match/` | Flip cards with the mouse to find pairs, fewest moves wins. |
| 7 | Minesweeper | `minesweeper/` | Classic grid. Left click to reveal, right click to flag. |
| 8 | Asteroids | `asteroids/` | Rotate, thrust and shoot rocks that split apart. |
| 9 | Tetris | `tetris/` | Falling blocks, clear lines, gets faster. |

(The Hollow Knight-style Metroidvania is my own project. The bot leaves it alone.)

## Current progress

**Current game:** Pong (`pong/`)

- [ ] Step 1: Start
- [ ] Step 2: Rules
- [ ] Step 3: Finish
- [ ] Step 4: Publish

## Log

The bot adds one line per run: date, game, step, and what it did.

- 2026-10-26 (setup, not a bot run): Created this plan + `tools/smoke_test.py`. First game: Pong.
