"""
smoke_test.py - check that a game starts and runs without crashing.

Usage (from the "small games" folder):
    python3 tools/smoke_test.py snake
    python3 tools/smoke_test.py snake --screenshot site/images/snake.png

  It gives up after 60 seconds, so a game that waits for a popup window
  (like Flappy Bird's customizer) fails instead of hanging.

What it does:
  Runs the game's main.py with no visible window (SDL's "dummy" driver) for a
  few seconds' worth of frames. If the game crashes, it prints the error and
  exits with code 1. If it keeps running, it passes.
  With --screenshot, it also saves the last frame as a picture (handy for the
  card image on the website).
"""
import argparse
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # the "small games" folder


class _Done(BaseException):
    """Raised from inside the game loop to stop it once we've seen enough."""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("game", help="game folder name, e.g. snake")
    parser.add_argument("--frames", type=int, default=180,
                        help="how many frames to run (default 180, about 3 seconds)")
    parser.add_argument("--screenshot", help="save the last frame to this .png path")
    args = parser.parse_args()

    game_dir = ROOT / args.game.strip("/")
    main_py = game_dir / "main.py"
    if not main_py.exists():
        print(f"FAIL: can't find {main_py}")
        sys.exit(1)

    # No real window or sound needed.
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

    import pygame

    # Count frames by wrapping pygame.display.flip / update.
    frames = {"n": 0}
    real_flip, real_update = pygame.display.flip, pygame.display.update

    def counted(real):
        def wrapper(*a, **kw):
            result = real(*a, **kw)
            frames["n"] += 1
            if frames["n"] >= args.frames:
                if args.screenshot:
                    out = Path(args.screenshot)
                    out.parent.mkdir(parents=True, exist_ok=True)
                    pygame.image.save(pygame.display.get_surface(), str(out))
                raise _Done
            return result
        return wrapper

    pygame.display.flip = counted(real_flip)
    pygame.display.update = counted(real_update)

    # Run the game as if started with "python3 main.py" from its own folder.
    os.chdir(game_dir)
    sys.path.insert(0, str(game_dir))
    try:
        runpy.run_path(str(main_py), run_name="__main__")
    except _Done:
        msg = f"PASS: {args.game} ran {frames['n']} frames without crashing"
        if args.screenshot:
            msg += f"; screenshot saved to {args.screenshot}"
        print(msg)
        return
    except SystemExit:
        pass
    except Exception:
        import traceback
        traceback.print_exc()
        print(f"FAIL: {args.game} crashed after {frames['n']} frames")
        sys.exit(1)

    # main.py returned on its own before reaching the frame count.
    print(f"FAIL: {args.game} stopped by itself after {frames['n']} frames "
          f"(expected it to keep running for {args.frames})")
    sys.exit(1)


def run_with_time_limit(seconds=60):
    """Run the test in a child process so a game that waits forever (for
    example a desktop popup window before the game starts) fails instead of
    hanging."""
    import subprocess
    env = dict(os.environ, _SMOKE_TEST_CHILD="1")
    try:
        result = subprocess.run([sys.executable, __file__, *sys.argv[1:]],
                                env=env, timeout=seconds)
    except subprocess.TimeoutExpired:
        print(f"FAIL: still waiting after {seconds}s - does the game open a "
              "window or wait for input before its game loop starts?")
        sys.exit(1)
    sys.exit(result.returncode)


if __name__ == "__main__":
    if os.environ.get("_SMOKE_TEST_CHILD"):
        main()
    else:
        run_with_time_limit()
