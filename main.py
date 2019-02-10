# TODO:
# - More visualization options (horizontal)
# - Set up automatic tests

import pygame
import sys
import random
import inspect

import algorithms
import initial
import visualizations
import colorschemes
import helper

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screen_rect = screen.get_rect()
font = pygame.font.SysFont('Arial', 20)

running = True
done    = False
speed = 0
zoom = 0
waiting_frames = 0


algorithm_list = list(filter(lambda x: inspect.isgeneratorfunction(eval('algorithms.' + x)), dir(algorithms)))
sort_dropdown = helper.Dropdown(algorithm_list, (330, 3), default="insertion_sort")
if len(sys.argv) > 1:
    algorithm = sys.argv[1]
else:
    algorithm = sort_dropdown.selected
sort_dropdown.selected = algorithm

visualization_list = list(filter(lambda x: inspect.isfunction(eval('visualizations.' + x)), dir(visualizations)))
vis_dropdown = helper.Dropdown(visualization_list, (100, 3), default="bars")
visualization = vis_dropdown.selected

color_list = list(filter(lambda x: inspect.isfunction(eval('colorschemes.' + x)), dir(colorschemes)))
color_dropdown = helper.Dropdown(color_list, (150, 3), default="simple")
color = color_dropdown.selected

initial_list = list(filter(lambda x: inspect.isfunction(eval('initial.' + x)), dir(initial)))
init_dropdown = helper.Dropdown(initial_list, (220, 3), default="shuffled")
init = init_dropdown.selected

def setup():
    global listy, algo, done, zoom
    done = False
    listy = eval(f"initial.{init}")(screen_rect.height, screen_rect.width//2**zoom)
    algo = eval(f"algorithms.{algorithm}")(listy)

def draw():
    eval(f"visualizations.{visualization}")(screen, screen_rect, listy, screen_rect.height, eval(f'colorschemes.{color}'), special)
    
    if speed < 0:
        speed_text = f"Speed: 1/{2**-speed}"
        
    else:
        speed_text = f"Speed: {2**speed}"
    screen.blit(font.render(speed_text, True, visualizations.white, visualizations.black), (3, 3))
    screen.blit(font.render(f"Zoom: {2**zoom}", True, visualizations.white, visualizations.black), (3, 23))

    sort_dropdown.draw(screen)
    vis_dropdown.draw(screen)
    color_dropdown.draw(screen)
    init_dropdown.draw(screen)

setup()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.VIDEORESIZE:
            screen_rect.size = event.dict['size']
            screen = pygame.display.set_mode(screen_rect.size, pygame.RESIZABLE)
            setup()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_SPACE:
                running = not running
            elif key == pygame.K_RIGHT:
                speed += 1
            elif key == pygame.K_LEFT:
                speed -= 1
            elif key == pygame.K_UP:
                zoom += 1
                setup()
            elif key == pygame.K_DOWN:
                if zoom > 0:
                    zoom -= 1
                    setup()
            elif key == pygame.K_RETURN:
                setup()
                draw()
        new_sort = sort_dropdown.process_event(event)
        if new_sort:
            algorithm = new_sort
            setup()
                
        new_vis = vis_dropdown.process_event(event)
        if new_vis:
            visualization = new_vis
        
        new_color = color_dropdown.process_event(event)
        if new_color:
            color = new_color
        
        new_init = init_dropdown.process_event(event)
        if new_init:
            init = new_init
            setup()
    
    if waiting_frames:
        waiting_frames -= 1

    if running and not done and not waiting_frames:
        if speed < 0:
            waiting_frames = 2**(-speed)
            times = 1
        else:
            times = 2**speed
        
        for _ in range(times):
            try:
                special = next(algo)
            except StopIteration:
                done = True
                special = None
    draw()
    pygame.display.update()