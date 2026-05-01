import pygame
import math
from collections import deque


def draw_brush(canvas, pos, color, size):
   
    pygame.draw.circle(canvas, color, pos, size)


def draw_pencil_line(canvas, prev_pos, curr_pos, color, size):
    
    pygame.draw.line(canvas, color, prev_pos, curr_pos, size * 2)
   
    pygame.draw.circle(canvas, color, curr_pos, size)


def draw_straight_line(canvas, start, end, color, size):
   
    pygame.draw.line(canvas, color, start, end, size * 2)


def draw_rectangle(canvas, start, end, color, size):
   
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    if w > 0 and h > 0:
        pygame.draw.rect(canvas, color, (x, y, w, h))
        pygame.draw.rect(canvas, (0, 0, 0), (x, y, w, h), max(1, size))


def draw_square(canvas, start, end, color, size):
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = max(abs(dx), abs(dy))
    x = start[0] if dx >= 0 else start[0] - side
    y = start[1] if dy >= 0 else start[1] - side
    if side > 0:
        pygame.draw.rect(canvas, color, (x, y, side, side))
        pygame.draw.rect(canvas, (0, 0, 0), (x, y, side, side), max(1, size))


def draw_circle(canvas, start, end, color, size):
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    radius = int(math.sqrt(dx**2 + dy**2))
    if radius > 0:
        pygame.draw.circle(canvas, color, start, radius)
        pygame.draw.circle(canvas, (0, 0, 0), start, radius, max(1, size))


def draw_right_triangle(canvas, start, end, color, size):
    
    points = [
        start,
        (end[0], start[1]),
        end,
    ]
    pygame.draw.polygon(canvas, color, points)
    pygame.draw.polygon(canvas, (0, 0, 0), points, max(1, size))


def draw_equilateral_triangle(canvas, start, end, color, size):
    
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = math.sqrt(dx**2 + dy**2)
    if side > 0:
        angle = math.atan2(dy, dx)
        p3 = (
            int(start[0] + side * math.cos(angle + math.pi / 3)),
            int(start[1] + side * math.sin(angle + math.pi / 3))
        )
        points = [start, end, p3]
        pygame.draw.polygon(canvas, color, points)
        pygame.draw.polygon(canvas, (0, 0, 0), points, max(1, size))


def draw_rhombus(canvas, start, end, color, size):
   
    cx = (start[0] + end[0]) / 2
    cy = (start[1] + end[1]) / 2
    d1x = end[0] - start[0]
    d1y = end[1] - start[1]
    # Perpendicular diagonal
    d2x = -d1y
    d2y = d1x
    points = [
        start,
        (int(cx + d2x / 2), int(cy + d2y / 2)),
        end,
        (int(cx - d2x / 2), int(cy - d2y / 2)),
    ]
    pygame.draw.polygon(canvas, color, points)
    pygame.draw.polygon(canvas, (0, 0, 0), points, max(1, size))


def flood_fill(canvas, start_pos, fill_color):
    x, y = start_pos
    width, height = canvas.get_size()

   
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = canvas.get_at((x, y))
    # Convert to plain tuple (ignore alpha)
    target_color = (target_color.r, target_color.g, target_color.b)
    fill_rgb = (fill_color[0], fill_color[1], fill_color[2])

    # Nothing to fill if same color
    if target_color == fill_rgb:
        return

    visited = set()
    queue = deque()
    queue.append((x, y))
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        current = canvas.get_at((cx, cy))
        current_rgb = (current.r, current.g, current.b)

        if current_rgb != target_color:
            continue

        canvas.set_at((cx, cy), fill_color)

        # Check 4 neighbors
        for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
