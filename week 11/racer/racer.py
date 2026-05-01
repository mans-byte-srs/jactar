import pygame, sys, random
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана и константы
W, H = 400, 600
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD  = (255, 215, 0)

# --- Загрузка ресурсов ---
def load(file, size):
    return pygame.transform.scale(pygame.image.load(file).convert_alpha(), size)

# Фоновые изображения и звуки
bg        = pygame.transform.scale(pygame.image.load("AnimatedStreet.png"), (W, H))
go_bg     = pygame.transform.scale(pygame.image.load("game_over_bg.png"), (W, H))
coin_snd  = pygame.mixer.Sound("coin_sound.mp3")
crash_snd = pygame.mixer.Sound("crash.mp3")

# Спрайты
player_img   = load("Player.png", (50, 100))
enemy_img    = load("Enemy.png",  (50, 100))
coin_frames  = [load(f"coin{i}.png", (40, 40)) for i in range(1, 5)]

# Координаты полос движения
LANES = [50, 150, 250, 350]

# --- Функция сброса/инициализации игры ---
def reset():
    return {
        "speed":      5,      # Скорость окружения (фон и монетки)
        "enemy_speed": 5,      # Начальная скорость врага
        "score":      0,      # Очки за проезд мимо врагов
        "coins":      0,      # Общее количество собранных монет
        "bg_y1":      0,      # Координата Y первого фона
        "bg_y2":      -H,     # Координата Y второго фона (над первым)
        "player":     player_img.get_rect(center=(W//2, H - 150)),
        "enemy":      enemy_img.get_rect(center=(random.choice(LANES), -100)),
        "coin":       coin_frames[0].get_rect(center=(random.choice(LANES), -300)),
        "coin_frame": 0.0,    # Индекс текущего кадра анимации монетки
        "coin_weight": random.randint(1, 5) # Случайный вес первой монетки
    }

g = reset()

# Пользовательское событие для постепенного ускорения игры
INC_SPEED = USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# --- Главный цикл игры ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        
        # Общее ускорение (скорость дороги) каждые 1 сек
        if event.type == INC_SPEED and g["speed"] < 15:
            g["speed"] += 0.2

    # --- Управление игроком ---
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]  and g["player"].left  > 0: g["player"].x -= 5
    if keys[K_RIGHT] and g["player"].right < W: g["player"].x += 5

    # --- Логика движения ---
    
    # Прокрутка фона (создает эффект бесконечной дороги)
    g["bg_y1"] += g["speed"]
    g["bg_y2"] += g["speed"]
    if g["bg_y1"] >= H: g["bg_y1"] = -H
    if g["bg_y2"] >= H: g["bg_y2"] = -H

    # Движение врага
    g["enemy"].y += g["enemy_speed"]
    if g["enemy"].top > H:
        g["score"] += 1
        g["enemy"].center = (random.choice(LANES), -100)

    # Движение и анимация монетки
    g["coin"].y += g["speed"]
    if g["coin"].top > H:
        g["coin"].center = (random.choice(LANES), -300)
        g["coin_weight"] = random.randint(1, 5) # Новый вес при респавне
    
    g["coin_frame"] = (g["coin_frame"] + 0.2) % 4
    coin_img = coin_frames[int(g["coin_frame"])]

    # --- Проверка столкновений (ХИТБОКСЫ УДАЛЕНЫ) ---

    # Сбор монетки
    if g["player"].colliderect(g["coin"]):
        g["coins"] += g["coin_weight"] # Прибавляем вес монетки
        coin_snd.play()
        
        # УВЕЛИЧЕНИЕ СКОРОСТИ ВРАГА: каждые 10 собранных монет враг ускоряется
        g["enemy_speed"] = 5 + (g["coins"] // 10)
        
        # Перемещаем монетку наверх и меняем вес
        g["coin"].center = (random.choice(LANES), -300)
        g["coin_weight"] = random.randint(1, 5)

    # Столкновение с врагом (Game Over)
    if g["player"].colliderect(g["enemy"]):
        crash_snd.play()
        
        # Внутренний цикл экрана проигрыша
        while True:
            SCREEN.blit(go_bg, (0, 0))
            SCREEN.blit(font.render(f"Score: {g['score']}", True, WHITE), (165, 240))
            SCREEN.blit(font.render(f"Total Coins: {g['coins']}", True, WHITE), (150, 270))
            SCREEN.blit(font.render("R — Restart", True, WHITE), (140, 460))
            SCREEN.blit(font.render("ESC — Exit",  True, WHITE), (148, 495))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        g = reset() # Сброс всех параметров
                    if event.key == K_ESCAPE:
                        pygame.quit(); sys.exit()
            
            # Выход из Game Over в основной цикл, если нажали R
            if g["score"] == 0: 
                break

    # --- Отрисовка графики ---
    
    # Отрисовка дороги
    SCREEN.blit(bg, (0, g["bg_y1"]))
    SCREEN.blit(bg, (0, g["bg_y2"]))
    
    # Отрисовка игрока и врага
    SCREEN.blit(player_img, g["player"])
    SCREEN.blit(enemy_img,  g["enemy"])
    
    # Отрисовка монетки и её веса сверху
    SCREEN.blit(coin_img, g["coin"])
    weight_txt = font.render(str(g["coin_weight"]), True, GOLD)
    SCREEN.blit(weight_txt, (g["coin"].x + 10, g["coin"].y - 25))
    
    # Интерфейс (счетчики)
    SCREEN.blit(font.render(f"Score: {g['score']}", True, BLACK), (10, 10))
    SCREEN.blit(font.render(f"Coins: {g['coins']}", True, BLACK), (10, 40))
    SCREEN.blit(font.render(f"E-Speed: {g['enemy_speed']}", True, BLACK), (10, 70))

    pygame.display.update()
    clock.tick(60)