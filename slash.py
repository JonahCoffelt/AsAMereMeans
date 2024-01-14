import numpy as np
import random
import pygame
from pygame._sdl2.video import Texture

def get_arch_points(w, h, n, reverse=False):

    if reverse:
        rev_x = np.linspace(0, w, 2*n+1)
        x = np.linspace(w, 0, 2*n+1)
    else:
        x = np.linspace(0, w, 2*n+1)
        rev_x = np.linspace(w, 0, 2*n+1)
    w /= 2
    y1 = (-h/(w**2 )) * (x - w)**2 + h
    h /=2
    y2 = (-h/(w**2 )) * (x - w)**2 + h
    points = np.concatenate((np.stack((x, y1), axis=-1), np.stack((rev_x, y2), axis=-1)))
    return points

class Slash():
    def __init__(self, x, y, angle, movement, renderer, reverse=False) -> None:
        self.x, self.y, self.angle = x, y, angle
        self.velocity = 12 + int(movement[0] or movement[1])*6
        self.renderer = renderer
        self.w, self.h = random.randrange(25, 35), random.randrange(10, 25)
        self.points = get_arch_points(self.w, self.h, 4, reverse)
        self.lifetime = 0
    
    def draw(self, win_size, tile_size, cam, dt):
        self.lifetime += dt
        frame = min(9, int(self.lifetime * 50))

        slash_surf = pygame.Surface((self.w, self.h))
        pygame.draw.polygon(slash_surf, (255, 255, 255), np.concatenate((self.points[:frame+2], self.points[-(frame+1):])))
        slash_surf.set_colorkey((0, 0, 0))
        text = Texture.from_surface(self.renderer, slash_surf)

        self.x -= np.cos(self.angle) * self.velocity * dt
        self.y -= np.sin(self.angle) * self.velocity * dt
        self.velocity = max(self.velocity - dt * 65, 0)

        text.draw(dstrect=(self.x * tile_size - cam.x * tile_size + win_size[0]/2 - self.w * tile_size/20, self.y * tile_size - cam.y * tile_size + win_size[1]/2 - self.h * tile_size/20, self.w * tile_size/10, self.h * tile_size/10), angle=np.rad2deg(self.angle) + 90)