import pygame
from pygame.locals import *
from .spring import Spring, Point
from .mouse import Mouse
from .polygon import Polygon
from .debug import Debug
from math import pi, sqrt


class PressureSoftbody:
    def __init__(self, ScreenSize, gas_amount, obstacles=[]):
        self.ScreenSize = ScreenSize

        self.points = []
        self.springs = []

        self.gas_amount = gas_amount
        self.area = 0

        self.polygon = None

        #these are polygon class 
        self.obstacles = obstacles

    def draw(self, screen):
        self.update()

        for spring in self.springs:
            spring.draw(screen)

        for point in self.points:
            point.draw(screen)

        self.polygon.draw(screen)

        Debug.text((5, 5), f'Area: {round(self.area, 2)}')
        Debug.text((5, 35), f'Gas Amount: {self.gas_amount}')

    def update(self):
        self.area = self.CalculateArea()
        
        for spring in self.springs:
            self.ApplyPressure(spring)
            spring.update()

        points = [point.position for point in self.points]
        self.polygon.update(points)

        for index, point in enumerate(self.points):
            point.update()
            point.resolveBounds(self.ScreenSize)
            self.CollisionResolve(index, point)


        points = [point.position for point in self.points]
        self.polygon.update(points)

    def CollisionResolve(self, index, point):
        '''
        Resolving collision with point and colliding edge
        Btw, there is collision detection 10x simpler, but works the same😭
        Not sure if which one to use
        '''

        #simpler collision detection, but works practically the same result
        '''for obstacle in self.obstacles:
            #[edgeIndex, closestPoint, normalVec]
            collision = obstacle.collisionResolve(point.position)

            if collision != False:
                point.position = collision[1]
                #print(collision[2].elementwise() * point.velocity)         
                point.acceleration -= collision[2] * point.gravity[1] #collision[2]# * point.velocity
                point.velocity *= 0'''

        for obstacle in self.obstacles:
            collision = obstacle.collisionResolve(point.position)
            if collision != False and obstacle.static:
                colPoint = self.points[index]
                colPoint.position = collision[1]        

                colPoint.acceleration -= collision[2] * colPoint.gravity[1]
                colPoint.velocity *= 0

            if collision != False and not obstacle.static:
                colPoint = self.points[index]
                colPoint.position = collision[1]     

                edge = obstacle.softbody.springs[collision[0]]

                edge.point1.position = collision[4][0] 
                edge.point2.position = collision[4][1]

                edge.point1.acceleration -= collision[3]
                edge.point2.acceleration += collision[3]
                edge.point1.velocity *= 0
                edge.point2.velocity *= 0

                colPoint.acceleration -= collision[2] #* colPoint.gravity[1]
                colPoint.velocity *= 0



    def CalculateArea(self):
        '''
        Simple, but inaccurate way to calculate area
        *Probably* will change it
        '''
        #i don't like that making 2 loops for x and y poses
        xPoses = [point.position.x for point in self.points]
        yPoses = [point.position.y for point in self.points]

        width = max(xPoses) - min(xPoses)
        height = max(yPoses) - min(yPoses)

        area = width * height
        if area == 0:
            area = 1

        return area

    def ApplyPressure(self, spring):
        '''
        Pressure Calculation and their application is here
        Here are 3 parts:
        1. Gathering needed values
        2. Pressure Force Calculation
        3. Applying the force to the spring points
        '''
        length = spring.length
        normalVec = spring.GetNormal()
        OneOverArea = 1 / self.area #smaller the the area, stronger the force

        PressureForce =  (OneOverArea * length * self.gas_amount) * normalVec

        spring.point1.acceleration += PressureForce# / spring.point1.mass
        spring.point2.acceleration += PressureForce# / spring.point2.mass

        spring.DrawNormal(PressureForce)


class SoftbodyBall(PressureSoftbody):
    def __init__(self, ScreenSize, center, radius, sides,
                mass, stiffness, damping, gas_amount, obstacles=[]):
        super().__init__(ScreenSize, gas_amount, obstacles)

        self.center = pygame.Vector2(center)
        self.radius = radius
        self.sides = sides

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
        
        indices = []
        for index, point in enumerate(self.points):
            nextPoint = index + 1
            if nextPoint >= len(self.points):
                nextPoint = 0
            
            indices.append([index, nextPoint])
            self.springs.append(
                Spring(point, self.points[nextPoint],
                    stiffness, sideLength, damping))

        points = [point.position for point in self.points]
        self.polygon = Polygon(points, indices, False, self)


# ---- Square softbody below which i don't need right now
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