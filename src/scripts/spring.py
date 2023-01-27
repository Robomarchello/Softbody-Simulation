import pygame
from pygame.locals import *


#tried to make this dataclass, but it didn't worked as i expected😭
class Point:
    def __init__(self, position, mass, damping, static):
        self.position = position
        self.mass = mass
        self.damping = damping
        self.static = static
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

    @property
    def gravity(self):
        return pygame.Vector2(0, 0.1) * self.mass

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, 6)

    def update(self):
        self.acceleration += self.gravity

        self.velocity += self.acceleration
        if not self.static:
            self.position += self.velocity

        self.velocity *= self.damping

        self.acceleration *= 0

    def resolveBounds(self, ScreenSize):
        if self.position.x < 0:
            self.position.x = 0
            self.acceleration.x += self.gravity[1]

        if self.position.x > ScreenSize[0]:
            self.position.x = ScreenSize[0]
            self.acceleration.x -= self.gravity[1]

        if self.position.y < 0:
            self.position.y = 0
            self.acceleration.y += self.gravity[1]

        if self.position.y > ScreenSize[1]:
            self.position.y = ScreenSize[1]
            self.acceleration.y -= self.gravity[1]


class Spring:
    def __init__(self, point1, point2, stiffness, restLength, damping):
        self.point1 = point1
        self.point2 = point2

        self.stiffness = stiffness
        self.restLength = restLength
        self.damping = damping

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.point1.position,
                        self.point2.position, 3)

    def update(self):
        SpringForce = self.GetSpringForce()
        
        self.point1.acceleration += SpringForce / self.point1.mass
        self.point2.acceleration -= SpringForce / self.point2.mass
    
    def GetSpringForce(self):
        distance = self.point1.position - self.point2.position
        length = distance.length()
        if length != 0:
            normalVec = distance.normalize()
                
            springForce = (-self.stiffness * (length - self.restLength))
            
            return springForce * normalVec

        return pygame.Vector2(0, 0)