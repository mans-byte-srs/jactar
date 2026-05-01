import pygame
import sys
import random
from datetime import datetime

import ui
import racer
import persistence
import sound
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
FPS           = 60

ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3
ROAD_LEFT  = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
GRAY   = (128, 128, 128)
DARK   = (30,  30,  60 )
GREEN  = (50,  200, 50 )
RED    = (220, 50,  50 )
YELLOW = (255, 220, 0  )
ORANGE = (255, 140, 0  )
CYAN   = (0,   200, 255)

DIFFICULTY_SPEEDS = {"easy": 3, "normal": 5, "hard": 7}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game — TSIS 3")
clock = pygame.time.Clock()

font       = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 46, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

road_offset = 0   

def draw_road():
    global road_offset
    road_offset = (road_offset + 5) % 40   # scroll speed

    screen.fill((34, 139, 34))   # grass
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    # Scrolling dashed lane dividers
    for y in range(-40 + road_offset, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + LANE_WIDTH - 2,     y, 4, 25))
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + 2 * LANE_WIDTH - 2, y, 4, 25))

    pygame.draw.line(screen, WHITE, (ROAD_LEFT,  0), (ROAD_LEFT,  SCREEN_HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 4)




def draw_hud(score, coins, total_value, distance, player, finish_dist):
    # Left column
    screen.blit(font.render(f"Score:  {score}",  True, WHITE),  (5, 10))
    screen.blit(font.render(f"Coins:  {coins}",  True, YELLOW), (5, 35))
    screen.blit(font.render(f"Value:  {total_value}", True, YELLOW), (5, 60))

    # Distance bar
    remaining = max(0, finish_dist - distance)
    screen.blit(font_small.render(f"Dist: {distance}m  Left: {remaining}m",
                                  True, WHITE), (5, 88))

    # Power-up status (right side)
    if player.shield:
        lbl = font.render("SHIELD", True, CYAN)
        screen.blit(lbl, (SCREEN_WIDTH - lbl.get_width() - 5, 10))
    if player.nitro:
        secs = player.nitro_timer // 60 + 1
        lbl = font.render(f"NITRO {secs}s", True, ORANGE)
        screen.blit(lbl, (SCREEN_WIDTH - lbl.get_width() - 5, 35))

def run_game(settings):
    username   = settings.get("username", "Player")
    diff       = settings.get("difficulty", "normal")
    snd_on     = settings.get("sound", False)
    base_speed = DIFFICULTY_SPEEDS[diff]
    finish_dist = {"easy": 3000, "normal": 2000, "hard": 1000}[diff]

    player = racer.Player(settings.get("car_color", "green"))

    # Enemies
    enemies = pygame.sprite.Group()
    for i in range(3):
        e = racer.Enemy(base_speed)
        e.rect.top -= i * 200
        enemies.add(e)

    # Coins
    coins_group = pygame.sprite.Group()
    for _ in range(3):
        coins_group.add(racer.Coin())

    # Obstacles
    obstacles = pygame.sprite.Group()
    for _ in range(2):
        obstacles.add(racer.Obstacle(base_speed))

    # Power-ups (one on screen at a time)
    powerups = pygame.sprite.Group()
    powerups.add(racer.PowerUp())

    score        = 0
    coins_count  = 0
    total_value  = 0
    distance     = 0
    oil_slow     = 0     
    bump_slow    = 0
    game_over    = False
    won          = False
    diff_timer   = 0     

    sound.play_music()   # start engine rumble
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound.stop_music()
                    return "menu", score, distance

        if not game_over and not won:
            # ── Difficulty scaling ──────────────────────────
            diff_timer += 1
            if diff_timer % (60 * 15) == 0:   # every 15 seconds
                for e in enemies:
                    e.boost(1)
                for o in obstacles:
                    o.speed = min(o.speed + 1, 12)
                # Spawn one more enemy
                if len(enemies) < 6:
                    ne = racer.Enemy(base_speed)
                    enemies.add(ne)

            # ── Slow effects ────────────────────────────────
            if oil_slow > 0:
                player.speed = max(2, player.base_speed - 3)
                oil_slow -= 1
                if oil_slow == 0:
                    player.speed = player.base_speed
            if bump_slow > 0:
                player.speed = max(2, player.base_speed - 1)
                bump_slow -= 1
                if bump_slow == 0:
                    player.speed = player.base_speed

            # ── Move everything ─────────────────────────────
            player.move()
            player.update_powerups()
            for e in enemies:   e.move()
            for c in coins_group: c.move()
            for o in obstacles: o.move()
            for p in powerups:  p.move()

            # Distance & score
            distance += 1
            score    += 1

            # ── Enemy collision ──────────────────────────────
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    if player.shield:
                        player.shield = False
                        e.respawn()
                    else:
                        sound.play("crash")
                        game_over = True

            # ── Obstacle collision ───────────────────────────
            for o in obstacles:
                if player.rect.colliderect(o.rect):
                    if o.kind == "barrier":
                        if player.shield:
                            player.shield = False
                            o.respawn()
                        else:
                            sound.play("crash")
                            game_over = True
                    elif o.kind == "oil":
                        oil_slow = 90     # 1.5 seconds
                        o.respawn()
                    elif o.kind == "bump":
                        bump_slow = 45
                        o.respawn()

            # ── Coin collection ──────────────────────────────
            for c in list(coins_group):
                if player.rect.colliderect(c.rect):
                    coins_count += 1
                    total_value += c.weight
                    score       += c.weight * 10
                    sound.play("coin")
                    c.respawn()
                    # Speed boost every 5 coins (Practice 11 rule)
                    if coins_count % 5 == 0:
                        for e in enemies:
                            e.boost(1)

            # ── Power-up collection ──────────────────────────
            for p in list(powerups):
                if player.rect.colliderect(p.rect):
                    if p.kind == "nitro":
                        player.activate_nitro()
                        score += 50
                        sound.play("nitro")
                    elif p.kind == "shield":
                        player.activate_shield()
                        score += 30
                        sound.play("shield")
                    elif p.kind == "repair":
                        player.repair()
                        oil_slow  = 0
                        bump_slow = 0
                        player.speed = player.base_speed
                        score += 20
                        sound.play("repair")
                    p.respawn()

            # ── Win condition ────────────────────────────────
            if distance >= finish_dist:
                won = True
                score += 500   # finish bonus

        # ── Draw ─────────────────────────────────────────────
        draw_road()
        for e in enemies:     screen.blit(e.image, e.rect)
        for o in obstacles:   screen.blit(o.image, o.rect)
        for p in powerups:    screen.blit(p.image, p.rect)
        for c in coins_group: screen.blit(c.image, c.rect)
        screen.blit(player.image, player.rect)
        draw_hud(score, coins_count, total_value, distance // 10,
                 player, finish_dist // 10)

        if game_over or won:
            sound.stop_music()
            sound.play("win" if won else "lose")
            result = "won" if won else "lost"
            action = _game_over_screen(score, distance // 10,
                                       coins_count, total_value, result)
            if action == "retry":
                return "retry", score, distance // 10
            elif action == "menu":
                return "menu", score, distance // 10

        pygame.display.flip()
        clock.tick(FPS)

    return "menu", score, distance // 10


def _game_over_screen(score, distance, coins, total_value, result):
    btn_retry = pygame.Rect(SCREEN_WIDTH // 2 - 110, 400, 100, 42)
    btn_menu  = pygame.Rect(SCREEN_WIDTH // 2 + 10,  400, 100, 42)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ui.button_clicked(btn_retry, event): return "retry"
            if ui.button_clicked(btn_menu,  event): return "menu"

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(190)
        screen.blit(overlay, (0, 0))

        title = "YOU WIN!" if result == "won" else "GAME OVER"
        color = YELLOW if result == "won" else RED
        lbl = font_large.render(title, True, color)
        screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 160))

        lines = [
            (f"Score:    {score}",       WHITE),
            (f"Distance: {distance} m",  WHITE),
            (f"Coins:    {coins}",        YELLOW),
            (f"Value:    {total_value}",  YELLOW),
        ]
        for i, (text, col) in enumerate(lines):
            lbl = font.render(text, True, col)
            screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 255 + i * 32))

        ui.draw_button(screen, btn_retry, "Retry")
        ui.draw_button(screen, btn_menu,  "Menu")
        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    btn_play   = pygame.Rect(SCREEN_WIDTH // 2 - 90, 230, 180, 50)
    btn_board  = pygame.Rect(SCREEN_WIDTH // 2 - 90, 300, 180, 50)
    btn_sett   = pygame.Rect(SCREEN_WIDTH // 2 - 90, 370, 180, 50)
    btn_quit   = pygame.Rect(SCREEN_WIDTH // 2 - 90, 440, 180, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ui.button_clicked(btn_play,  event): sound.play("click"); return "play"
            if ui.button_clicked(btn_board, event): sound.play("click"); return "leaderboard"
            if ui.button_clicked(btn_sett,  event): sound.play("click"); return "settings"
            if ui.button_clicked(btn_quit,  event):
                pygame.quit(); sys.exit()

        screen.fill(DARK)
        ui.draw_title(screen, "RACER", SCREEN_WIDTH, 100)
        lbl = font_small.render("TSIS 3", True, GRAY)
        screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 160))
        ui.draw_button(screen, btn_play,  "Play")
        ui.draw_button(screen, btn_board, "Leaderboard")
        ui.draw_button(screen, btn_sett,  "Settings")
        ui.draw_button(screen, btn_quit,  "Quit")
        pygame.display.flip()
        clock.tick(FPS)

def leaderboard_screen():
    btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 70, 555, 140, 38)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ui.button_clicked(btn_back, event): return

        screen.fill(DARK)
        ui.draw_title(screen, "TOP 10", SCREEN_WIDTH, 30)

        board = persistence.load_leaderboard()
        headers = ["#", "Name", "Score", "Dist"]
        col_x   = [15, 55, 215, 310]
        header_lbl = [font_small.render(h, True, YELLOW) for h in headers]
        for i, lbl in enumerate(header_lbl):
            screen.blit(lbl, (col_x[i], 100))
        pygame.draw.line(screen, GRAY, (10, 118), (385, 118), 1)

        for rank, entry in enumerate(board[:10], 1):
            y = 125 + (rank - 1) * 38
            color = YELLOW if rank == 1 else WHITE
            vals = [str(rank), entry["name"][:12],
                    str(entry["score"]), f"{entry['distance']}m"]
            for i, val in enumerate(vals):
                lbl = font_small.render(val, True, color)
                screen.blit(lbl, (col_x[i], y))

        if not board:
            lbl = font.render("No scores yet!", True, GRAY)
            screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 200))

        ui.draw_button(screen, btn_back, "Back")
        pygame.display.flip()
        clock.tick(FPS)

