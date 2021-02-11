import os
import sys

import pygame

from Ball import Ball
from Ground import Ground
from Info import Info

pygame.mixer.init()
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1200
height = 650
c = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
Ball(100, 100, 50, (200, 0, 0), screen)
Ball(200, 100, 10, (100, 0, 0), screen)
Ball(300, 100, 20, (100, 0, 0), screen)
Ball(400, 100, 30, (100, 0, 0), screen)
# g = Ground(600, 2000, 50, (0, 0, 0), screen)
click = False
mousePos = None
prevPos = None
drags = [False] * len(Info.balls)
screen.fill((255, 255, 255))

while True:
    screen.fill((255, 255, 255))
    screen.blit(pygame.font.SysFont("Comic Sans", 30).render("Press g to toggle gravity", 1, (0, 0, 0)), (0, 0))
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                Info.gravity = 9.8 if Info.gravity == 0 else 0
                for i in Info.balls:
                    i.yvel = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            for i in range(len(drags)):
                if (mousePos[0] - Info.balls[i].cx) ** 2 + (mousePos[1] - Info.balls[i].cy) ** 2 < Info.balls[i].size ** 2:
                    drags[i] = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
            for i in range(len(drags)):
                drags[i] = False
    # g.draw()
    for i in range(len(drags)):
        if drags[i]:
            Info.balls[i].xvel = mousePos[0] - prevPos[0]
            Info.balls[i].yvel = mousePos[1] - prevPos[1]
    for i in range(len(drags)):
        Info.balls[i].tick(drags[i])
        Info.balls[i].draw()
    prevPos = mousePos
    pygame.display.update()
    c.tick(60)
