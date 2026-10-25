"""
publish_game.py - put a Pygame game on the website.

Usage (from the "small games" folder):
    python3 tools/publish_game.py snake

What it does:
  1. Runs pygbag to turn the game folder into a web version (game/build/web).
  2. Copies that web version into site/games/<name>/ so the website can load it.

After running it, if this is a NEW game, also:
  - add an entry for it in site/games.json
  - add a picture for its card at site/images/<name>.png
Then save your changes with git and push; Netlify puts the update online.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # the "small games" folder


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tools/publish_game.py <game-folder>")
        sys.exit(1)

    name = sys.argv[1].strip("/")
    game_dir = ROOT / name
    if not (game_dir / "main.py").exists():
        print(f"Can't find {game_dir / 'main.py'} - is the folder name right?")
        sys.exit(1)

    # The python.org version of Python on macOS doesn't know about web
    # security certificates by default, so point it at the ones from certifi.
    env = dict(os.environ)
    try:
        import certifi
        env.setdefault("SSL_CERT_FILE", certifi.where())
    except ImportError:
        pass

    print(f"1/2  Building the web version of '{name}' with pygbag...")
    subprocess.run([sys.executable, "-m", "pygbag", "--build", str(game_dir)],
                   check=True, env=env)

    built = game_dir / "build" / "web"
    target = ROOT / "site" / "games" / name
    print(f"2/2  Copying {built.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(built, target)

    print("\nDone! Next steps:")
    print(f"  - New game? Add it to site/games.json and add site/images/{name}.png")
    print("  - Test:  python3 -m http.server 8000 --directory site")
    print("           then open http://127.0.0.1:8000  (use 127.0.0.1, not localhost)")
    print("  - Publish:  git add -A && git commit -m \"Add/update " + name + "\" && git push")


if __name__ == "__main__":
    main()
