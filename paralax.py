from pygame._sdl2.video import Texture
import sheetLoader

class Background():
    def __init__(self, renderer) -> None:
        self.renderer = renderer
        
        imgs = sheetLoader.load_sheet('Assets/MereMeansBG1-Sheet.png', (128, 72), (1, 4)) # Get list of background surfaces
        self.textures = []
        for img in imgs:
            self.textures.append(Texture.from_surface(self.renderer, img))
        imgs = []
    
    def draw(self, win_size, cam):
        width = win_size[1] * 16/9
        for i, img in enumerate(self.textures):
            img.draw(dstrect=(-(cam.x * (i + 1) * 5) % width, 0, width, win_size[1]))
            img.draw(dstrect=(-(cam.x * (i + 1) * 5) % width - width, 0, width, win_size[1]))
            img.draw(dstrect=(-(cam.x * (i + 1) * 5) % width + width - 1, 0, width, win_size[1]))