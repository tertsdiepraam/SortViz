import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red   = (255,0,0)

def full(screen, screen_rect, listy, largest, colors, special=None):
    if not special:
        special = ()
    screen.fill((0,0,0))
    length = len(listy)
    for index, elem in enumerate(listy):
        x_pos = index*screen_rect.width // length
        width = (index + 1)*screen_rect.width//length - x_pos
        screen.fill(colors(elem, largest, index in special), (x_pos, 0, width, screen_rect.height))

def bars(screen, screen_rect, listy, largest, colors, special=None):
    if not special:
        special = ()
    screen.fill((0,0,0))
    length = len(listy)
    for index, elem in enumerate(listy):
        x_pos = index*screen_rect.width // length
        width = (index + 1)*screen_rect.width//length - x_pos
        screen.fill(colors(elem, largest, index in special), (x_pos, screen_rect.height-elem, width, elem))

def dots(screen, screen_rect, listy, largest, colors, special=None):
    if not special:
        special = ()
    screen.fill((0,0,0))
    length = len(listy)
    for index, elem in enumerate(listy):
        x_pos = index*screen_rect.width // length
        pygame.draw.circle(screen, colors(elem, largest, index in special), (x_pos, screen_rect.height-elem), 3)