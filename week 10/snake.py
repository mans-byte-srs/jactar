import pygame
import random
import sys
pygame.init()

CELL      = 20
COLS      = 30
ROWS      = 25
WIDTH     = COLS * CELL
HEIGHT    = ROWS * CELL

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200,  0)
DARK_GREEN = (0,   150,  0)
RED        = (220,  20, 60)
YELLOW     = (255, 215,  0)
GRAY       = (50,   50,  50)
ORANGE     = (255, 165,  0)

FOODS_PER_LEVEL = 3
BASE_SPEED      = 8
SPEED_STEP      = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock  = pygame.time.Clock()

font_big   = pygame.font.SysFont("Verdana", 48, bold=True)
font_med   = pygame.font.SysFont("Verdana", 24)
font_small = pygame.font.SysFont("Verdana", 18)

def random_food(snake_body):
    """Generate food not on snake and not on border walls."""
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake_body:
            return (x, y)

def draw_grid():
    """Draw subtle grid lines."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_walls():
    """Draw border wall around the playfield."""
    wall_color = (100, 100, 100)
    for col in range(COLS):
        pygame.draw.rect(screen, wall_color, (col * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, wall_color, (col * CELL, (ROWS-1)*CELL, CELL, CELL))
    for row in range(ROWS):
        pygame.draw.rect(screen, wall_color, (0, row * CELL, CELL, CELL))
        pygame.draw.rect(screen, wall_color, ((COLS-1)*CELL, row*CELL, CELL, CELL))

def draw_snake(body):
    """Draw snake: bright head, darker body."""
    for i, (x, y) in enumerate(body):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (x*CELL+1, y*CELL+1, CELL-2, CELL-2))
        if i == 0:
            pygame.draw.circle(screen, BLACK, (x*CELL+5, y*CELL+5), 3)
            pygame.draw.circle(screen, BLACK, (x*CELL+15, y*CELL+5), 3)

def draw_food(pos):
    """Draw food as a red circle with a stem."""
    x, y = pos
    pygame.draw.circle(screen, RED, (x*CELL + CELL//2, y*CELL + CELL//2), CELL//2 - 2)
    pygame.draw.line(screen, DARK_GREEN,
                     (x*CELL + CELL//2, y*CELL + 2),
                     (x*CELL + CELL//2 + 4, y*CELL - 2), 2)

def draw_hud(score, level):
    """Draw score and level at the top bar."""
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, CELL))
    score_surf = font_small.render(f"Score: {score}", True, WHITE)
    level_surf = font_small.render(f"Level: {level}", True, ORANGE)
    screen.blit(score_surf, (8, 2))
    screen.blit(level_surf, (WIDTH - 90, 2))

def show_message(title, sub=""):
    """Show a temporary level-up message for 1 second."""
    screen.fill(BLACK)
    title_surf = font_big.render(title, True, YELLOW)
    sub_surf   = font_med.render(sub, True, WHITE)
    screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    screen.blit(sub_surf,   sub_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.flip()
    pygame.time.wait(1000)


def game_over_screen(score):
    """
    Show Game Over screen with Restart and Quit buttons.
    Returns True = restart, False = quit.
    """
    btn_restart = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 40, 120, 45)
    btn_quit    = pygame.Rect(WIDTH//2 + 20,  HEIGHT//2 + 40, 120, 45)

    while True:
        screen.fill(BLACK)
        title_surf = font_big.render("Game Over", True, RED)
        score_surf = font_med.render(f"Score: {score}", True, WHITE)
        hint_surf  = font_small.render("Choose an option:", True, GRAY)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))
        screen.blit(score_surf, score_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        screen.blit(hint_surf,  hint_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

        pygame.draw.rect(screen, (0, 180, 0), btn_restart, border_radius=8)
        pygame.draw.rect(screen, (180, 0, 0), btn_quit,    border_radius=8)
        r_txt = font_med.render("Restart", True, WHITE)
        q_txt = font_med.render("Quit",    True, WHITE)
        screen.blit(r_txt, r_txt.get_rect(center=btn_restart.center))
        screen.blit(q_txt, q_txt.get_rect(center=btn_quit.center))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_restart.collidepoint(event.pos):
                    return True
                if btn_quit.collidepoint(event.pos):
                    return False


def game_loop():
    """Main snake game loop. Returns score when player dies."""
    snake      = [(COLS//2, ROWS//2),
                  (COLS//2 - 1, ROWS//2),
                  (COLS//2 - 2, ROWS//2)]
    direction  = (1, 0)
    next_dir   = (1, 0)
    food       = random_food(snake)
    score      = 0
    level      = 1
    food_eaten = 0
    speed      = BASE_SPEED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != (0,  1): next_dir = (0, -1)
                if event.key == pygame.K_DOWN  and direction != (0, -1): next_dir = (0,  1)
                if event.key == pygame.K_LEFT  and direction != (1,  0): next_dir = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0): next_dir = (1,  0)

        direction = next_dir
        head_x    = snake[0][0] + direction[0]
        head_y    = snake[0][1] + direction[1]
        new_head  = (head_x, head_y)

    
        if head_x <= 0 or head_x >= COLS - 1 or head_y <= 0 or head_y >= ROWS - 1:
            return score

        if new_head in snake:
            return score

        snake.insert(0, new_head)

        if new_head == food:
            score      += 10 * level
            food_eaten += 1
            food        = random_food(snake)
            if food_eaten >= FOODS_PER_LEVEL:
                food_eaten = 0
                level     += 1
                speed     += SPEED_STEP
                show_message(f"Level {level}!", "Speed increased!")
        else:
            snake.pop()

        screen.fill((20, 20, 20))
        draw_grid()
        draw_walls()
        draw_food(food)
        draw_snake(snake)
        draw_hud(score, level)
        pygame.display.flip()
        clock.tick(speed)
def start_screen():
    screen.fill(BLACK)
    title = font_big.render("SNAKE", True, GREEN)
    hint  = font_med.render("Press any key to start", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    screen.blit(hint,  hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
start_screen()

while True:
    final_score = game_loop()
    restart = game_over_screen(final_score)
    if not restart:
        break

pygame.quit()
sys.exit()
