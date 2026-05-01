import pygame
import sys

from persistence import (
    load_settings,
    save_settings,
    save_score
)

from ui import (
    draw_menu,
    draw_settings,
    draw_leaderboard,
    draw_game_over
)

from racer import (
    load_assets,
    reset_game,
    update_game,
    draw_game
)

pygame.init()
pygame.mixer.init()

W, H = 400, 600

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("TSIS 3 Racer")

clock = pygame.time.Clock()

settings = load_settings()

assets = load_assets(W, H)

# ---------------- MUSIC ----------------

pygame.mixer.music.load(
    "assets/background.wav"
)

pygame.mixer.music.play(-1)

# установка громкости при запуске

if settings["sound"]:

    pygame.mixer.music.set_volume(0.5)

    assets["coin_sound"].set_volume(1)

    assets["crash_sound"].set_volume(1)

else:

    pygame.mixer.music.set_volume(0)

    assets["coin_sound"].set_volume(0)

    assets["crash_sound"].set_volume(0)

# ---------------- STATES ----------------

MENU = 0
GAME = 1
GAME_OVER = 2
SETTINGS = 3
LEADERBOARD = 4

state = MENU

game = reset_game(assets)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # ---------------- MENU ----------------

        if state == MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    game = reset_game(assets)

                    state = GAME

                if event.key == pygame.K_2:

                    state = LEADERBOARD

                if event.key == pygame.K_3:

                    state = SETTINGS

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

        # ---------------- SETTINGS ----------------

        elif state == SETTINGS:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:

                    settings["sound"] = not settings["sound"]

                    save_settings(settings)

                    # управление громкостью

                    if settings["sound"]:

                        pygame.mixer.music.set_volume(0.5)

                        assets["coin_sound"].set_volume(1)

                        assets["crash_sound"].set_volume(1)

                    else:

                        pygame.mixer.music.set_volume(0)

                        assets["coin_sound"].set_volume(0)

                        assets["crash_sound"].set_volume(0)

                if event.key == pygame.K_ESCAPE:

                    state = MENU

        # ---------------- GAME OVER ----------------

        elif state == GAME_OVER:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    game = reset_game(assets)

                    state = GAME

                if event.key == pygame.K_m:

                    state = MENU

        # ---------------- LEADERBOARD ----------------

        elif state == LEADERBOARD:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    state = MENU

    # ---------------- GAME LOGIC ----------------

    if state == GAME:

        result = update_game(game)

        if result == "game_over":

            # crash звук

            assets["crash_sound"].play()

            save_score(
                "Player",
                game["score"],
                int(game["distance"])
            )

            state = GAME_OVER

    # ---------------- DRAW ----------------

    if state == MENU:

        draw_menu(screen)

    elif state == SETTINGS:

        draw_settings(screen, settings)

    elif state == LEADERBOARD:

        draw_leaderboard(screen)

    elif state == GAME:

        draw_game(screen, game)

    elif state == GAME_OVER:

        draw_game_over(
            screen,
            game["score"],
            int(game["distance"])
        )

    pygame.display.update()

    clock.tick(60)