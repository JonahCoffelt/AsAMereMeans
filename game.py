import asyncio
import sys
import pygame
import levelRenderer
import player
import camera
import entity
import paralax
import particles

class Game():
    def __init__(self, renderer, win) -> None:
        self.win_size = (1280, 720)
        self.renderer = renderer
        self.win = win
        self.clock = pygame.time.Clock()

        self.level_renderer = levelRenderer.LevelRenderer(self.renderer)

        self.player = player.Player(self.level_renderer.col, self.renderer)
        self.cam = camera.Camera(self.player)

        self.bg = paralax.Background(self.renderer)
        self.particles = particles.ParticleHandeler(self.renderer)

        self.level_renderer.set_tile_size(self.win_size, self.cam.zoom)
    
    def update(self):
        self.level_renderer.set_tile_size(self.win_size, self.cam.zoom)

        self.player.update(self.events, self.mouse_world_pos, self.entities, self.particles, self.cam, self.dt)
        self.cam.update(self.mouse_world_pos, self.dt)
        self.particles.update(self.dt)
        
        removes = []
        for entity in self.entities:
            if entity.update(self.level_renderer.col, self.dt): removes.append(entity)
            if entity.acts: entity.act(self.player, self.level_renderer.col, self.dt)

        for entity in removes:
            #self.particles.add_particles(5, entity.x, entity.y, .4, .4, color=(225, 225, 225), glow=True, gravity=10, simple_vert_vel=-3, shape=2)
            self.particles.add_particles(1, entity.x, entity.y, .2, .2, color=(225, 225, 225), glow=True, gravity=10, simple_vert_vel=-3, shape=1)
            self.entities.remove(entity)

        self.draw()
    
    def draw(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        self.bg.draw(self.win_size, self.cam)

        self.level_renderer.draw(self.win_size, self.cam)
        self.player.draw(self.win_size, self.level_renderer.tile_size, self.cam, self.dt)
        for entity in self.entities: 
            entity.draw(self.cam, self.level_renderer.tile_size, self.win_size)

        self.particles.draw(self.win_size, self.level_renderer.tile_size, self.cam)

        self.renderer.present()
    
    async def start(self):

        self.entities = [entity.Enemey(self.renderer, 10, -10), entity.Enemey(self.renderer, 0, -10)]
        self.particles.add_particles(10, 0, 0, 1, 1, shape=1)

        self.run = True
        while self.run:
            self.dt = self.clock.tick(120) / 1000
            self.dt = min(self.dt, .03)
            self.win.title = "Mere Means: " + str(int(self.clock.get_fps()))

            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_world_pos = ((self.mouse_pos[0] - self.win_size[0]/2) / self.level_renderer.tile_size + self.cam.x, (self.mouse_pos[1] - self.win_size[1]/2) / self.level_renderer.tile_size + self.cam.y)
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.win_size = (event.w, event.h)
                    self.level_renderer.set_tile_size(self.win_size, self.cam.zoom)

            self.update()
            await asyncio.sleep(0)