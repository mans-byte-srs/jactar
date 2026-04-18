import pygame
import datetime

def get_time_angles():
    now = datetime.datetime.now()
    # 1 секунд = 6 градус, 1 минут = 6 градус
    # Минус таңбасы сағат тілімен қозғалу үшін керек
    sec_angle = now.second * 6
    min_angle = now.minute * 6
    return sec_angle, min_angle

def rotate_hand(surf, image, angle, pos):
    # Суретті ортасынан айналдыру
    # Pygame-де 0 градус оң жақта, сондықтан суретті бастапқыда тік (жоғары) етіп алған дұрыс
    rotated_image = pygame.transform.rotate(image, -angle)
    rect = rotated_image.get_rect(center=pos)
    surf.blit(rotated_image, rect)