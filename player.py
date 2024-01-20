import pygame
import math
import random
import slash

class Player():
    def __init__(self, col, renderer) -> None:
        self.x = 10
        self.y = -5
        self.size = (1, 1.75)

        self.col = col
        self.renderer = renderer

        self.slash = None
        self.combo_timer = 0

        self.movement = [False, False, False, False, False] # Left, Right, Jump, Up, Down
        self.dash_timer = 0
        self.dashes = 1
        self.dash = [0, 0]

        # Horizontal Movement
        self.speed = 8
        self.acceleration = 75
        self.x_velocity = 0
    
        # Vertical Movement
        self.velocity = 0
        self.gravity = 40
        self.jump_height = -17
        self.jump = 1
        self.jump_que = 0
        self.cayote_timer = 0
        self.wall_jump_timers = [0, 0]
        self.air_time = 0
    
    def update(self, events, mouse_world_pos, particles, dt):
        self.col_directions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_w:
                    self.movement[3] = True
                if event.key == pygame.K_s:
                    self.movement[4] = True
                if event.key == pygame.K_SPACE:
                    self.movement[2] = True
                    self.jump_que = .1
                if event.key == pygame.K_LSHIFT:
                    if not self.dash_timer and self.dashes:
                        self.dashes -= 1
                        self.dash_timer = .25
                        if self.movement[0]: self.dash[0] -= self.speed * 2
                        if self.movement[1]: self.dash[0] += self.speed * 2
                        if self.movement[3]: self.dash[1] -= self.speed * 1.75
                        if self.movement[4]: self.dash[1] += self.speed * 1.75
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_w:
                    self.movement[3] = False
                if event.key == pygame.K_s:
                    self.movement[4] = False
                if event.key == pygame.K_SPACE:
                    self.movement[2] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.slash:
                    angle = math.atan2((self.y - mouse_world_pos[1] - self.size[1]/2), (self.x - mouse_world_pos[0]))
                    if self.combo_timer == 0:
                        self.slash = slash.Slash(self.x + math.cos(angle) * .1, self.y + math.sin(angle) * .1 - self.size[1]/2, angle, self.movement, self.renderer, reverse=False)
                        self.combo_timer: self.combo_timer = .5
                    elif self.combo_timer > 0:
                        self.slash = slash.Slash(self.x + math.cos(angle) * .1, self.y + math.sin(angle) * .1 - self.size[1]/2, angle, self.movement, self.renderer, reverse=True)
                        self.combo_timer = -.5
                    else:
                        self.slash = slash.Slash(self.x + math.cos(angle) * .1, self.y + math.sin(angle) * .1 - self.size[1]/2, angle, self.movement, self.renderer, stab=True)
                        self.combo_timer = 0

        if self.combo_timer > 0.0: 
            self.combo_timer = max(0.0, self.combo_timer - dt)
        elif self.combo_timer < 0.0:
            self.combo_timer = min(0.0, self.combo_timer + dt)

        if self.movement[0]: 
            self.x_velocity -= self.acceleration * dt
        if self.movement[1]:
            self.x_velocity += self.acceleration * dt
        if not self.movement[0] and not self.movement[1] or self.movement[0] and self.movement[1]: self.x_velocity = 0

        self.x_velocity = min(self.speed, self.x_velocity)
        self.x_velocity = max(-self.speed, self.x_velocity)

        self.dash_timer = max(0, self.dash_timer - dt)

        if self.dash_timer:
            self.x += self.dash[0] * dt
        else:
            self.x += self.x_velocity * dt
            self.dash = [0, 0]

        #Horizontal Collisions
        if self.collide():
            ledge = self.ledge_bump()
            if ledge:
                self.y = math.floor(self.y) - .001
            if self.movement[0]: #Left
                self.x = math.floor(self.x) - self.size[0]/2 + 1  + .01
                self.col_directions['left'] = True
            elif self.movement[1]: # Right
                self.x = math.floor(self.x) + self.size[0]/2 - .01
                self.col_directions['right'] = True

        if self.grounded():
            self.air_time = 0
            self.cayote_timer = .1
            if self.movement[0] or self.movement[1]: 
                if not random.randrange(int(1/(dt+.001))): particles.add_particles(random.randrange(2, 5), self.x, self.y, .15, .15, color=(122, 72, 65), gravity=10, simple_vert_vel=-3, angle=random.randrange(0, 360), angular_velocity=random.uniform(360, 720))
        else:
            self.air_time += dt
            if self.col_directions['left']:
                self.wall_jump_timers[0] = .2
            elif self.col_directions['right']:
                self.wall_jump_timers[1] = .2

        if self.jump_que:
            if self.cayote_timer and self.jump:
                self.jump_que = 0
                self.velocity = self.jump_height
                self.jump -= 1
            elif (self.col_directions['right'] or self.wall_jump_timers[1]) and self.air_time > .12:
                self.jump_que = 0
                self.velocity = self.jump_height / 1.25
                self.jump -= 1
                self.x_velocity = -10
            elif (self.col_directions['left'] or self.wall_jump_timers[0]) and self.air_time > .12:
                self.jump_que = 0
                self.velocity = self.jump_height / 1.25
                self.jump -= 1
                self.x_velocity = 10
            self.jump_que = max(0, self.jump_que - dt)


        self.cayote_timer = max(0, self.cayote_timer - dt)
        self.wall_jump_timers[0] = max(0, self.wall_jump_timers[0] - dt)
        self.wall_jump_timers[1] = max(0, self.wall_jump_timers[1] - dt)

        if not self.movement[2] or self.velocity > 0:
            self.velocity += self.gravity * dt * 1.65
        else:
            self.velocity += self.gravity * dt
        
        
        if self.col_directions['left'] or self.col_directions['right']:
            self.velocity = min(5, self.velocity)
        else:
            self.velocity = min(30, self.velocity)
        
        if not self.dash_timer: self.y += self.velocity * dt
        else: 
            self.velocity = self.dash[1]
            self.y += self.dash[1] * dt

        if self.collide():
            if self.velocity > 0 or self.dash[1] > 0: # Down
                if self.velocity > 10: particles.add_particles(random.randrange(5, 8), self.x, self.y, .2, .2, color=(122, 72, 65), gravity=10, simple_vert_vel=-3, angle=random.randrange(0, 360), angular_velocity=random.uniform(360, 720))
                self.y = math.floor(self.y) - .001
                self.velocity = 0
                self.jump = 1
                self.dashes = 1
                self.dash[1] = 0
            elif self.velocity < 0  or self.dash[1] < 0: # Up
                self.y = math.floor(self.y) + self.size[1] - 1
                self.velocity = 0
                self.dash[1] = 0

    def draw(self, win_size, tile_size, cam, dt):
        self.tile_size = tile_size
        self.renderer.draw_color = (255, 0, 0, 255)
        self.renderer.fill_rect((win_size[0]/2 - self.size[0]/2 * tile_size + (self.x - cam.x) * tile_size, win_size[1]/2 - self.size[1] * tile_size + (self.y - cam.y) * tile_size, self.size[0] * tile_size, self.size[1] * tile_size))
        if self.slash: 
            self.slash.draw(win_size, tile_size, cam, dt)
            if self.slash.lifetime >= .25: self.slash = None

    def collide(self):
        return (math.floor(self.x + self.size[0]/2), math.floor(self.y)) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y)) in self.col or (math.floor(self.x + self.size[0]/2), math.floor(self.y - self.size[1])) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y - self.size[1])) in self.col

    def ledge_bump(self):
        return not ((math.floor(self.x + self.size[0]/2), math.floor(self.y - .15)) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y - .15)) in self.col) and not ((math.floor(self.x + self.size[0]/2), math.floor(self.y - self.size[1])) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y - self.size[1])) in self.col) and ((math.floor(self.x + self.size[0]/2), math.floor(self.y)) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y)) in self.col)

    def grounded(self):
        return (math.floor(self.x + self.size[0]/2), math.floor(self.y + .005)) in self.col or (math.floor(self.x - self.size[0]/2), math.floor(self.y + .005)) in self.col