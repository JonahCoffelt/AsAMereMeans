import asyncio
import sys
import pygame
from pygame._sdl2.video import Window, Renderer

import game

pygame.init()

class App():
    def __init__(self) -> None:
        self.win_size = (1280, 720)

        self.win = Window(title="Mere Means: ", size=self.win_size, resizable=True) # Creates and SDL2 Window
        self.win.maximize()
        self.renderer = Renderer(self.win)
        self.game = game.Game(self.renderer, self.win)

    def start(self):
        asyncio.run(self.game.start())

app = App()
app.start()
