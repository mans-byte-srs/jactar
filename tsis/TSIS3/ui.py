import pygame
from persistence import load_leaderboard


# --- Загрузка фоновых изображений ---

menu_bg = pygame.image.load(
    "assets/menu_bg.png"
)

settings_bg = pygame.image.load(
    "assets/settings_bg.png"
)

leaderboard_bg = pygame.image.load(
    "assets/leaderboard_bg.png"
)

# растянуть под размер окна

menu_bg = pygame.transform.scale(
    menu_bg,
    (400, 600)
)

settings_bg = pygame.transform.scale(
    settings_bg,
    (400, 600)
)

leaderboard_bg = pygame.transform.scale(
    leaderboard_bg,
    (400, 600)
)

WHITE = (230, 230, 230)
BLACK = (0, 0, 0)
REDDER=(100,0,0)
GREY=(150,150,150)
BLUE=(0,0,90)
GREEN=(0,60,0)


def get_font():

    return pygame.font.SysFont(
        "Verdana",
        20,
        bold=True
    )

def draw_text(screen, text, x, y):

    font = get_font()

    screen.blit(
        font.render(
            text,
            True,
            GREY
        ),
        (x, y)
    )




def draw_menu(screen):

    screen.blit(menu_bg, (0, 0))

    draw_text(
        screen,
        "1 - Play",
        30,
        270
    )

    draw_text(
        screen,
        "2 - Leaderboard",
        30,
        320
    )

    draw_text(
        screen,
        "3 - Settings",
        30,
        370
    )

    

def draw_settings(screen, settings):

    screen.blit(settings_bg, (0, 0))

    draw_text(
        screen,
        f"Sound: {settings['sound']}",
        30,
        250
    )

    draw_text(
        screen,
        "S - Toggle sound",
        30,
        300
    )

    draw_text(
        screen,
        "ESC - Back",
        30,
        500
    )


def draw_leaderboard(screen):

    screen.blit(leaderboard_bg, (0, 0))

    data = load_leaderboard()

    y = 180

    for i, row in enumerate(data):

        text = (
            f"{i+1}. "
            f"{row['name']}  "
            f"Score:{row['score']}  "
            f"Dist:{row['distance']}"
        )

        draw_text(
            screen,
            text,
            40,
            y
        )

        y += 30

    draw_text(
        screen,
        "ESC - Back",
        10,
        700
    )


def draw_game_over(screen, score, distance):

    # загрузка картинки
    img = pygame.image.load(
        "assets/game_over.png"
    ).convert()

    # растянуть под размер окна
    img = pygame.transform.scale(
        img,
        (400, 600)
    )

    # нарисовать фон
    screen.blit(img, (0, 0))

    # текст поверх картинки

    font = pygame.font.SysFont(
        "Verdana",
        20
    )

    text1 = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    text2 = font.render(
        f"Distance: {distance}",
        True,
        (255, 255, 255)
    )

    text3 = font.render(
        "R - Retry",
        True,
        (255, 255, 255)
    )

    text4 = font.render(
        "M - Menu",
        True,
        (255, 255, 255)
    )

    screen.blit(text1, (120, 260))
    screen.blit(text2, (110, 300))
    screen.blit(text3, (140, 380))
    screen.blit(text4, (140, 420))