import pygame
from pygame.locals import *
from .debug import Debug


class Point:
    def __init__(self, position, mass, damping, static):
        self.position = position
        self.mass = mass
        self.damping = damping
        self.static = static

        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, 6)

    def update(self):
        self.velocity += self.acceleration
        
        if not self.static:
            self.position += self.velocity

        self.velocity *= self.damping
        self.acceleration *= 0

    def resolveBounds(self, ScreenSize, gravity):
        if self.position.x < 0:
            self.position.x = 0
            self.acceleration.x += gravity[1]
            self.velocity.x *= 0

        if self.position.x > ScreenSize[0]:
            self.position.x = ScreenSize[0]
            self.acceleration.x -= gravity[1]
            self.velocity.x *= 0

        if self.position.y < 0:
            self.position.y = 0
            self.acceleration.y += gravity[1]
            self.velocity.y *= 0

        if self.position.y > ScreenSize[1]:
            self.position.y = ScreenSize[1]
            self.acceleration.y -= gravity[1]
            self.velocity.y *= 0


class Spring:
    def __init__(self, point1, point2, stiffness, restLength, damping):
        self.point1 = point1
        self.point2 = point2

        self.stiffness = stiffness
        self.restLength = restLength
        self.damping = damping

        self.normalVec = pygame.Vector2(0, 0)
        self.length = self.GetLength()

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.point1.position,
                        self.point2.position, 3)

    def update(self):
        self.length = self.GetLength()
        self.normalVec = self.GetNormal()
        SpringForce = self.GetSpringForce()
        
        self.point1.acceleration += SpringForce / self.point1.mass
        self.point2.acceleration -= SpringForce / self.point2.mass
    
    def GetSpringForce(self):
        distance = self.point1.position - self.point2.position
        length = self.length
        if length != 0:
            normalVec = distance / length  
                
            springForce = -self.stiffness * (length - self.restLength)
            
            return springForce * normalVec

        return pygame.Vector2(0, 0)

    def GetNormal(self):
        '''
        gets perpendicular normal vector to the spring
        cool trick to get perpendicular vector:
        vec = [vec.y, -vec.x]
        pygame.Vector2 does this too but i still use mine
        '''
        SpringVec = self.point2.position - self.point1.position
        if SpringVec.length() != 0:
            normalVec = pygame.Vector2(SpringVec.y, -SpringVec.x).normalize()

            return normalVec
        
        return pygame.Vector2(0, 0)

    def DrawNormal(self, force, length):
        SpringVec = self.point2.position - self.point1.position
        startPos = SpringVec * 0.5 + self.point1.position
        endPos = startPos + (force * length)

        Debug.line(startPos, endPos, (0, 0, 0))

    def GetLength(self):
        return (self.point1.position - self.point2.position).length()