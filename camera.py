import random

class Camera():
    def __init__(self, target) -> None:
        self.x = target.x
        self.y = target.y
        self.target = target
        self.speed = 50
        self.zoom = 7

        self.shake_timer = 0
        self.shake_intensity = 0
    
    def update(self, mouse_pos, dt):
        self.x -= (self.x - (self.target.x * 5 + mouse_pos[0]) / 6) / 10 * dt * self.speed
        self.y -= (self.y - ((self.target.y * 5 + mouse_pos[1]) / 6) + 1.5) / 10 * dt * self.speed

        if self.shake_timer:
            self.x += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.y += random.uniform(-self.shake_intensity, self.shake_intensity)
        
        self.shake_timer = max(0, self.shake_timer - dt)
    
    def shake(self, duration=.03, intensity=.08):
        self.shake_timer = duration
        self.shake_intensity = intensity