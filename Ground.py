import pygame

from Info import Info


class Ground:
    def __init__(self, y, width, height, colour, screen):
        self.x = 0
        self.y = y
        self.cx = (self.x + width)/2
        self.cy = (self.y + height)/2
        self.width = width
        self.height = height
        self.screen = screen
        self.colour = colour
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        Info.ground = self.hitbox

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.hitbox)

    def tick(self):
        pass
