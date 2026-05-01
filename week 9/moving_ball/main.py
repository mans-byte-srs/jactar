import pygame
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
my_ball = Ball(400, 300, 50, 800, 600)
running = True
while running:
    screen.fill((255, 255, 255)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:    my_ball.move(0, -5)
    if keys[pygame.K_DOWN]:  my_ball.move(0, 5)
    if keys[pygame.K_LEFT]:  my_ball.move(-5, 0)
    if keys[pygame.K_RIGHT]: my_ball.move(5, 0)
    pygame.draw.circle(screen, (255, 255, 0), (my_ball.x, my_ball.y), my_ball.radius)
    
    pygame.display.flip()
    clock.tick(60)

    pygame.draw.circle(screen, (255, 255, 0), (my_ball.x, my_ball.y), my_ball.radius)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()