class Ball:
    def __init__(self, x, y, radius, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen_width = width
        self.screen_height = height
        self.speed = 20

    def move(self, dx, dy):
        # Жаңа позицияны есептеу
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Шекараны тексеру (экраннан шығып кетпеуі керек)
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y