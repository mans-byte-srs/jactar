import pygame
from clock import get_time_angles, rotate_hand

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Mickey's Clock")

# Суреттерді жүктеу (аттары мен папкасы дұрыс болуы керек)
# images/ папкасында осы файлдар тұруы тиіс
body = pygame.image.load('images/mickey_body.png')
hand = pygame.image.load('images/mickey_hand.png')

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Қазіргі бұрыштарды алу
    sec_a, min_a = get_time_angles()

    # 2. Экранды тазалау және денесін салу
    screen.fill((255, 255, 255))
    screen.blit(body, (0, 0))
    
    # 3. Қолдарын (тілдерін) салу
    # Орталық нүкте (400, 400) - экранның қақ ортасы
    rotate_hand(screen, hand, min_a, (400, 400)) # Минуттық
    rotate_hand(screen, hand, sec_a, (400, 400)) # Секундтық

    pygame.display.flip()
    clock.tick(60)

pygame.quit()