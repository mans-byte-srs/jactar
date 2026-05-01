import pygame
import random

# Road geometry (same as practice files)
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
ROAD_WIDTH    = 300
LANE_WIDTH    = ROAD_WIDTH // 3
ROAD_LEFT     = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT    = ROAD_LEFT + ROAD_WIDTH

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
RED    = (255, 50,  50 )
GREEN  = (50,  200, 50 )
BLUE   = (50,  100, 255)
YELLOW = (255, 220, 0  )
GRAY   = (128, 128, 128)
ORANGE = (255, 165, 0  )
BRONZE = (205, 127, 50 )
SILVER = (192, 192, 192)
GOLD   = (255, 215, 0  )
DARK   = (40,  40,  40 )

CAR_COLORS = {
    "green":  GREEN,
    "blue":   BLUE,
    "yellow": YELLOW,
}

pygame.font.init()
small_font = pygame.font.SysFont("Arial", 13, bold=True)


def lane_center(lane):
    """Return the x-center pixel of a lane (0-2)."""
    return ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH

class Player(pygame.sprite.Sprite):

    def __init__(self, color_name="green"):
        super().__init__()
        color = CAR_COLORS.get(color_name, GREEN)
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, (5,  10, 30, 15))  # windshield
        pygame.draw.rect(self.image, BLACK, (0,   5, 10, 15))  # FL wheel
        pygame.draw.rect(self.image, BLACK, (30,  5, 10, 15))  # FR wheel
        pygame.draw.rect(self.image, BLACK, (0,  50, 10, 15))  # BL wheel
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))  # BR wheel

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom   = SCREEN_HEIGHT - 20
        self.base_speed    = 5
        self.speed         = self.base_speed

        # Power-up state
        self.shield   = False
        self.nitro    = False
        self.nitro_timer  = 0    # frames remaining
        self.shield_hits  = 0   # hits absorbed

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)
        # Stay on road
        if self.rect.left  < ROAD_LEFT:  self.rect.left  = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT: self.rect.right = ROAD_RIGHT

    def update_powerups(self):
        if self.nitro and self.nitro_timer > 0:
            self.nitro_timer -= 1
            self.speed = self.base_speed + 5
            if self.nitro_timer == 0:
                self.nitro  = False
                self.speed  = self.base_speed
        # Draw shield tint when active
        if self.shield:
            pygame.draw.rect(self.image, (100, 200, 255, 80),
                             self.image.get_rect(), 4)

    def activate_nitro(self):
        self.nitro       = True
        self.nitro_timer = 60 * 4   # 4 seconds at 60 fps

    def activate_shield(self):
        self.shield     = True
        self.shield_hits = 1

    def repair(self):
        """Repair: re-center the car (clears stuck position)."""
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom  = SCREEN_HEIGHT - 20

class Enemy(pygame.sprite.Sprite):

    def __init__(self, base_speed=4):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        pygame.draw.rect(self.image, BLACK, (5,  45, 30, 15))
        pygame.draw.rect(self.image, BLACK, (0,   5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30,  5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (0,  50, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))

        self.rect       = self.image.get_rect()
        self.base_speed = base_speed
        self.speed      = base_speed
        self.respawn(safe_y=None)

    def respawn(self, safe_y=None):
        lane = random.randint(0, 2)
        self.rect.centerx = lane_center(lane)
        self.rect.top      = random.randint(-400, -80)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn(safe_y=None)

    def boost(self, amount=1):
        self.speed = min(self.base_speed + amount, 15)

class Coin(pygame.sprite.Sprite):
    TYPES = [
        {"color": BRONZE, "weight": 1, "chance": 0.60},
        {"color": SILVER, "weight": 2, "chance": 0.30},
        {"color": GOLD,   "weight": 3, "chance": 0.10},
    ]

    def __init__(self):
        super().__init__()
        self.speed = 3
        self._make_image()
        self.rect = self.image.get_rect()
        self.respawn()

    def _pick_type(self):
        r, cum = random.random(), 0
        for t in self.TYPES:
            cum += t["chance"]
            if r <= cum:
                return t
        return self.TYPES[0]

    def _make_image(self):
        ct = self._pick_type()
        self.weight = ct["weight"]
        self.image  = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ct["color"], (14, 14), 12)
        pygame.draw.circle(self.image, BLACK, (14, 14), 12, 2)
        lbl = small_font.render(str(self.weight), True, BLACK)
        self.image.blit(lbl, lbl.get_rect(center=(14, 14)))

    def respawn(self):
        lane = random.randint(0, 2)
        self.rect.centerx = lane_center(lane)
        self.rect.top = random.randint(-500, -50)
        self._make_image()

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

class Obstacle(pygame.sprite.Sprite):
    """
    type = 'oil'     — slows player for 2 seconds
    type = 'barrier' — instant crash (like enemy)
    type = 'bump'    — cosmetic / slows briefly
    type = 'nitro'   — (handled separately; not an obstacle)
    """
    TYPES = ["oil", "barrier", "bump"]

    def __init__(self, speed=4):
        super().__init__()
        self.kind  = random.choice(self.TYPES)
        self.speed = speed
        self.image = pygame.Surface((44, 22), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect()
        self.respawn()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        if self.kind == "oil":
            pygame.draw.ellipse(self.image, (30, 30, 80, 200), (0, 0, 44, 22))
            lbl = small_font.render("OIL", True, WHITE)
            self.image.blit(lbl, lbl.get_rect(center=(22, 11)))
        elif self.kind == "barrier":
            pygame.draw.rect(self.image, ORANGE, (0, 0, 44, 22), border_radius=4)
            lbl = small_font.render("STOP", True, BLACK)
            self.image.blit(lbl, lbl.get_rect(center=(22, 11)))
        elif self.kind == "bump":
            pygame.draw.ellipse(self.image, GRAY, (0, 4, 44, 14))
            lbl = small_font.render("BUMP", True, BLACK)
            self.image.blit(lbl, lbl.get_rect(center=(22, 11)))

    def respawn(self):
        lane = random.randint(0, 2)
        self.rect.centerx = lane_center(lane)
        self.rect.top = random.randint(-600, -100)
        self.kind = random.choice(self.TYPES)
        self._draw()

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

class PowerUp(pygame.sprite.Sprite):
    TYPES = ["nitro", "shield", "repair"]

    def __init__(self, speed=3):
        super().__init__()
        self.kind   = random.choice(self.TYPES)
        self.speed  = speed
        self.timer  = 300   # disappear after 300 frames (~5 s)
        self.image  = pygame.Surface((34, 34), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect()
        self.respawn()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        colors = {"nitro": (255, 140, 0), "shield": (0, 200, 255), "repair": (0, 220, 80)}
        labels = {"nitro": "N", "shield": "S", "repair": "R"}
        pygame.draw.rect(self.image, colors[self.kind], (0, 0, 34, 34), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (0, 0, 34, 34), 2, border_radius=6)
        lbl = small_font.render(labels[self.kind], True, WHITE)
        self.image.blit(lbl, lbl.get_rect(center=(17, 17)))

    def respawn(self):
        lane = random.randint(0, 2)
        self.rect.centerx = lane_center(lane)
        self.rect.top = random.randint(-700, -200)
        self.kind  = random.choice(self.TYPES)
        self.timer = 300
        self._draw()

    def move(self):
        self.rect.move_ip(0, self.speed)
        self.timer -= 1
        if self.rect.top > SCREEN_HEIGHT or self.timer <= 0:
            self.respawn()
