import pygame

def simple(elem, largest, special):
    return (255,0,0) if special else (255, 255, 255)

def hue(elem, largest, special):
    c = pygame.Color(0, 0, 0, 0)
    if special:
        sat = 0
    else:
        sat = 100
    c.hsva = (elem*360//largest, sat, 100, 100)
    return c

def lightness(elem, largest, special):
    c = pygame.Color(0, 0, 0, 0)
    if special:
        c.hsva = (0, 100, 100, 100)
    else:
        c.hsva = (0, 0, elem*100//largest, 100)
    return c