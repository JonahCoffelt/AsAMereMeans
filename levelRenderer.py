import pygame
from pygame._sdl2.video import Texture
import sheetLoader

class LevelRenderer():
    def __init__(self, renderer) -> None:
        self.renderer = renderer

        self.load_tile_textures()
        self.load_level('Levels/WallJump.txt')

    def load_tile_textures(self):
        self.tile_textures = []
        self.tile_surfaces = sheetLoader.load_sheet('Assets/primary_sheet.png', (16, 16), (13, 13)) # Get list of tile surfaces
        for tile in self.tile_surfaces:
            self.tile_textures.append(Texture.from_surface(self.renderer, tile))
    
    def load_level(self, path):
        with open (path, 'r') as file: self.level = eval(file.readline())
        self.chunck_textures = {}
        self.col = []
        self.grass = []
        chunk_size = 15
        for chunk in self.level['Collisions']:
            if ';' in chunk:
                chunkx, chunky = chunk.split(';')
                chunkx, chunky = int(chunkx), int(chunky)
                for y in range(chunk_size):
                    for x in range(chunk_size):
                        if self.level['Collisions'][chunk][x][y]:
                            self.col.append((x + chunkx * chunk_size, y + chunky * chunk_size))
        for chunk in self.level['Decor']:
            if ';' in chunk:
                chunkx, chunky = chunk.split(';')
                chunkx, chunky = int(chunkx), int(chunky)
                for y in range(chunk_size):
                    for x in range(chunk_size):
                        if self.level['Decor'][chunk][x][y]:
                            self.grass.append((x + chunkx * chunk_size, y + chunky * chunk_size))
        for layer in self.level:
            if not layer in ('Collisions', 'Decor', 'Custom'):
                self.chunck_textures[layer] = {}
                for chunk in self.level[layer]:
                    if ';' in chunk:
                        chunk_surf = pygame.Surface((16 * chunk_size, 16 * chunk_size))
                        for y in range(chunk_size):
                            for x in range(chunk_size):
                                if self.level[layer][chunk][x][y]:
                                    chunk_surf.blit(self.tile_surfaces[self.level[layer][chunk][x][y] - 1], (x * 16, y * 16))
                        chunk_surf.set_colorkey((0, 0, 0))
                        self.chunck_textures[layer][chunk] = Texture.from_surface(self.renderer, chunk_surf)

    def set_tile_size(self, win_size, zoom):
        self.win_size = win_size
        self.tile_size = (win_size[1] / 2) // zoom
    
    def draw(self, cam):
        chunk_size = 15
        chunk_pixel_size = self.tile_size * chunk_size
        for layer in self.chunck_textures:
            for chunk in self.chunck_textures[layer]:
                chunkx, chunky = chunk.split(';')
                chunkx, chunky = int(chunkx), int(chunky)
                self.chunck_textures[layer][chunk].draw(dstrect=(chunk_pixel_size * chunkx - cam.x * self.tile_size + self.win_size[0]/2, chunk_pixel_size * chunky - cam.y * self.tile_size + self.win_size[1]/2, chunk_pixel_size, chunk_pixel_size))