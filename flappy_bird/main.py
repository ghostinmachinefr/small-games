# main.py
import asyncio
import sys
import pygame  # not used here, but pygbag reads main.py's imports to know it must load pygame in the browser
from game import run_game

# In a web browser sys.platform is "emscripten". The tkinter customizer
# window can't open there, so the web version uses the default colours.
IN_BROWSER = sys.platform == "emscripten"

if not IN_BROWSER:
    from customizer import run_customizer
    run_customizer()   # show customisation window first

asyncio.run(run_game())   # then launch the game
