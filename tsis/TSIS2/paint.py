import pygame
import math
import datetime

# Инициализация
pygame.init()

WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
toolbar_height = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT + toolbar_height))
pygame.display.set_caption("Paint TSIS 2 - Fixed")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

FONT = pygame.font.SysFont("Arial", 18)
TEXT_FONT = pygame.font.SysFont("Arial", 24)

# Переменные состояния
clock = pygame.time.Clock()
running = True
drawing = False
mode = "pen"
color = BLACK
brush_size = 5
start_pos = (0, 0)
last_pos = (0, 0)

# Текст
text_active = False
text_content = ""
text_pos = (0, 0)

# ================= UNDO / REDO =================
undo_stack = []
redo_stack = []

def save_state():
    undo_stack.append(canvas.copy())
    if len(undo_stack) > 30: undo_stack.pop(0)
    redo_stack.clear()

def undo():
    if undo_stack:
        redo_stack.append(canvas.copy())
        last = undo_stack.pop()
        canvas.blit(last, (0, 0))

def redo():
    if redo_stack:
        undo_stack.append(canvas.copy())
        last = redo_stack.pop()
        canvas.blit(last, (0, 0))

# ================= ИНСТРУМЕНТЫ =================

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
            if surface.get_at((cx, cy)) == target_color:
                surface.set_at((cx, cy), new_color)
                stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])

def draw_shape(surface, mode, color, start, end, size):
    if mode == "line":
        pygame.draw.line(surface, color, start, end, size)
    elif mode == "rect":
        x, y = min(start[0], end[0]), min(start[1], end[1])
        w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
        pygame.draw.rect(surface, color, (x, y, w, h), size)
    elif mode == "circle":
        r = int(math.hypot(end[0]-start[0], end[1]-start[1]))
        pygame.draw.circle(surface, color, start, r, size)
    elif mode == "square":
        side = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
        x = start[0] if end[0] > start[0] else start[0] - side
        y = start[1] if end[1] > start[1] else start[1] - side
        pygame.draw.rect(surface, color, (x, y, side, side), size)
    elif mode == "right_tri":
        pygame.draw.polygon(surface, color, [start, (start[0], end[1]), end], size)
    elif mode == "rhombus":
        mx, my = (start[0]+end[0])//2, (start[1]+end[1])//2
        pts = [(mx, start[1]), (end[0], my), (mx, end[1]), (start[0], my)]
        pygame.draw.polygon(surface, color, pts, size)

# ================= ПАНЕЛЬ УПРАВЛЕНИЯ =================

colors_palette = [
    (0,0,0), (255,0,0), (0,255,0), (0,0,255), 
    (255,255,0), (255,165,0), (128,0,128), (255,255,255)
]
color_rects = []
for i, c in enumerate(colors_palette):
    color_rects.append((c, pygame.Rect(10 + i*35, HEIGHT + 75, 30, 30)))

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, HEIGHT, WIDTH, toolbar_height))
    msg = f"Mode: {mode.upper()} | Size: {brush_size} | Color: {color}"
    screen.blit(FONT.render(msg, True, BLACK), (10, HEIGHT + 5))
    
    tools_msg = "P: Pen | L: Line | R: Rect | C: Circle | S: Square | T: Tri | H: Rhombus | F: Fill | X: Text | E: Eraser"
    screen.blit(FONT.render(tools_msg, True, BLACK), (10, HEIGHT + 25))
    
    edit_msg = "1, 2, 3: Sizes | Ctrl+Z: Undo | Ctrl+Y: Redo | Ctrl+S: Save"
    screen.blit(FONT.render(edit_msg, True, BLACK), (10, HEIGHT + 45))

    for c_val, rect in color_rects:
        pygame.draw.rect(screen, c_val, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        if color == c_val:
            pygame.draw.rect(screen, (0, 255, 255), rect, 3)

# ================= ЦИКЛ ИГРЫ =================

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    if drawing and mode not in ["pen", "eraser", "fill", "text"]:
        draw_shape(screen, mode, color, start_pos, pygame.mouse.get_pos(), brush_size)
    
    if text_active:
        screen.blit(TEXT_FONT.render(text_content + "|", True, color), text_pos)

    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
            
            if text_active:
                if event.key == pygame.K_RETURN:
                    canvas.blit(TEXT_FONT.render(text_content, True, color), text_pos)
                    text_active = False
                elif event.key == pygame.K_ESCAPE: text_active = False
                elif event.key == pygame.K_BACKSPACE: text_content = text_content[:-1]
                else: text_content += event.unicode
            else:
                # ГОРЯЧИЕ КЛАВИШИ КОМБИНАЦИЙ (CTRL + ...)
                if ctrl_pressed:
                    if event.key in [pygame.K_s]: # СОХРАНЕНИЕ
                        fname = f"paint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        pygame.image.save(canvas, fname)
                        print(f"Изображение сохранено как: {fname}")
                    elif event.key in [pygame.K_z]:
                        undo()
                    elif event.key in [pygame.K_y]:
                        redo()
                
                # ГОРЯЧИЕ КЛАВИШИ РЕЖИМОВ
                else:
                    if event.key == pygame.K_p: mode = "pen"
                    elif event.key == pygame.K_l: mode = "line"
                    elif event.key == pygame.K_r: mode = "rect"
                    elif event.key == pygame.K_c: mode = "circle"
                    elif event.key == pygame.K_s: mode = "square"
                    elif event.key == pygame.K_t: mode = "right_tri"
                    elif event.key == pygame.K_h: mode = "rhombus"
                    elif event.key == pygame.K_f: mode = "fill"
                    elif event.key == pygame.K_x: mode = "text"
                    elif event.key == pygame.K_e: mode = "eraser"
                    elif event.key == pygame.K_1: brush_size = 2
                    elif event.key == pygame.K_2: brush_size = 5
                    elif event.key == pygame.K_3: brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < HEIGHT:
                save_state()
                if mode == "fill": flood_fill(canvas, event.pos[0], event.pos[1], color)
                elif mode == "text":
                    text_active, text_pos, text_content = True, event.pos, ""
                else:
                    drawing, start_pos, last_pos = True, event.pos, event.pos
            else:
                for c_val, rect in color_rects:
                    if rect.collidepoint(event.pos): color = c_val

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if mode not in ["pen", "eraser"]:
                    draw_shape(canvas, mode, color, start_pos, event.pos, brush_size)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "pen":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos
            elif mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()