# game.py
import asyncio
import pygame
import sys
import settings
from bird import Bird
from pipe import Pipe

async def run_game():   # async so it can also run in a web browser
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    try:
        pygame.display.set_icon(pygame.image.load("assets/icon.ico"))
    except Exception:
        pass

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36, bold=True)
    small = pygame.font.SysFont("Arial", 22)

    # A new pipe every PIPE_INTERVAL milliseconds. (pygame.time.set_timer
    # doesn't work in the browser, so we keep track of the time ourselves.)
    last_pipe_time = pygame.time.get_ticks()

    def new_game():
        return Bird(), [], 0, False

    bird, pipes, score, dead = new_game()

    while True:
        clock.tick(settings.FPS)
        screen.fill(settings.bg_color)

        # Ground
        ground_h = 60
        pygame.draw.rect(screen, settings.ground_color,
                         (0, settings.HEIGHT - ground_h,
                          settings.WIDTH, ground_h))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dead:
                        bird, pipes, score, dead = new_game()
                    else:
                        bird.flap()
            if event.type == pygame.MOUSEBUTTONDOWN and dead:
                bird, pipes, score, dead = new_game()

        now = pygame.time.get_ticks()
        if now - last_pipe_time >= settings.PIPE_INTERVAL:
            last_pipe_time = now
            if not dead:
                pipes.append(Pipe(settings.WIDTH + 10))

        if not dead:
            bird.update()
            bird_rect = bird.get_rect()

            # Floor / ceiling
            if bird.y > settings.HEIGHT - ground_h or bird.y < 0:
                dead = True

            for pipe in pipes:
                pipe.update()
                if pipe.collides(bird_rect):
                    dead = True
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1

            pipes = [p for p in pipes if not p.off_screen()]

        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)

        # Score
        score_surf = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_surf, (settings.WIDTH // 2 - score_surf.get_width() // 2, 30))

        if dead:
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT),
                                     pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            over = font.render("Game Over", True, (255, 80, 80))
            hint = small.render("Press SPACE or click to retry", True, (220, 220, 220))
            screen.blit(over, (settings.WIDTH//2 - over.get_width()//2, 220))
            screen.blit(hint, (settings.WIDTH//2 - hint.get_width()//2, 280))

        pygame.display.flip()
        await asyncio.sleep(0)   # let the browser update the page