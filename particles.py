import pygame
from pygame._sdl2.video import Texture
import random

class ParticleHandeler():
    def __init__(self, renderer) -> None:
        self.renderer = renderer
        self.particles = []
    
    def add_particles(self, n, x, y, w, h, color=(255, 0, 255), glow=False, lifetime=.75, angle=0, angular_velocity=0, velocity=0, acceleration=0, gravity=0, simple_horiz_vel=0, simple_vert_vel=0, shape=0):
        for i in range(n):
            self.particles.append(Particle(self.renderer, x, y, w, h, color, glow, lifetime, angle, angular_velocity, velocity, acceleration, gravity, simple_horiz_vel + random.uniform(-2, 2), simple_vert_vel + random.uniform(-2, 2), shape))

    def draw(self, win_size, tile_size, cam):
        for particle in self.particles:
            particle.draw(win_size, tile_size, cam)
    
    def update(self, dt):
        removes = []
        for particle in self.particles:
            if particle.update(dt): removes.append(particle)
        for particle in removes:
            self.particles.remove(particle)

class Particle():
    def __init__(self, renderer, x, y, w, h, color=(255, 0, 255), glow=False, lifetime=.5, angle=0, angular_velocity=0, velocity=0, acceleration=0, gravity=0, simple_horiz_vel=0, simple_vert_vel=0, shape=0) -> None:
        self.renderer = renderer
        
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color = color
        self.glow = glow
        self.lifetime = lifetime
        self.orig_life = lifetime
        self.angle, self.angular_velocity = angle, angular_velocity
        self.velocity, self.acceleration = velocity, acceleration
        self.simple_velocity = [simple_horiz_vel, simple_vert_vel]
        self.gravity = gravity
        self.shape = shape

        if shape == 0:
            surf = pygame.Surface((1, 1))
            surf.fill(self.color)
            self.texture = Texture.from_surface(self.renderer, surf)
        elif shape == 1:
            w = self.w * 21
            h = self.w * 21
            points = [
                (w/2, 0),
                (w, h * 1/5),
                (w/2, h),
                (0, h * 1/5)
            ]
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.polygon(surf, self.color, points)
            self.texture = Texture.from_surface(self.renderer, surf)
        elif shape == 2:
            surf = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (7, 7), 7)
            self.texture = Texture.from_surface(self.renderer, surf)

        if self.glow:
            self.glow_size = .4
            self.texture.blend_mode = 2
    
    def draw(self, win_size, tile_size, cam):
        scale = self.lifetime / self.orig_life
        if self.glow:
            self.texture.alpha = 150
            self.texture.draw(dstrect=(((self.x - cam.x - self.glow_size/2 * scale) * tile_size + win_size[0]/2, (self.y - cam.y - self.glow_size/2 * scale) * tile_size + win_size[1]/2, (self.w + self.glow_size) * tile_size * scale, (self.h + self.glow_size) * tile_size * scale)), angle=self.angle)
            self.texture.alpha = 255
        self.texture.draw(dstrect=(((self.x - cam.x) * tile_size + win_size[0]/2, (self.y - cam.y) * tile_size + win_size[1]/2, self.w * tile_size * scale, self.h * tile_size * scale)), angle=self.angle)


    def update(self, dt):
        self.lifetime -= dt

        # Simple Physics
        self.simple_velocity[1] += self.gravity * dt

        self.x += self.simple_velocity[0] * dt
        self.y += self.simple_velocity[1] * dt

        # Angular Physics
        self.angle += self.angular_velocity * dt

        if self.lifetime < 0 : return True