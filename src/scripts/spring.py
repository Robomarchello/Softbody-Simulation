import pygame
from pygame.locals import *
from dataclasses import dataclass


@dataclass
class Point:
    #idk if i will use it (for later)
    position: pygame.Vector2
    mass: float
    velocity = pygame.Vector2(0, 0)
    acceleration = pygame.Vector2(0, 0)


class Spring:
    def __init__(self, position, mass, stiffness, damping, static=False):
        self.position = pygame.Vector2(position)
        self.mass = mass
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
        self.stiffness = stiffness

        self.connections = []

        self.gravity = pygame.Vector2(0, 0.5)
        self.damping = pygame.Vector2(damping, damping)

        self.static = static

    def draw(self, screen):
        for spring in self.connections:
            pygame.draw.line(screen, (0, 0, 0), self.position, spring[0].position, 3)

        pygame.draw.circle(screen, (255, 0, 0), self.position, 6)

    def update(self):
        self.applySpringForce()
        
        self.acceleration += self.gravity

        self.velocity += self.acceleration 
        self.position += self.velocity

        self.velocity = self.velocity.elementwise() * self.damping
        self.acceleration *= 0

    def applySpringForce(self):
        #spring = [SpringObject, RestLength]
        for spring in self.connections:
            maxLength = spring[1]
            distance = self.position - spring[0].position
            length = distance.length()
            if length != 0:
                normalVec = distance.normalize()
                
                springForce = (-self.stiffness * (length - maxLength)) / self.mass
                
                self.acceleration += springForce * normalVec

    def addForce(self, force):
        self.acceleration += force / self.mass

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