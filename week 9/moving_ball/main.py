import pygame
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
my_ball = Ball(400, 300, 25, 800, 600)

running = True
while running:
    screen.fill((255, 255, 255)) # Ақ түс
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    my_ball.move(0, -20)
            if event.key == pygame.K_DOWN:  my_ball.move(0, 20)
            if event.key == pygame.K_LEFT:  my_ball.move(-20, 0)
            if event.key == pygame.K_RIGHT: my_ball.move(20, 0)

    pygame.draw.circle(screen, (255, 0, 0), (my_ball.x, my_ball.y), my_ball.radius)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()