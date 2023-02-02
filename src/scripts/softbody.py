import pygame
from pygame.locals import *
from .spring import Spring, Point
from .mouse import Mouse
from .debug import Debug
from math import pi, sqrt


class Softbody:
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize

        self.points = []
        self.springs = []

        self.holding = None
        self.holdRadius = 100

    def draw(self, screen):
        self.update()
        for spring in self.springs:
            spring.draw(screen)

        for point in self.points:
            point.draw(screen)

    def update(self):
        for spring in self.springs:
            spring.update()

        for point in self.points:
            point.update()
            point.resolveBounds(self.ScreenSize)

        if self.holding != None:
            self.holding.position = Mouse.position.copy()
            self.holding.velocity *= 0
            
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for point in self.points:
                    distance = (point.position - Mouse.position).length()

                    if distance - self.holdRadius < 0:
                        self.holding = point

        if event.type == MOUSEBUTTONUP:
            self.holding = None    


class SoftbodySquare(Softbody):
    def __init__(self, rect, ScreenSize):
        super().__init__(ScreenSize)

        mass = 10
        stiffness = 1.0
        damping = 0.92

        self.points = [
            Point(pygame.Vector2(rect.topleft), mass, damping, False),
            Point(pygame.Vector2(rect.topright), mass, damping, False),
            Point(pygame.Vector2(rect.bottomright), mass, damping, False),
            Point(pygame.Vector2(rect.bottomleft), mass, damping, False)
        ]

        diagonalLen = sqrt(rect.width ** 2 + rect.height ** 2)
        self.springs = [
            Spring(self.points[0], self.points[1], stiffness, rect.width, damping),
            Spring(self.points[1], self.points[2], stiffness, rect.width, damping),
            Spring(self.points[2], self.points[3], stiffness, rect.width, damping),
            Spring(self.points[3], self.points[0], stiffness, rect.width, damping),
            Spring(self.points[0], self.points[2], stiffness, diagonalLen, damping),
            Spring(self.points[1], self.points[3], stiffness, diagonalLen, damping)
        ]


class PressureSoftbody:
    '''Hey, not ready yet'''
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize

        self.points = []
        self.springs = []

        self.gas_amount = 2500.0
        self.area = 0

    def draw(self, screen):
        self.update()
        for spring in self.springs:
            spring.draw(screen)

        for point in self.points:
            point.draw(screen)

        for spring in self.springs:
            line = spring.NormalVisulalize()
            Debug.line(line[0], line[1], (100, 100, 100))

    def update(self):
        self.area = self.CalculateArea()
        
        for spring in self.springs:
            self.ApplyPressure(spring)
            spring.update()

        for point in self.points:
            point.update()
            point.resolveBounds(self.ScreenSize)
    
    def CalculateArea(self):
        '''
        Simple, but inaccurate way to calculate area
        *Probably* will change it
        '''
        xPoses = [point.position.x for point in self.points]
        yPoses = [point.position.y for point in self.points]
        width = max(xPoses) - min(xPoses)
        height = max(yPoses) - min(yPoses)

        area = width * height

        Debug.text((5, 5), f'Area: {round(area, 2)}')

        return area

    def ApplyPressure(self, spring):
        '''
        Pressure Calculations and their application is here
        Here are 3 parts:
        1. Gathering 
        2. Pressure Force Calculation
        3. Applying the force to the spring points
        '''
        length = spring.GetLength()
        normalVec = spring.GetNormal()
        OneOverArea = 1 / self.area #smaller the the area, bigger the force

        PressureForce =  (OneOverArea * length * self.gas_amount) * normalVec

        spring.point1.acceleration += PressureForce# / spring.point1.mass
        spring.point2.acceleration += PressureForce# / spring.point2.mass


class SoftbodyBall(PressureSoftbody):
    '''Hey, not ready yet'''
    def __init__(self, ScreenSize, center, radius, sides):
        super().__init__(ScreenSize)

        self.center = pygame.Vector2(center)
        self.radius = radius
        self.sides = sides

        mass = 10
        stiffness = 1.0
        damping = 0.92

        sideLength = (2 * radius * pi) / self.sides

        AnglePerSide = 360 / sides
        for side in range(sides):
            angle = AnglePerSide * side
            position = pygame.Vector2(0, 0)
            position.from_polar((radius, angle))
            position += self.center
            
            self.points.append(
                Point(position, mass, damping, False)
            )
        
        for index, point in enumerate(self.points):
            nextPoint = index + 1
            if nextPoint >= len(self.points):
                nextPoint = 0

            self.springs.append(
                Spring(point, self.points[nextPoint],
                    stiffness, sideLength, damping))