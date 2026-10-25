# main.py  -  run this file to play:  python3 main.py
#
# Why "async"?  This same file also runs inside a web browser (via pygbag).
# A browser can only do one thing at a time, so every frame we must hand
# control back to it with `await asyncio.sleep(0)` - otherwise the page freezes.
# On your Mac this changes nothing; the game plays the same.
import asyncio
import pygame
import settings
from game import Game


async def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0   # seconds since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        game.update(dt)
        game.draw()
        pygame.display.flip()
        await asyncio.sleep(0)         # let the browser breathe

    pygame.quit()


asyncio.run(main())
