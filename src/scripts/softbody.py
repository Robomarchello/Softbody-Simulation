import pygame
from pygame.locals import *
from .spring import Spring
from .mouse import Mouse
from math import pi, sqrt


class Softbody:
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize

        self.springs = []

        self.holding = None
        self.holdRadius = 100

    def draw(self, screen):
        self.update()
        for spring in self.springs:
            spring.draw(screen)

    def update(self):
        for spring in self.springs:
            if not spring.static:
                spring.update()
                spring.resolveBounds(self.ScreenSize)

        if self.holding != None:
            self.holding.position = Mouse.position.copy()
            self.holding.velocity *= 0
            
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for spring in self.springs:
                    distance = (spring.position - Mouse.position).length()

                    if distance - self.holdRadius < 0:
                        self.holding = spring

        if event.type == MOUSEBUTTONUP:
            self.holding = None    


class SoftbodySquare(Softbody):
    def __init__(self, rect, ScreenSize):
        super().__init__(ScreenSize)

        mass = 10
        stiffness = 1.0
        damping = 0.90

        self.springs = [
            Spring(rect.topleft, mass, stiffness, damping),
            Spring(rect.topright, mass, stiffness, damping),
            Spring(rect.bottomright, mass, stiffness, damping),
            Spring(rect.bottomleft, mass, stiffness, damping)
        ]
        diagonalLen = sqrt(rect.width ** 2 + rect.height ** 2)
        self.springs[0].connections = [
        [self.springs[1], rect.width], [self.springs[2], diagonalLen],
        [self.springs[3], rect.width]
        ]
        self.springs[1].connections = [
        [self.springs[0], rect.width], [self.springs[2], rect.width],
        [self.springs[3], diagonalLen]
        ]
        self.springs[2].connections = [
        [self.springs[0], diagonalLen], [self.springs[1], rect.width],
        [self.springs[3], rect.width]
        ]
        self.springs[3].connections = [
        [self.springs[0], rect.width], [self.springs[1], diagonalLen],
        [self.springs[2], rect.width]
        ]


       
#copy def handle_event from softbody class when this done
class PressureSoftbody:
    '''Hey, not ready yet'''
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize

        self.springs = []

    def draw(self, screen):
        #for spring in self.springs:
        #    spring.draw(screen)

        self.springs[6].draw(screen)
        self.springs[7].draw(screen)
        
        self.update()

    def update(self):
        #calculate pressure
        print(self.springs[6].connections)


class SoftbodyBall(PressureSoftbody):
    '''Hey, not ready yet'''
    def __init__(self, ScreenSize, center, radius, sides):
        super().__init__(ScreenSize)

        self.center = pygame.Vector2(center)
        self.radius = radius
        self.sides = sides

        mass = 2
        stiffness = 0.25
        damping = 0.92

        sideLength = (2 * radius * pi) / self.sides
        self.springs = []
        AnglePerSide = 360 / sides
        for side in range(sides):
            angle = AnglePerSide * side
            position = pygame.Vector2(0, 0)
            position.from_polar((radius, angle))
            position += self.center
            
            self.springs.append(
                Spring(position, mass, stiffness, damping)
            )
        
        self.springs[6].connections = [[self.springs[7], sideLength]]