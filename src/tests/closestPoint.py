import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.TargetLine = [Vector2(250, 100), Vector2(300, 300)]
        self.rect = pygame.Rect(self.TargetLine[0], self.TargetLine[1] - self.TargetLine[0])
        
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

            pygame.draw.line(screen, (0, 0, 0), self.TargetLine[0], self.TargetLine[1], 1)
            pygame.draw.circle(screen, (0, 0, 0), pointPos, 3)

            ClosestPos = self.getClosest(pointPos, self.TargetLine, self.rect)
            if ClosestPos != False:
                pygame.draw.line(screen, (0, 0, 0), pointPos, ClosestPos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()

    def getClosest(self, position, edge, rect):
        TargetPointPos = position - edge[0] 

        EdgeVec = (edge[1] - edge[0])
        VecNormal = EdgeVec.normalize()
        normal = Vector2(VecNormal.y, -VecNormal.x)            

        distanceX = (EdgeVec - TargetPointPos).x * VecNormal.y
        distanceY = -(EdgeVec - TargetPointPos).y * VecNormal.x

        ClosestPos = normal * (distanceX + distanceY)
        ClosestPos += position

        if rect.collidepoint(ClosestPos):
            return ClosestPos
        
        return False

App((960, 540), 'Closest Point', 0).loop()