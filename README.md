# Small Games

A collection of 2D games I'm building in **Python with Pygame**. Every game can be
played **in the browser** on my website, and visitors can **suggest the next game**
I should build.

**Live site: [gandalfgames.netlify.app](https://gandalfgames.netlify.app)**

| Game | Status |
|---|---|
| Snake | Playable |
| Flappy Bird | Playable |
| Untitled Metroidvania (Hollow Knight-inspired) | In development |

---

## How it works (the big picture)

```
 Python game (snake/main.py)
        │
        │  pygbag  (tools/publish_game.py runs it)
        ▼
 Web version (site/games/snake/)  ── index.html + snake.tar.gz
        │
        │  shown inside an <iframe> on play.html
        ▼
 Website (site/)  ── hosted on Netlify, which also collects suggestions
```

1. **The games are normal Pygame programs.** You can run any of them on your
   computer with `python3 main.py`.
2. **pygbag turns a Pygame game into a web game.** Browsers can't run Python
   directly, but they can run **WebAssembly** (a fast, low-level format). pygbag
   packs the game's code and uses a version of Python that's been compiled to
   WebAssembly, so the exact same Python code runs inside the browser.
3. **The website is plain HTML, CSS and JavaScript** with no frameworks.
   - `games.json` is the list of games. The home page reads it and draws a card
     for each one, so adding a game means adding an entry, not editing HTML.
   - `play.html?id=snake` is one page that can play *any* game. It looks the
     id up in `games.json` and loads that game into an `<iframe>` (a page inside
     a page).
4. **The suggestion box uses Netlify Forms.** The `<form>` has
   `data-netlify="true"`, so Netlify (the host) saves every submission. They show
   up in the Netlify dashboard under **Forms**, and Netlify can email you each one.
   A hidden "honeypot" field catches spam bots.
5. **Deploying:** the code lives on GitHub. Netlify watches the GitHub repo, and
   every time new code is pushed, it publishes the `site/` folder
   (configured in `netlify.toml`).

## Folder guide

```
small games/
├── snake/                  Snake source code (Python)
│   ├── main.py             starts the game; the game loop
│   ├── game.py             rules: food, score, game over, drawing screens
│   ├── snake.py            the snake: moving, turning, growing
│   └── settings.py         colours, speed, board size: tweak these!
├── flappy_bird/            Flappy Bird source code (Python)
├── site/                   THE WEBSITE (this folder is what goes online)
│   ├── index.html          home page: intro, game cards, suggestion box
│   ├── play.html           the page that plays a game
│   ├── style.css           all the styling (colours are variables at the top)
│   ├── app.js              builds the game cards, sends the suggestion form
│   ├── play.js             loads the chosen game into the page
│   ├── games.json          the list of games (edit this to add one)
│   ├── images/             card pictures + site icon
│   └── games/              web versions of each game (made by pygbag)
├── tools/
│   └── publish_game.py     builds a game for the web + copies it into site/
└── netlify.toml            tells Netlify to publish the site/ folder
```

## Common tasks

**Play a game on your computer**
```bash
cd snake
python3 main.py
```

**Preview the website on your computer**
```bash
python3 -m http.server 8000 --directory site
```
Then open **http://127.0.0.1:8000**. Use `127.0.0.1`, not `localhost`: pygbag
treats `localhost` as its own test server and looks for files in the wrong place.
(The suggestion box only works on the live site.)

**Add a new game**
1. Make the game in its own folder with a `main.py` (see "Making a game
   web-ready" below).
2. Build it for the web:
   ```bash
   python3 tools/publish_game.py my_new_game
   ```
3. Add a picture at `site/images/my_new_game.png`.
4. Add an entry to `site/games.json` (copy an existing one and change it).
5. Publish:
   ```bash
   git add -A
   git commit -m "Add my new game"
   git push
   ```
   Netlify updates the live site within a minute.

**Read suggestions:** Netlify dashboard → your site → **Forms** → `suggestions`.

## Making a game web-ready (lessons learned)

These are the problems I ran into getting Pygame games to run in the browser:

| Problem | Why | Fix |
|---|---|---|
| Page froze | A browser can't run an endless `while True` loop; it needs control back every frame | Make the main loop `async` and call `await asyncio.sleep(0)` once per frame |
| Pygame never loaded | pygbag reads `main.py`'s `import` lines to decide what to download | Put `import pygame` in `main.py` itself |
| Flappy Bird crashed | `pygame.time.set_timer` isn't available in the browser | Track time with `pygame.time.get_ticks()` instead |
| tkinter window can't open | Browsers can't open desktop windows | Skip it when `sys.platform == "emscripten"` (the browser) |
| Visitors saw my high score | Every file in the game folder gets packed into the web version | Don't load the saved score in the browser |
| `pygbag` build hung | python.org's Python on macOS has no HTTPS certificates | Use the `certifi` package's certificates (`publish_game.py` does this) |

## Tech used

- **Python 3** and **pygame-ce** for the games
- **pygbag** to compile them to **WebAssembly** for the browser
- **HTML, CSS, JavaScript** (no frameworks) for the website
- **Netlify** for hosting and form handling, **GitHub** for the code
