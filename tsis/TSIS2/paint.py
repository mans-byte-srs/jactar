
import pygame
import sys
from datetime import datetime
import tools
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 680
CANVAS_HEIGHT = 540
UI_HEIGHT     = 140
FPS           = 60
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
GRAY       = (200, 200, 200)
DARK_GRAY  = (100, 100, 100)
LIGHT_BLUE = (150, 200, 255)
RED        = (255, 0,   0  )

COLORS = [
    BLACK,
    WHITE,
    (255, 0,   0  ),   # Red
    (0,   200, 0  ),   # Green
    (0,   0,   255),   # Blue
    (255, 255, 0  ),   # Yellow
    (255, 165, 0  ),   # Orange
    (128, 0,   128),   # Purple
    (255, 192, 203),   # Pink
    (0,   255, 255),   # Cyan
    (139, 69,  19 ),   # Brown
    (128, 128, 128),   # Gray
]
BRUSH_SIZES = {1: 2, 2: 5, 3: 10}
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint — TSIS 2")
clock = pygame.time.Clock()
font       = pygame.font.SysFont("Arial", 14)
font_bold  = pygame.font.SysFont("Arial", 14, bold=True)
text_font  = pygame.font.SysFont("Arial", 24)   # font used on canvas

class PaintApp:

    def __init__(self):
        self.canvas = pygame.Surface((SCREEN_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)

        self.tool          = 'pencil'
        self.color         = BLACK
        self.brush_size    = 2          
        self.size_level    = 1          

        # Shape / line drawing state
        self.drawing       = False
        self.start_pos     = None
        self.prev_pos      = None       
        self.temp_surface  = None       

        # Text tool state
        self.text_mode     = False
        self.text_pos      = None
        self.text_buffer   = ""

        self.tool_buttons  = {}
        self.color_buttons = []
        self.size_buttons  = {}
        self._build_ui()

    def _build_ui(self):
        btn_w, btn_h = 72, 30
        row1_y = CANVAS_HEIGHT + 10
        row2_y = CANVAS_HEIGHT + 50

        # Row 1 — drawing tools
        tools_row1 = [
            ('pencil',    'Pencil'),
            ('line',      'Line'),
            ('brush',     'Brush'),
            ('eraser',    'Eraser'),
            ('fill',      'Fill'),
            ('text',      'Text'),
            ('clear',     'Clear'),
        ]
        for i, (tid, label) in enumerate(tools_row1):
            x = 10 + i * (btn_w + 6)
            self.tool_buttons[tid] = {
                'rect':  pygame.Rect(x, row1_y, btn_w, btn_h),
                'label': label,
            }

        # Row 2 — shape tools
        tools_row2 = [
            ('rectangle',  'Rect'),
            ('square',     'Square'),
            ('circle',     'Circle'),
            ('right_tri',  'R-Tri'),
            ('eq_tri',     'E-Tri'),
            ('rhombus',    'Rhombus'),
        ]
        for i, (tid, label) in enumerate(tools_row2):
            x = 10 + i * (btn_w + 6)
            self.tool_buttons[tid] = {
                'rect':  pygame.Rect(x, row2_y, btn_w, btn_h),
                'label': label,
            }

        # Brush-size buttons (top-right area)
        size_labels = {1: 'S(1)', 2: 'M(2)', 3: 'L(3)'}
        for lvl, label in size_labels.items():
            x = SCREEN_WIDTH - 210 + (lvl - 1) * 68
            self.size_buttons[lvl] = {
                'rect':  pygame.Rect(x, row1_y, 62, 30),
                'label': label,
            }

        # Color palette — two rows on the right side
        c_size = 28
        cx_start = SCREEN_WIDTH - 210
        cy_start = CANVAS_HEIGHT + 52
        for i, c in enumerate(COLORS):
            x = cx_start + (i % 6) * (c_size + 4)
            y = cy_start + (i // 6) * (c_size + 4)
            self.color_buttons.append({
                'rect':  pygame.Rect(x, y, c_size, c_size),
                'color': c,
            })

    def _draw_ui(self):
        pygame.draw.rect(screen, GRAY, (0, CANVAS_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (0, CANVAS_HEIGHT), (SCREEN_WIDTH, CANVAS_HEIGHT), 2)

        # Tool buttons
        for tid, data in self.tool_buttons.items():
            rect = data['rect']
            bg = LIGHT_BLUE if tid == self.tool else WHITE
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            lbl = font.render(data['label'], True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        # Size buttons
        for lvl, data in self.size_buttons.items():
            rect = data['rect']
            bg = LIGHT_BLUE if lvl == self.size_level else WHITE
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            lbl = font_bold.render(data['label'], True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        # Color palette
        for cb in self.color_buttons:
            rect = cb['rect']
            pygame.draw.rect(screen, cb['color'], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if cb['color'] == self.color:
                pygame.draw.rect(screen, RED, rect, 3)

        # Status line
        status = f"Tool: {self.tool}   Size: {self.brush_size}px   Ctrl+S = Save"
        if self.text_mode:
            status = "TEXT MODE — type, Enter=confirm, Esc=cancel"
        lbl = font.render(status, True, DARK_GRAY)
        screen.blit(lbl, (10, CANVAS_HEIGHT + 90 + 28))

    def _handle_ui_click(self, pos):
        # Tool buttons
        for tid, data in self.tool_buttons.items():
            if data['rect'].collidepoint(pos):
                if tid == 'clear':
                    self.canvas.fill(WHITE)
                else:
                    self.tool = tid
                    # Exit text mode if switching away
                    if tid != 'text':
                        self._cancel_text()
                return True

        # Size buttons
        for lvl, data in self.size_buttons.items():
            if data['rect'].collidepoint(pos):
                self.size_level = lvl
                self.brush_size = BRUSH_SIZES[lvl]
                return True

        # Color buttons
        for cb in self.color_buttons:
            if cb['rect'].collidepoint(pos):
                self.color = cb['color']
                if self.tool == 'eraser':
                    self.tool = 'pencil'
                return True

        return False

    def _cancel_text(self):
        self.text_mode   = False
        self.text_pos    = None
        self.text_buffer = ""

    def _confirm_text(self):
        if self.text_pos and self.text_buffer:
            rendered = text_font.render(self.text_buffer, True, self.color)
            self.canvas.blit(rendered, self.text_pos)
        self._cancel_text()

    def _draw_text_cursor(self):
        """Show live text preview on screen (not burned into canvas yet)."""
        if not self.text_mode or self.text_pos is None:
            return
        preview = text_font.render(self.text_buffer + "|", True, self.color)
        screen.blit(preview, self.text_pos)

    SHAPE_TOOLS = {'rectangle', 'square', 'circle',
                   'right_tri', 'eq_tri', 'rhombus', 'line'}

    def _draw_shape_preview(self, end):
        self.canvas.blit(self.temp_surface, (0, 0))
        s = self.brush_size
        c = self.color
        st = self.start_pos

        if   self.tool == 'line':       tools.draw_straight_line(self.canvas, st, end, c, s)
        elif self.tool == 'rectangle':  tools.draw_rectangle(self.canvas, st, end, c, s)
        elif self.tool == 'square':     tools.draw_square(self.canvas, st, end, c, s)
        elif self.tool == 'circle':     tools.draw_circle(self.canvas, st, end, c, s)
        elif self.tool == 'right_tri':  tools.draw_right_triangle(self.canvas, st, end, c, s)
        elif self.tool == 'eq_tri':     tools.draw_equilateral_triangle(self.canvas, st, end, c, s)
        elif self.tool == 'rhombus':    tools.draw_rhombus(self.canvas, st, end, c, s)

    def _save(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"canvas_{timestamp}.png"
        pygame.image.save(self.canvas, filename)
        print(f"Saved: {filename}")
        # Flash a small message on screen
        msg = font_bold.render(f"Saved as {filename}", True, BLACK)
        screen.blit(msg, (10, 10))
        pygame.display.flip()
        pygame.time.wait(800)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():

                # ── Quit ──────────────────────────────────
                if event.type == pygame.QUIT:
                    running = False

                # ── Keyboard ──────────────────────────────
                if event.type == pygame.KEYDOWN:

                    # Text mode input
                    if self.text_mode:
                        if event.key == pygame.K_RETURN:
                            self._confirm_text()
                        elif event.key == pygame.K_ESCAPE:
                            self._cancel_text()
                        elif event.key == pygame.K_BACKSPACE:
                            self.text_buffer = self.text_buffer[:-1]
                        else:
                            if event.unicode and event.unicode.isprintable():
                                self.text_buffer += event.unicode
                        continue   

                    # Global shortcuts
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # Ctrl + S  →  save
                    if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        self._save()

                    if event.key == pygame.K_1:
                        self.size_level = 1;  self.brush_size = BRUSH_SIZES[1]
                    if event.key == pygame.K_2:
                        self.size_level = 2;  self.brush_size = BRUSH_SIZES[2]
                    if event.key == pygame.K_3:
                        self.size_level = 3;  self.brush_size = BRUSH_SIZES[3]

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos

                    # Click in UI bar
                    if pos[1] >= CANVAS_HEIGHT:
                        self._handle_ui_click(pos)
                        continue

                    # ── Text tool ──────────────────────────
                    if self.tool == 'text':
                        # Confirm previous if any, start new
                        self._confirm_text()
                        self.text_mode   = True
                        self.text_pos    = pos
                        self.text_buffer = ""
                        continue

                    # ── Fill tool ──────────────────────────
                    if self.tool == 'fill':
                        tools.flood_fill(self.canvas, pos, self.color)
                        continue

                    # ── Brush / pencil / eraser ────────────
                    if self.tool in ('brush', 'pencil', 'eraser'):
                        draw_color = WHITE if self.tool == 'eraser' else self.color
                        tools.draw_brush(self.canvas, pos, draw_color, self.brush_size)
                        self.prev_pos = pos
                        self.drawing  = True
                        continue

                    # ── Shape / line tools ─────────────────
                    if self.tool in self.SHAPE_TOOLS:
                        self.start_pos    = pos
                        self.temp_surface = self.canvas.copy()
                        self.drawing      = True

                # ── Mouse motion ──────────────────────────
                if event.type == pygame.MOUSEMOTION:
                    if not self.drawing:
                        continue
                    pos = event.pos
                    if pos[1] >= CANVAS_HEIGHT:
                        continue

                    if self.tool in ('brush', 'pencil'):
                        if self.prev_pos:
                            tools.draw_pencil_line(self.canvas, self.prev_pos, pos,
                                                   self.color, self.brush_size)
                        self.prev_pos = pos

                    elif self.tool == 'eraser':
                        tools.draw_brush(self.canvas, pos, WHITE, self.brush_size * 3)
                        self.prev_pos = pos

                    elif self.tool in self.SHAPE_TOOLS:
                        self._draw_shape_preview(pos)

                # ── Mouse button up ────────────────────────
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.tool in self.SHAPE_TOOLS and self.drawing:
                        # Finalise shape at release position
                        self._draw_shape_preview(event.pos)
                    self.drawing      = False
                    self.start_pos    = None
                    self.temp_surface = None
                    self.prev_pos     = None

            # ── Render ────────────────────────────────────
            screen.blit(self.canvas, (0, 0))
            self._draw_ui()
            self._draw_text_cursor()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    PaintApp().run()
