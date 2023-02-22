import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
from math import sqrt

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.TargetLine = [Vector2(0, 0), Vector2(300, 540)]
        self.Checkline = [Vector2(25, 128), Vector2(640, 128)]   
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = fps


    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            pointPos = Mouse.position

            pygame.draw.line(screen, (0, 0, 0), self.TargetLine[0], self.TargetLine[1], 3)
            pygame.draw.circle(screen, (0, 0, 0), pointPos, 3)
            
            TargetNormal = (self.TargetLine[1] - self.TargetLine[0]).normalize()
            normal = Vector2(TargetNormal.y, -TargetNormal.x)            

            distanceX = (self.TargetLine[1] - pointPos).x * TargetNormal.y
            distanceY = -(self.TargetLine[1] - pointPos).y * TargetNormal.x
            #print(distance)
            ClosestPos = normal * (distanceX + distanceY)
            ClosestPos += pointPos
            #pygame.draw.line(screen, (0, 0, 0), (0, 0), pointPos)
            pygame.draw.line(screen, (0, 0, 0), pointPos, ClosestPos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((960, 540), 'Closest Point', 0).loop()