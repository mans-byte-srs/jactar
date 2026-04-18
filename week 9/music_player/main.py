import pygame
import sys
from player import MusicPlayer

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# Font
font = pygame.font.SysFont(None, 36)

# Music player
player = MusicPlayer("music")

clock = pygame.time.Clock()

def draw_text(text, y):
    render = font.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

running = True
while running:
    screen.fill((255, 255, 255))

    # UI text
    draw_text("P - Play | S - Stop", 50)
    draw_text("N - Next | B - Previous", 100)
    draw_text("Q - Quit", 150)
    draw_text(f"Track: {player.get_current_track_name()}", 220)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()