import pygame
import sys
pygame.init()
 
WIDTH       = 900
HEIGHT      = 650
TOOLBAR_H   = 60      # Height of the top toolbar
CANVAS_TOP  = TOOLBAR_H
 
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED     = (220,  20,  60)
GREEN   = (0,   200,   0)
BLUE    = (30,  144, 255)
YELLOW  = (255, 215,   0)
ORANGE  = (255, 165,   0)
PURPLE  = (148,   0, 211)
CYAN    = (0,   255, 255)
PINK    = (255, 105, 180)
BROWN   = (139,  69,  19)
 

PALETTE = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW,
           ORANGE, PURPLE, CYAN, PINK, BROWN, DARK_GRAY]
 

TOOL_PEN       = "pen"
TOOL_RECT      = "rect"
TOOL_CIRCLE    = "circle"
TOOL_ERASER    = "eraser"
 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()
 
font = pygame.font.SysFont("Verdana", 14, bold=True)
 

canvas = pygame.Surface((WIDTH, HEIGHT - CANVAS_TOP))
canvas.fill(WHITE)
 
 
def draw_toolbar(current_tool, current_color, brush_size):
    """
    Draw the top toolbar with:
    - Tool buttons (Pen, Rect, Circle, Eraser)
    - Color palette swatches
    - Current brush size indicator
    """
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 2)
 
  
    tools = [
        (TOOL_PEN,    "Pen",    10),
        (TOOL_RECT,   "Rect",   80),
        (TOOL_CIRCLE, "Circle", 150),
        (TOOL_ERASER, "Eraser", 225),
    ]
    tool_rects = {}
    for name, label, x in tools:
      
        bg = DARK_GRAY if name == current_tool else (180, 180, 180)
        r = pygame.Rect(x, 10, 65, 38)
        pygame.draw.rect(screen, bg, r, border_radius=6)
        pygame.draw.rect(screen, DARK_GRAY, r, 2, border_radius=6)
        txt = font.render(label, True, WHITE if name == current_tool else BLACK)
        screen.blit(txt, txt.get_rect(center=r.center))
        tool_rects[name] = r
 
  
    palette_rects = []
    for i, color in enumerate(PALETTE):
        r = pygame.Rect(310 + i * 38, 10, 32, 32)
        pygame.draw.rect(screen, color, r)
        # White border around the currently selected color
        border = WHITE if color == current_color else DARK_GRAY
        pygame.draw.rect(screen, border, r, 3)
        palette_rects.append((color, r))
 
  
    size_text = font.render(f"Size: {brush_size}  [+/-]", True, BLACK)
    screen.blit(size_text, (WIDTH - 130, 22))
 
  
    clear_r = pygame.Rect(WIDTH - 200, 10, 60, 38)
    pygame.draw.rect(screen, RED, clear_r, border_radius=6)
    pygame.draw.rect(screen, DARK_GRAY, clear_r, 2, border_radius=6)
    clear_txt = font.render("Clear", True, WHITE)
    screen.blit(clear_txt, clear_txt.get_rect(center=clear_r.center))
 
    return tool_rects, palette_rects, clear_r
 
 

current_tool  = TOOL_PEN
current_color = BLACK
brush_size    = 5
 
drawing       = False   
start_pos     = None    
last_pos      = None       
 

canvas_snapshot = None
 
 
def canvas_pos(screen_x, screen_y):
    """Convert screen coordinates to canvas coordinates."""
    return (screen_x, screen_y - CANVAS_TOP)

while True:
    clock.tick(60)
 
   
    screen.blit(canvas, (0, CANVAS_TOP))
    tool_rects, palette_rects, clear_r = draw_toolbar(
        current_tool, current_color, brush_size)
 
  
    if drawing and start_pos and current_tool in (TOOL_RECT, TOOL_CIRCLE):
        mx, my = pygame.mouse.get_pos()
        cx, cy = canvas_pos(mx, my)
        
        if current_tool == TOOL_RECT:
            sx, sy = start_pos
            rx = min(sx, cx)
            ry = min(sy, cy) + CANVAS_TOP
            rw = abs(cx - sx)
            rh = abs(cy - sy)
            pygame.draw.rect(screen, current_color,
                             (rx, ry, rw, rh), brush_size)
        elif current_tool == TOOL_CIRCLE:
            sx, sy = start_pos
            cx2, cy2 = cx + CANVAS_TOP, cy + CANVAS_TOP  
            radius = int(((cx - sx)**2 + (cy - sy)**2) ** 0.5)
            pygame.draw.circle(screen, current_color,
                               (sx, sy + CANVAS_TOP), radius, brush_size)
 
    pygame.display.flip()
 
    
    for event in pygame.event.get():
 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                brush_size = min(brush_size + 2, 50)
            if event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 2, 1)
 
       
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
 
          
            if my < CANVAS_TOP:
 
              
                for name, r in tool_rects.items():
                    if r.collidepoint(mx, my):
                        current_tool = name
 
             
                for color, r in palette_rects:
                    if r.collidepoint(mx, my):
                        current_color = color
                       
                        if current_tool == TOOL_ERASER:
                            current_tool = TOOL_PEN
 
              
                if clear_r.collidepoint(mx, my):
                    canvas.fill(WHITE)
 
            else:
               
                drawing = True
                cx, cy  = canvas_pos(mx, my)
                start_pos = (cx, cy)
                last_pos  = (cx, cy)
               
                canvas_snapshot = canvas.copy()
 
            
                if current_tool == TOOL_PEN:
                    pygame.draw.circle(canvas, current_color, (cx, cy), brush_size)
                elif current_tool == TOOL_ERASER:
                    pygame.draw.circle(canvas, WHITE, (cx, cy), brush_size * 3)
 
    
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my >= CANVAS_TOP:   
                cx, cy = canvas_pos(mx, my)
 
                if current_tool == TOOL_PEN:
                
                    pygame.draw.line(canvas, current_color, last_pos, (cx, cy), brush_size * 2)
                    pygame.draw.circle(canvas, current_color, (cx, cy), brush_size)
                    last_pos = (cx, cy)
 
                elif current_tool == TOOL_ERASER:
                  
                    pygame.draw.circle(canvas, WHITE, (cx, cy), brush_size * 3)
                    last_pos = (cx, cy)
 
               
 
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            mx, my = event.pos
            cx, cy = canvas_pos(mx, my)
 
            if current_tool == TOOL_RECT and start_pos:
                
                canvas.blit(canvas_snapshot, (0, 0))
                sx, sy = start_pos
                rx = min(sx, cx)
                ry = min(sy, cy)
                rw = abs(cx - sx)
                rh = abs(cy - sy)
                pygame.draw.rect(canvas, current_color, (rx, ry, rw, rh), brush_size)
 
            elif current_tool == TOOL_CIRCLE and start_pos:
                canvas.blit(canvas_snapshot, (0, 0))
                sx, sy = start_pos
                radius = int(((cx - sx)**2 + (cy - sy)**2) ** 0.5)
                pygame.draw.circle(canvas, current_color, (sx, sy), radius, brush_size)
 
        
            drawing          = False
            start_pos        = None
            last_pos         = None
            canvas_snapshot  = None