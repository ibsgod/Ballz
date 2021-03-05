import math

import pygame

from Info import Info


class Ball:
    def __init__(self, x, y, size, colour, screen):
        self.x = x
        self.y = y
        self.size = size
        self.cx = self.x + self.size
        self.cy = self.y + self.size
        self.screen = screen
        self.colour = colour
        self.yvel = 0
        self.xvel = 0
        self.lastColl = []
        self.mass = math.pi * self.size**2
        Info.balls.append(self)
        self.wood = pygame.mixer.Sound("wood1.wav")
        self.woodd = pygame.mixer.Sound("wood2.wav")

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, (self.cx, self.cy), self.size)

    def tick(self, dragging):
        if not dragging:
            if not self.checkRect((self.cx, self.cy), self.size, Info.ground):
                self.yvel += Info.gravity
            else:
                self.yvel = min(self.yvel, 0)
                # friction
                # if self.xvel != 0:
                #     self.xvel -= self.xvel / abs(self.xvel)
                #     if abs(self.xvel) < 1:
                #         self.xvel = 0
        self.y += self.yvel
        self.x += self.xvel
        # self.y = max(0, min(self.y, Info.ground.y - self.size * 2))
        # self.x = max(0, min(self.x, 1200 - self.size * 2))
        if self.x < 0 or self.x + self.size*2 > 1200:
            self.xvel *= -1
            self.woodd.play()
        if Info.gravity > 0:
            self.y = min(self.y, 650 - self.size * 2)
        else:
            if self.y < 0 or self.y + self.size*2 > 650:
                self.yvel *= -1
                self.woodd.play()
            self.y = max(0, min(self.y, 650 - self.size * 2))
        self.x = max(0, min(self.x, 1200 - self.size * 2))
        self.cx = self.x + self.size
        self.cy = self.y + self.size
        for i in Info.balls:
            if (i.cx - self.cx) ** 2 + (i.cy - self.cy) ** 2 < self.size ** 2 + i.size ** 2:
                if i != self and self not in i.lastColl and i not in self.lastColl:
                    self.lastColl.append(i)
                    i.lastColl.append(self)
                    self.ballColl(i)
                    self.wood.play()
            else:
                if self in i.lastColl:
                    i.lastColl.remove(self)
                    self.lastColl.remove(i)

    def checkRect(self, pos, rad, rect):
        if rect is None:
            return False
        distx = abs(pos[0] - rect.x - rect.width / 2)
        disty = abs(pos[1] - rect.y - rect.height / 2)
        if distx > (rect.width / 2 + rad):
            return False
        if disty > (rect.height / 2 + rad):
            return False
        if distx <= (rect.width / 2):
            return True
        if disty <= (rect.height / 2):
            return True
        cornerDistance_sq = (distx - rect.width / 2) ** 2 + (disty - rect.height / 2) ** 2
        return (cornerDistance_sq <= (rad ** 2))

    def ballColl(self, ball):
        diff = ball.xvel - self.xvel
        leftmom = self.mass * self.xvel + ball.mass * ball.xvel
        leftmom -= diff * self.mass
        leftmom /= self.mass + ball.mass
        ball.xvel = leftmom
        self.xvel = leftmom + diff
        diff = ball.yvel - self.yvel
        leftmom = self.mass * self.yvel + ball.mass * ball.yvel
        leftmom -= diff * self.mass
        leftmom /= self.mass + ball.mass
        ball.yvel = leftmom
        self.yvel = leftmom + diff

