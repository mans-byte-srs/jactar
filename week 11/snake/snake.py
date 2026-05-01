import pygame
import random
import sys
import os

pygame.init()

# Sizes
CELL = 40
COLS = 20
ROWS = 16
W = COLS * CELL
H = ROWS * CELL + 60  # +60 for the score panel

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Tax")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)
font_big = pygame.font.SysFont("consolas", 44, bold=True)

# Image loading
def load(name):
    for ext in [".png", ".jpg", ".jpeg", ".bmp"]:
        path = os.path.join("images", name + ext)
        if os.path.isfile(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, (CELL, CELL))
    return None

img_head = load("head")
img_body = load("body")
img_food = load("food")

# Draw function
def draw_cell(x, y, img, color):
    rx = x * CELL
    ry = y * CELL + 60
    if img:
        screen.blit(img, (rx, ry))
    else:
        pygame.draw.rect(screen, color, (rx + 2, ry + 2, CELL - 4, CELL - 4), border_radius=6)

# Head rotation angle
def angle(d):
    return {(1,0): 270, (-1,0): 90, (0,-1): 0, (0,1): 180}[d]

# --- NEW LOGIC: SPAWN FOOD WITH WEIGHT AND TIMER ---
def spawn_food(snake):
    free = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in snake]
    pos = random.choice(free)
    
    # Task 1: Random weight (e.g., 1 to 3)
    weight = random.randint(1, 3)
    
    # Task 2: Store creation time (in milliseconds)
    spawn_time = pygame.time.get_ticks()
    
    # We return a dictionary to keep track of all food properties
    return {
        "pos": pos,
        "weight": weight,
        "spawn_time": spawn_time,
        "timer": 5000  # Food disappears after 5 seconds
    }

def new_game():
    cx, cy = COLS // 2, ROWS // 2
    snake = [(cx, cy), (cx-1, cy), (cx-2, cy)]
    direction = (1, 0)
    food = spawn_food(snake)
    return snake, direction, food, 0

# Initial setup
snake, direction, food, score = new_game()
next_dir = direction
hi = 0
alive = True
speed = 150 
last_move = pygame.time.get_ticks()

# Main Loop
while True:
    now = pygame.time.get_ticks() # Current time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            keys = {
                pygame.K_UP: (0,-1), pygame.K_w: (0,-1),
                pygame.K_DOWN: (0,1), pygame.K_s: (0,1),
                pygame.K_LEFT: (-1,0), pygame.K_a: (-1,0),
                pygame.K_RIGHT: (1,0), pygame.K_d: (1,0),
            }
            if event.key in keys:
                nd = keys[event.key]
                if nd[0] + direction[0] != 0 or nd[1] + direction[1] != 0:
                    next_dir = nd
            if event.key == pygame.K_r and not alive:
                snake, direction, food, score = new_game()
                next_dir = direction
                alive = True
                speed = 150

    # --- TASK: DISAPPEARING FOOD TIMER ---
    if alive:
        # If current time - spawn time > food life duration
        if now - food["spawn_time"] > food["timer"]:
            food = spawn_food(snake) # Spawn new food elsewhere

    # Movement by timer
    if alive and now - last_move > speed:
        last_move = now
        direction = next_dir
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Wall/Body collision check
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in snake[:-1]:
            alive = False
        else:
            snake.insert(0, head)
            # Check if head reaches food position
            if head == food["pos"]:
                # --- TASK: APPLY WEIGHT TO SCORE ---
                score += 10 * food["weight"] 
                hi = max(hi, score)
                food = spawn_food(snake)
                speed = max(60, speed - 3) 
            else:
                snake.pop()

    # --- DRAWING ---
    screen.fill((15, 20, 30))

    # Score Panel
    screen.blit(font.render(f"Счёт: {score}", True, (90, 230, 140)), (16, 18))
    screen.blit(font.render(f"Рекорд: {hi}", True, (150, 170, 150)), (200, 18))
    
    # Task: Visualize the food timer on screen
    time_left = max(0, (food["timer"] - (now - food["spawn_time"])) // 1000)
    screen.blit(font.render(f"Еда исчезнет через: {time_left}с", True, (255, 100, 100)), (W - 350, 36))

    # Grid
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, (22, 30, 42),
                (c*CELL+1, r*CELL+61, CELL-2, CELL-2), border_radius=4)

    # Food rendering
    # Different weights can be visualized by changing colors or drawing text
    food_color = (220, 60, 60) if food["weight"] == 1 else (255, 215, 0) # Gold if heavy
    draw_cell(food["pos"][0], food["pos"][1], img_food, food_color)
    
    # Draw weight number on the food
    weight_text = font.render(str(food["weight"]), True, (255, 255, 255))
    screen.blit(weight_text, (food["pos"][0] * CELL + 12, food["pos"][1] * CELL + 68))

    # Body
    for seg in snake[1:]:
        draw_cell(seg[0], seg[1], img_body, (50, 170, 90))

    # Head
    hx, hy = snake[0]
    if img_head:
        rotated = pygame.transform.rotate(img_head, angle(direction))
        screen.blit(rotated, (hx * CELL, hy * CELL + 60))
    else:
        draw_cell(hx, hy, None, (80, 220, 120))

    # Game Over
    if not alive:
        overlay = pygame.Surface((W, H - 60), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 60))
        screen.blit(font_big.render("GAME OVER", True, (230, 70, 70)),
            font_big.render("GAME OVER", True, (0,0,0)).get_rect(center=(W//2, H//2 - 20)))
        screen.blit(font.render(f"Счёт: {score}  |  Нажми R", True, (200, 200, 200)),
            font.render("x", True, (0,0,0)).get_rect(center=(W//2, H//2 + 30)))

    pygame.display.flip()
    clock.tick(60)