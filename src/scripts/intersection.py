import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
#import numpy #do if slow


pygame.init()

class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.TargetLine = [Vector2(100, 150), Vector2(125, 150)]
        self.Checkline = [Vector2(25, 128), Vector2(640, 128)]   
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = fps

    def getIntersection(self):
        '''
        My solution to get intersection between horizontal line and any line
        not cleanest one, but works
        '''
        self.TargetLine[1] = Mouse.position
        TargetVec = (self.TargetLine[1] - self.TargetLine[0]).normalize()
        TargetY = [vec.y for vec in self.TargetLine]

        #0 length check
        if self.TargetLine[0] == self.TargetLine[1].xy:
            return None

        #DO THE CHECK IF LINE INTERSECTS Y POSITION
        if not (min(TargetY) < self.Checkline[0].y and
                max(TargetY) > self.Checkline[0].y):
            return None

        #check if lines are parallel
        if TargetVec.y == 0:
            return None
        
        HeightBtwn = self.Checkline[0].y - self.TargetLine[0].y

        #check if line y direction has the same sign(+/-) height difference 
        if not (HeightBtwn > 0 and TargetVec.y > 0) and not (
            HeightBtwn < 0 and TargetVec.y < 0):

            return None
        
        position = TargetVec * HeightBtwn / TargetVec.y
        position += self.TargetLine[0]

        if position.x > self.Checkline[0].x and position.x < self.Checkline[1].x:
            return position
        else:
            return None

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            intersection = self.getIntersection()

            pygame.draw.line(screen, (0, 0, 0), self.Checkline[0], self.Checkline[1], 2)
            pygame.draw.line(screen, (0, 0, 0), self.TargetLine[0], self.TargetLine[1], 2)
            if intersection != None:
                pygame.draw.circle(screen, (255, 0, 0), intersection, 2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()

App((1280, 720), 'Intersection', 60).loop()
