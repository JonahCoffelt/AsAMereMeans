import asyncio
import sys
import pygame
import levelRenderer
import player
import camera

class Game():
    def __init__(self, renderer, win) -> None:
        self.win_size = (1280, 720)
        self.renderer = renderer
        self.win = win
        self.clock = pygame.time.Clock()

        self.level_renderer = levelRenderer.LevelRenderer(self.renderer)

        self.player = player.Player(self.level_renderer.col, self.renderer)
        self.cam = camera.Camera(self.player)

        self.level_renderer.set_tile_size(self.win_size, self.cam.zoom)
    
    def update(self):

        self.level_renderer.set_tile_size(self.win_size, self.cam.zoom)

        self.player.update(self.events, self.mouse_world_pos, self.dt)
        self.cam.update(self.mouse_world_pos, self.dt)

        self.draw()
    
    def draw(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        self.level_renderer.draw(self.cam)
        self.player.draw(self.win_size, self.level_renderer.tile_size, self.cam, self.dt)

        self.renderer.present()
    
    async def start(self):
        self.run = True
        while self.run:
            self.dt = self.clock.tick(120) / 1000
            self.win.title = "Mere Means: " + str(int(self.clock.get_fps()))

            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_world_pos = ((self.mouse_pos[0] - self.win_size[0]/2) / self.level_renderer.tile_size + self.player.x, (self.mouse_pos[1] - self.win_size[1]/2) / self.level_renderer.tile_size + self.player.y)
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