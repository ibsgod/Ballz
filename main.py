import os
import random
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
# g = Ground(600, 2000, 50, (0, 0, 0), screen)
click = False
mousePos = None
prevPos = None
drags = []
screen.fill((255, 255, 255))

while True:
    screen.fill((255, 255, 255))
    screen.blit(pygame.font.SysFont("Comic Sans", 30).render("Press g to toggle gravity", True, (0, 0, 0)), (0, 0))
    screen.blit(pygame.font.SysFont("Comic Sans", 30).render("Press b to add ball", True, (0, 0, 0)), (0, 30))
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                Info.gravity = 9.8 if Info.gravity == 0 else 0
                for i in Info.balls:
                    i.yvel = 0
            if event.key == pygame.K_b:
                Ball(random.randint(0, 1140), random.randint(0, 590), random.randint(5, 60), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), screen)
                drags.append(False)
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
