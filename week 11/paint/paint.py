import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 24)
toolbar_height = 80 # Increased slightly for more instructions

screen = pygame.display.set_mode((WIDTH, HEIGHT + toolbar_height))
pygame.display.set_caption("Paint - Extended Shapes")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# ================= UNDO / REDO =================
undo_stack = []
redo_stack = []

def save_state():
    undo_stack.append(canvas.copy())
    if len(undo_stack) > 20: undo_stack.pop(0)
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

# ================= SHAPE FUNCTIONS =================

def draw_square(surface, color, start, end):
    # For a square, we take the smaller of the two distances to keep sides equal
    width = end[0] - start[0]
    height = end[1] - start[1]
    side = min(abs(width), abs(height))
    
    # Adjust direction based on mouse movement
    new_w = side if width > 0 else -side
    new_h = side if height > 0 else -side
    
    rect = pygame.Rect(start[0], start[1], new_w, new_h)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, 2)

def draw_right_triangle(surface, color, start, end):
    # A right triangle using start and end as the diagonal of the bounding box
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, color, start, end):
    # Calculate distance for the side length
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = math.sqrt(dx**2 + dy**2)
    
    # Height of equilateral triangle: (sqrt(3)/2) * side
    height = (math.sqrt(3) / 2) * side
    
    # Points: Top, Bottom Left, Bottom Right
    points = [
        (start[0], start[1] - height/2),
        (start[0] - side/2, start[1] + height/2),
        (start[0] + side/2, start[1] + height/2)
    ]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, color, start, end):
    # Calculate midpoints based on the bounding box created by start and end
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    
    points = [
        (mid_x, start[1]), # Top center
        (end[0], mid_y),   # Right center
        (mid_x, end[1]),   # Bottom center
        (start[0], mid_y)  # Left center
    ]
    pygame.draw.polygon(surface, color, points, 2)

# ================= BUTTONS & CONFIG =================
# Note: Logic for tool_buttons icons is kept from your snippet; 
# ensure "img/" folder exists or use pygame.draw placeholder logic.
tool_buttons = {
    "brush": pygame.Rect(10, HEIGHT + 10, 40, 40),
    "eraser": pygame.Rect(60, HEIGHT + 10, 40, 40),
    "save": pygame.Rect(110, HEIGHT + 10, 40, 40)
}

color_buttons = {
    (0, 0, 0): pygame.Rect(300, HEIGHT + 10, 30, 30),
    (255, 0, 0): pygame.Rect(340, HEIGHT + 10, 30, 30),
    (0, 0, 255): pygame.Rect(380, HEIGHT + 10, 30, 30)
}

clock = pygame.time.Clock()
running = True
drawing = False
mode = "pen"
color = BLACK
size = 5
start_pos = (0,0)
last_pos = (0,0)

def redraw_canvas():
    screen.fill((220, 220, 220))
    screen.blit(canvas, (0, 0))
    
    # Draw Toolbar
    pygame.draw.rect(screen, (180, 180, 180), (0, HEIGHT, WIDTH, toolbar_height))
    
    # Instructions
    txt = "P: Pen | S: Square | T: Right Tri | K: Equilat Tri | H: Rhombus | E: Eraser | Ctrl+Z: Undo"
    instr = FONT.render(txt, True, BLACK)
    screen.blit(instr, (10, HEIGHT + 55))
    
    # Draw color buttons
    for c_val, rect in color_buttons.items():
        pygame.draw.rect(screen, c_val, rect)
        if color == c_val: pygame.draw.rect(screen, WHITE, rect, 2)

# ================= MAIN LOOP =================
while running:
    redraw_canvas()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: mode = "pen"
            elif event.key == pygame.K_s: mode = "square"
            elif event.key == pygame.K_t: mode = "right_tri"
            elif event.key == pygame.K_k: mode = "equi_tri"
            elif event.key == pygame.K_h: mode = "rhombus"
            elif event.key == pygame.K_e: mode = "eraser"
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                undo()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < HEIGHT:
                save_state()
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
            else:
                # Color Selection
                for c_val, rect in color_buttons.items():
                    if rect.collidepoint(event.pos): color = c_val

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if mode == "square": draw_square(canvas, color, start_pos, event.pos)
                elif mode == "right_tri": draw_right_triangle(canvas, color, start_pos, event.pos)
                elif mode == "equi_tri": draw_equilateral_triangle(canvas, color, start_pos, event.pos)
                elif mode == "rhombus": draw_rhombus(canvas, color, start_pos, event.pos)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "pen":
                pygame.draw.line(canvas, color, last_pos, event.pos, size)
                last_pos = event.pos
            elif mode == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, 10)
                last_pos = event.pos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()