def settings_screen(settings):
    btn_sound  = pygame.Rect(230, 150, 140, 40)
    btn_color  = pygame.Rect(230, 220, 140, 40)
    btn_diff   = pygame.Rect(230, 290, 140, 40)
    btn_save   = pygame.Rect(SCREEN_WIDTH // 2 - 70, 390, 140, 42)
    btn_back   = pygame.Rect(SCREEN_WIDTH // 2 - 70, 450, 140, 42)

    colors_cycle = ["green", "blue", "yellow"]
    diffs_cycle  = ["easy", "normal", "hard"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ui.button_clicked(btn_sound, event):
                settings["sound"] = not settings["sound"]
                sound.set_enabled(settings["sound"])
                sound.play("click")   # audible confirmation if just turned ON
            if ui.button_clicked(btn_color, event):
                sound.play("click")
                idx = colors_cycle.index(settings["car_color"])
                settings["car_color"] = colors_cycle[(idx + 1) % len(colors_cycle)]
            if ui.button_clicked(btn_diff, event):
                sound.play("click")
                idx = diffs_cycle.index(settings["difficulty"])
                settings["difficulty"] = diffs_cycle[(idx + 1) % len(diffs_cycle)]
            if ui.button_clicked(btn_save, event):
                sound.play("click")
                persistence.save_settings(settings)
                lbl = font.render("Saved!", True, GREEN)
                screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 355))
                pygame.display.flip()
                pygame.time.wait(600)
            if ui.button_clicked(btn_back, event):
                sound.play("click")
                return settings

        screen.fill(DARK)
        ui.draw_title(screen, "Settings", SCREEN_WIDTH, 50)

        # Labels
        for text, y in [("Sound:", 160), ("Car Color:", 230), ("Difficulty:", 300)]:
            lbl = font.render(text, True, WHITE)
            screen.blit(lbl, (30, y))

        sound_val = "ON" if settings["sound"] else "OFF"
        ui.draw_button(screen, btn_sound, sound_val,
                       active=settings["sound"])
        ui.draw_button(screen, btn_color,
                       settings["car_color"].capitalize())
        ui.draw_button(screen, btn_diff,
                       settings["difficulty"].capitalize())
        ui.draw_button(screen, btn_save, "Save")
        ui.draw_button(screen, btn_back, "Back")

        pygame.display.flip()
        clock.tick(FPS)

def main():
    settings = persistence.load_settings()

    # Initialise sound engine using the saved preference
    sound.init(enabled=settings.get("sound", False))

    while True:
        action = main_menu()

        if action == "leaderboard":
            leaderboard_screen()

        elif action == "settings":
            settings = settings_screen(settings)

        elif action == "play":
            # Ask for username if not set
            if not settings.get("username"):
                name = ui.text_input_screen(screen, clock,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            "Type your name and press Enter")
                settings["username"] = name
                persistence.save_settings(settings)

            while True:
                result, score, distance = run_game(settings)
                # Save score
                persistence.save_score(settings["username"], score, distance)
                if result == "menu":
                    break
                # "retry" → loop back into run_game


if __name__ == "__main__":
    main()
