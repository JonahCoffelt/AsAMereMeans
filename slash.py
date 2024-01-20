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

def get_stab_points(w, h):
    return [
        (w/2, 0),
        (w, h * 1/5),
        (w/2, h),
        (0, h * 1/5)
    ]

class Slash():
    def __init__(self, x, y, angle, movement, renderer, reverse=False, stab=False) -> None:
        self.renderer = renderer

        self.stab = stab

        self.x, self.y, self.angle = x, y, angle
        self.velocity = 12 + int(movement[0] or movement[1])*6

        if not self.stab: 
            self.acceleration = 65
            self.w, self.h = random.randrange(25, 35), random.randrange(10, 25)
            self.points = list(get_arch_points(self.w, self.h, 4, reverse))

        else: 
            self.acceleration = 150
            self.w, self.h = random.randrange(5, 12), random.randrange(40, 50)
            self.points = list(get_stab_points(self.w, self.h))

        self.lifetime = 0
        self.prev_frame = -1
        self.scale = 0
        self.alpha = 255
    
    def draw(self, win_size, tile_size, cam, dt):
        self.lifetime += dt
        frame = min(9, int(self.lifetime * 50))
        if frame >= 4:
            self.scale += 150 * dt
            self.alpha -= 500 * dt

        self.alpha = max(0, self.alpha)

        self.x -= np.cos(self.angle) * self.velocity * dt
        self.y -= np.sin(self.angle) * self.velocity * dt
        self.velocity = max(self.velocity - dt * self.acceleration, 0)

        if frame > self.prev_frame:
            self.prev_frame = frame
            
            self.slash_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            if self.stab: pygame.draw.polygon(self.slash_surf, (255, 255, 255), self.points)
            else: pygame.draw.polygon(self.slash_surf, (255, 255, 255), np.concatenate((self.points[:frame+2], self.points[-(frame+1):])))
            self.text = Texture.from_surface(self.renderer, self.slash_surf)

        self.text.alpha = self.alpha
        self.text.draw(dstrect=(self.x * tile_size - cam.x * tile_size + win_size[0]/2 - self.w * tile_size/20 + self.scale, self.y * tile_size - cam.y * tile_size + win_size[1]/2 - self.h * tile_size/20 + self.scale, self.w * tile_size/10 - self.scale * 2, self.h * tile_size/10 - self.scale * 2), angle = np.rad2deg(self.angle) + 90)