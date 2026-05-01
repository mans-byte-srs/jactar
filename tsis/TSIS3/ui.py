import pygame

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
GRAY       = (180, 180, 180)
DARK_GRAY  = (80,  80,  80 )
BLUE       = (50,  120, 220)
LIGHT_BLUE = (100, 160, 255)
RED        = (220, 50,  50 )
GREEN      = (50,  180, 80 )
YELLOW     = (255, 220, 0  )

pygame.font.init()
font       = pygame.font.SysFont("Arial", 22)
font_large = pygame.font.SysFont("Arial", 48, bold=True)
font_small = pygame.font.SysFont("Arial", 16)


def draw_button(surface, rect, text, active=False):
    mouse = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse)
    color = LIGHT_BLUE if (hover or active) else BLUE
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    lbl = font.render(text, True, WHITE)
    surface.blit(lbl, lbl.get_rect(center=rect.center))
    return hover


def button_clicked(rect, event):
    return (event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            rect.collidepoint(event.pos))


def draw_text(surface, text, x, y, color=WHITE, big=False, center=False):
    f = font_large if big else font
    lbl = f.render(text, True, color)
    if center:
        x = x - lbl.get_width() // 2
    surface.blit(lbl, (x, y))


def draw_title(surface, title, screen_width, y=40):
    lbl = font_large.render(title, True, YELLOW)
    surface.blit(lbl, (screen_width // 2 - lbl.get_width() // 2, y))


def text_input_screen(surface, clock, screen_width, screen_height, prompt):
    user_text = ""
    box = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 45)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys; sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_text.strip():
                    return user_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 18 and event.unicode.isprintable():
                    user_text += event.unicode

        surface.fill((30, 30, 60))
        draw_title(surface, "Enter Your Name", screen_width, 160)
        lbl = font.render(prompt, True, GRAY)
        surface.blit(lbl, (screen_width // 2 - lbl.get_width() // 2,
                            screen_height // 2 - 50))
        pygame.draw.rect(surface, WHITE, box, 2, border_radius=6)
        name_lbl = font.render(user_text + "|", True, YELLOW)
        surface.blit(name_lbl, (box.x + 8, box.y + 8))
        hint = font_small.render("Press Enter to confirm", True, GRAY)
        surface.blit(hint, (screen_width // 2 - hint.get_width() // 2,
                             box.bottom + 12))
        pygame.display.flip()
        clock.tick(60)
