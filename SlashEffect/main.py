import pygame
import sys
import numpy as np

pygame.init()

win = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

def get_arch_points(w, h, n):

    x = np.linspace(0, w, 2*n+1)
    rev_x = np.linspace(w, 0, 2*n+1)
    w /= 2
    y1 = (-h/(w**2 )) * (x - w)**2 + h
    h /=2
    y2 = (-h/(w**2 )) * (x - w)**2 + h
    points = np.concatenate((np.stack((x, y1), axis=-1), np.stack((rev_x, y2), axis=-1)))
    return points

def draw():
    win.fill((0, 0, 0))


    points = get_arch_points(mouse_pos[0]/4, mouse_pos[0]/8, 4)
    slash_surf = pygame.Surface((mouse_pos[0]/4, mouse_pos[0]/8))
    pygame.draw.polygon(slash_surf, (255, 0, 0), np.concatenate((points[:slash], points[-(slash-1):])))
    win.blit(pygame.transform.scale(slash_surf, (mouse_pos[0], mouse_pos[1])), (0, 0))

    pygame.display.flip()


slash = 3
run = True
while run:
    dt = clock.tick() / 1000

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                slash += 1
                print(slash)
            if event.key == pygame.K_DOWN:
                slash -= 1
                print(slash)

    
    draw()