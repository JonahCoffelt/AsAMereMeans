import pygame
import math
import numpy as np

class Entity():
    def __init__(self, renderer, x, y) -> None:
        self.renderer = renderer
        self.x, self.y = x, y
        self.size = [.9, .9]
        self.velocity = [0, 0]
        self.gravity = 40

        self.acts = False
        self.hit_cooldown = 0
        self.health = 1
        self.speed = 0
        self.knockback = 4
        self.jumps = 1
        self.total_jumps = 1
    
    def update(self, col, dt):
        if self.hit_cooldown: self.hit_cooldown = max(0, self.hit_cooldown - dt)
        self.velocity[1] += self.gravity * dt

        self.y += self.velocity[1] * dt
        if self.collide(col):
            if self.velocity[1] > 1:
                self.y = math.floor(self.y) + 1 - self.size[1]/2 - .001
                self.velocity[1] = 1
                self.jumps = self.total_jumps
        
        if self.velocity[0] > 0: self.velocity[0] = max(0, self.velocity[0] - 10 * dt)
        if self.velocity[0] < 0: self.velocity[0] = min(0, self.velocity[0] + 10 * dt)
        self.x += self.velocity[0] * dt
        if self.collide(col):
            if self.velocity[0] > 1: #Right
                self.x = math.floor(self.x) - self.size[0]/2 + 1
                self.velocity[0] = 0
            if self.velocity[0] < 1: #Left
                self.x = math.floor(self.x) + self.size[0]/2
                self.velocity[0] = 0
        
        if self.health <= 0: return True
        return False

    def draw(self, cam, tile_size, win_size):
        self.rect = pygame.Rect(((self.x - cam.x) * tile_size + win_size[0]/2 - tile_size * self.size[0] / 2, (self.y - cam.y) * tile_size + win_size[1]/2 - tile_size * self.size[1] / 2, tile_size * self.size[0], tile_size * self.size[1]))
        self.renderer.fill_rect(self.rect)

    def hit(self, other, damage, knockback_multiplier):
        if not self.hit_cooldown:
            self.hit_cooldown = .3
            self.health -= damage
            self.velocity[0] -= self.knockback * knockback_multiplier * ((other.x - self.x) / abs((other.x - self.x)))

    def slash_collide(self, player):
        if self.hit_cooldown <= 0:
            player_angle = math.atan2((player.y - (self.y)), (player.x - self.x))
            lower = player.slash.angle - 1
            upper = player.slash.angle + 1
            if (player_angle - lower) % 6.2831 <= (upper - lower) % 6.2831:
                if math.sqrt(((player.x) - (self.x)) ** 2 + ((player.y - player.size[1]/2) - (self.y)) ** 2) < 3:
                    self.hit_cooldown = .25
                    if self.x != player.x:
                        self.velocity[0] -= self.knockback * ((player.x - self.x) / abs((player.x - self.x)))
            elif math.sqrt(((player.x) - (self.x)) ** 2 + ((player.y - player.size[1]/2) - (self.y)) ** 2) < .75:
                self.hit_cooldown = .25
                if self.x != player.x:
                    self.velocity[0] -= self.knockback * ((player.x - self.x) / abs((player.x - self.x)))

    def collide(self, col):
        return (math.floor(self.x + self.size[0]/2), math.floor(self.y + self.size[1]/2)) in col or (math.floor(self.x - self.size[0]/2), math.floor(self.y + self.size[1]/2)) in col or (math.floor(self.x + self.size[0]/2), math.floor(self.y - self.size[1]/2)) in col or (math.floor(self.x - self.size[0]/2), math.floor(self.y - self.size[1]/2)) in col

    def grounded(self, col):
        return (math.floor(self.x + self.size[0]/2), math.floor(self.y + .005)) in col or (math.floor(self.x - self.size[0]/2), math.floor(self.y + .005)) in col

class Box(Entity):
    def __init__(self, renderer, x, y) -> None:
        super().__init__(renderer, x, y)

    def draw(self, cam, tile_size, win_size):
        self.renderer.draw_color = (150, 75, 0, 255)
        self.rect = pygame.Rect(((self.x - cam.x) * tile_size + win_size[0]/2 - tile_size * self.size[0] / 2, (self.y - cam.y) * tile_size + win_size[1]/2 - tile_size * self.size[1] / 2, tile_size * self.size[0], tile_size * self.size[1]))
        self.renderer.fill_rect(self.rect)

class Enemey(Entity):
    def __init__(self, renderer, x, y) -> None:
        super().__init__(renderer, x, y)
        self.speed = 4.5
        self.knockback = 10
        self.jumps = 2
        
        self.acts = True
        self.pursuing = False
        self.pursue_distance = 10
        self.end_pursue_distance = 15
        self.attack_distance = 2


    def draw(self, cam, tile_size, win_size):
        self.renderer.draw_color = (150, 75, 255, 255)
        self.rect = pygame.Rect(((self.x - cam.x) * tile_size + win_size[0]/2 - tile_size * self.size[0] / 2, (self.y - cam.y) * tile_size + win_size[1]/2 - tile_size * self.size[1] / 2, tile_size * self.size[0], tile_size * self.size[1]))
        self.renderer.fill_rect(self.rect)

    def act(self, other, col, dt):
        if self.inRange(other, self.attack_distance): # attack behavior
            self.pursuing = False
        elif self.inRange(other, self.pursue_distance):
            if self.LOS(other, col):
                self.pursuing = True
        elif not self.inRange(other, self.end_pursue_distance):
            self.pursuing = False
        
        if self.pursuing: self.pursue(other, col, dt)

    def pursue(self, other, col, dt):
        dir = int(other.x > self.x) * 2 - 1
        self.velocity[0] += dir * dt * 20

        if dir > 0 and ((math.floor(self.x + 1), math.floor(self.y)) in col or (not (math.floor(self.x + .25), math.floor(self.y + 1)) in col and not (math.floor(self.x + .25), math.floor(self.y + 2)) in col and (math.floor(self.x - .15), math.floor(self.y + 1)) in col)) and self.jumps and self.velocity[1] >= 0: 
            self.velocity[1] = -13
            self.jumps -= 1
        elif dir < 0 and ((math.floor(self.x - 1), math.floor(self.y)) in col or (not (math.floor(self.x - .25), math.floor(self.y + 1)) in col and not (math.floor(self.x - .25), math.floor(self.y + 2)) in col and (math.floor(self.x + .15), math.floor(self.y + 1)) in col)) and self.jumps and self.velocity[1] >= 0: 
            self.velocity[1] = -13
            self.jumps -= 1

        if dir > 0: self.velocity[0] = min(self.speed, self.velocity[0])
        else: self.velocity[0] = max(-self.speed, self.velocity[0])

    def inRange(self, other, dist):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2) <= dist

    def LOS(self, other, col):
        sight_line = [np.array([self.x, self.y - 1]), np.array([other.x, other.y - 1])]

        visable = True

        magnitude = math.sqrt(sum(i ** 2 for i in (sight_line[1] - sight_line[0])))
        step_vector = (sight_line[1] - sight_line[0]) / magnitude / 4
        total_steped_distance = 0
        check_pos = np.array([self.x, self.y - 1])

        while abs(total_steped_distance) < abs(magnitude):
            if (math.floor(check_pos[0]), math.floor(check_pos[1])) in col:
                visable = False
                break
            check_pos += step_vector
            total_steped_distance += .25

        return visable
        