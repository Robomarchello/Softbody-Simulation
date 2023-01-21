import pygame
from pygame.locals import *
import math
from .mouse import Mouse


class Spring:
    def __init__(self, position, mass, stiffness, extension, static=False):
        self.position = pygame.Vector2(position)
        self.mass = mass
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
        self.stiffness = stiffness
        self.extension = extension

        self.connections = []

        self.gravity = pygame.Vector2(0, 0.5)
        self.damping = pygame.Vector2(0.97, 0.97)

        self.static = static

    def draw(self, screen):
        for spring in self.connections:
            pygame.draw.line(screen, (0, 0, 0), self.position, spring.position, 3)

        pygame.draw.circle(screen, (255, 0, 0), self.position, 6)

    def update(self):
        for spring in self.connections:
            distance = self.position - spring.position
            length = distance.length()
            angle = math.atan2(distance[1], distance[0])

            springForce = (-self.stiffness * (length - self.extension)) / self.mass
            
            self.acceleration.x += springForce * math.cos(angle)
            self.acceleration.y += springForce * math.sin(angle)

        self.acceleration += self.gravity

        self.velocity += self.acceleration 
        self.position += self.velocity

        self.velocity = self.velocity.elementwise() * self.damping
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
        stiffness = 0.25

        self.springs = [
            Spring(rect.topleft, mass, stiffness, rect.width),
            Spring(rect.topright, mass, stiffness, rect.width),
            Spring(rect.bottomright, mass, stiffness, rect.width),
            Spring(rect.bottomleft, mass, stiffness, rect.width)
        ]
        self.springs[0].connections = [self.springs[1], self.springs[2], self.springs[3]]
        self.springs[1].connections = [self.springs[0], self.springs[2], self.springs[3]]
        self.springs[2].connections = [self.springs[0], self.springs[1], self.springs[3]]
        self.springs[3].connections = [self.springs[0], self.springs[1], self.springs[2]]