import pygame, sys
from pygame.locals import *
import random, time
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
 

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
YELLOW     = (255, 215,   0)
DARK_GRAY  = (40,  40,  40)
ROAD_GRAY  = (80,  80,  80)
LINE_WHITE = (200, 200, 200)
 

PLAYER_BODY   = (30,  144, 255) 
PLAYER_WINDOW = (173, 216, 230)  
 

ENEMY_COLORS = [
    (220,  20,  60),
    (0,   180,   0),
    (255, 140,   0),
    (148,   0, 211),
    (255,  20, 147),
]
 

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
SPEED  = 5
SCORE  = 0
COINS  = 0
 
CAR_W = 44
CAR_H = 72
 

font           = pygame.font.SysFont("Verdana", 60)
font_small     = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, WHITE)
 

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
 

INC_SPEED  = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED,  1000)
pygame.time.set_timer(SPAWN_COIN, 3000)
 

road_offset = 0
 
 
def draw_car(surface, x, y, body_color, window_color, facing_up=False):
    """
    Draw a top-down pixel car onto 'surface' at position (x, y).
    facing_up=True  → enemy car (headlights at top)
    facing_up=False → player car (headlights at bottom)
    """
    w, h = CAR_W, CAR_H
 
   
    pygame.draw.rect(surface, body_color,
                     (x + 4, y, w - 8, h), border_radius=8)
 
    if not facing_up:
       
        pygame.draw.rect(surface, window_color,
                         (x + 8, y + h - 22, w - 16, 16), border_radius=4)
        
        pygame.draw.rect(surface, window_color,
                         (x + 8, y + 6, w - 16, 12), border_radius=4)
   
        pygame.draw.rect(surface, (20, 100, 200),
                         (x + w//2 - 3, y + 4, 6, h - 8), border_radius=3)
   
        pygame.draw.circle(surface, YELLOW,       (x + 10,     y + h - 8), 4)
        pygame.draw.circle(surface, YELLOW,       (x + w - 10, y + h - 8), 4)
     
        pygame.draw.circle(surface, (255, 60, 60), (x + 10,     y + 8), 4)
        pygame.draw.circle(surface, (255, 60, 60), (x + w - 10, y + 8), 4)
    else:
     
        pygame.draw.rect(surface, window_color,
                         (x + 8, y + 6, w - 16, 16), border_radius=4)

        pygame.draw.rect(surface, window_color,
                         (x + 8, y + h - 22, w - 16, 12), border_radius=4)
      
        pygame.draw.circle(surface, YELLOW,       (x + 10,     y + 8), 4)
        pygame.draw.circle(surface, YELLOW,       (x + w - 10, y + 8), 4)
   
        pygame.draw.circle(surface, (255, 60, 60), (x + 10,     y + h - 8), 4)
        pygame.draw.circle(surface, (255, 60, 60), (x + w - 10, y + h - 8), 4)
 
    ww, wh = 8, 18
    pygame.draw.rect(surface, (20, 20, 20), (x - 2,     y + 10,     ww, wh), border_radius=3)
    pygame.draw.rect(surface, (20, 20, 20), (x + w - 6, y + 10,     ww, wh), border_radius=3)
    pygame.draw.rect(surface, (20, 20, 20), (x - 2,     y + h - 28, ww, wh), border_radius=3)
    pygame.draw.rect(surface, (20, 20, 20), (x + w - 6, y + h - 28, ww, wh), border_radius=3)
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = random.choice(ENEMY_COLORS)
        self.image = pygame.Surface((CAR_W + 8, CAR_H), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -CAR_H)
 
    def _draw(self):
        """Redraw car surface with current color."""
        self.image.fill((0, 0, 0, 0))
        draw_car(self.image, 4, 0, self.color, (220, 220, 255), facing_up=True)
 
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -CAR_H
            self.rect.centerx = random.randint(50, SCREEN_WIDTH - 50)
            self.color = random.choice(ENEMY_COLORS)
            self._draw()
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CAR_W + 8, CAR_H), pygame.SRCALPHA)
        draw_car(self.image, 4, 0, PLAYER_BODY, PLAYER_WINDOW, facing_up=False)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
 
    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]  and self.rect.left > 5:
            self.rect.move_ip(-6, 0)
        if pressed[K_RIGHT] and self.rect.right < SCREEN_WIDTH - 5:
            self.rect.move_ip(6, 0)
 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (13, 13), 12)
        pygame.draw.circle(self.image, (180, 140, 0), (13, 13), 12, 2)
        coin_font = pygame.font.SysFont("Verdana", 13, bold=True)
        sign = coin_font.render("$", True, (140, 100, 0))
        self.image.blit(sign, sign.get_rect(center=(13, 13)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -20)
 
    def move(self):
        self.rect.move_ip(0, max(SPEED - 2, 2))
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

P1          = Player()
E1          = Enemy()
enemies     = pygame.sprite.Group()
coins       = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies.add(E1)
all_sprites.add(P1, E1)
 
 
def draw_road():
    """Draw scrolling road with sidewalks and lane markings."""
    global road_offset
    DISPLAYSURF.fill(ROAD_GRAY)
 

    pygame.draw.rect(DISPLAYSURF, (110, 90, 60), (0,                  0, 30, SCREEN_HEIGHT))
    pygame.draw.rect(DISPLAYSURF, (110, 90, 60), (SCREEN_WIDTH - 30,  0, 30, SCREEN_HEIGHT))

    road_offset = (road_offset + int(SPEED) // 2 + 1) % 80
    for y in range(-80 + road_offset, SCREEN_HEIGHT + 80, 80):
        pygame.draw.rect(DISPLAYSURF, LINE_WHITE,
                         (SCREEN_WIDTH // 2 - 4, y, 8, 50))
   
    for y in range(-80 + road_offset, SCREEN_HEIGHT + 80, 80):
        pygame.draw.rect(DISPLAYSURF, (140, 140, 140),
                         (SCREEN_WIDTH // 3,     y, 4, 30))
        pygame.draw.rect(DISPLAYSURF, (140, 140, 140),
                         (2 * SCREEN_WIDTH // 3, y, 4, 30))
 
while True:
 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == INC_SPEED:
            SPEED += 0.5
 
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
 
    draw_road()
 
    P1.move()
    for e in enemies:
        e.move()
    for c in coins:
        c.move()
 

    if pygame.sprite.spritecollideany(P1, enemies):
 

        DISPLAYSURF.fill(DARK_GRAY)
        DISPLAYSURF.blit(game_over_text,
                         game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200)))
        final = font_small.render(f"Score: {SCORE}   Coins: {COINS}", True, YELLOW)
        DISPLAYSURF.blit(final, final.get_rect(center=(SCREEN_WIDTH // 2, 280)))
 
        btn_restart = pygame.Rect(60, 340, 120, 45)
        btn_quit    = pygame.Rect(220, 340, 120, 45)
        pygame.draw.rect(DISPLAYSURF, (0, 180, 0), btn_restart, border_radius=8)
        pygame.draw.rect(DISPLAYSURF, (180, 0, 0), btn_quit,    border_radius=8)
        txt_r = font_small.render("Restart", True, WHITE)
        txt_q = font_small.render("Quit",    True, WHITE)
        DISPLAYSURF.blit(txt_r, txt_r.get_rect(center=btn_restart.center))
        DISPLAYSURF.blit(txt_q, txt_q.get_rect(center=btn_quit.center))
        pygame.display.update()
 
   
        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if btn_restart.collidepoint(ev.pos):
                       
                        SCORE = 0
                        COINS = 0
                        SPEED = 5
                        road_offset = 0
                        P1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
                        E1.rect.center = (random.randint(50, SCREEN_WIDTH - 50), -CAR_H)
                        for c in coins:
                            c.kill()
                        waiting = False
                    if btn_quit.collidepoint(ev.pos):
                        pygame.quit()
                        sys.exit()
 
    
    collected = pygame.sprite.spritecollide(P1, coins, True)
    COINS += len(collected)
 

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
 

    score_text = font_small.render(f"Score: {SCORE}", True, WHITE)
    DISPLAYSURF.blit(score_text, (35, 10))
 
    coin_text = font_small.render(f"Coins: {COINS}", True, YELLOW)
    DISPLAYSURF.blit(coin_text, coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10)))
 
    pygame.display.update()
    FramePerSec.tick(FPS)