class Camera():
    def __init__(self, target) -> None:
        self.x = target.x
        self.y = target.y
        self.target = target
        self.speed = 50
        self.zoom = 7
    
    def update(self, mouse_pos, dt):
        self.x -= (self.x - (self.target.x * 5 + mouse_pos[0]) / 6) / 10 * dt * self.speed
        self.y -= (self.y - ((self.target.y * 5 + mouse_pos[1]) / 6) + 1.5) / 10 * dt * self.speed