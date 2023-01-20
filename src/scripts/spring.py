import pygame
from pygame.locals import *
import math


class Spring:
    def __init__(self, position, mass, stiffness, extension, static=False):
        self.position = position
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


class Softbody:
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize

        self.springs = [
            Spring(pygame.Vector2(440, 100), 10, 0.1, 350),
            Spring(pygame.Vector2(840, 100), 10, 0.1, 350),
            Spring(pygame.Vector2(440, 500), 10, 0.1, 350),
            Spring(pygame.Vector2(840, 500), 10, 0.1, 350),
        ]
        self.springs[0].connections = [self.springs[1], self.springs[2], self.springs[3]]
        self.springs[1].connections = [self.springs[0], self.springs[2], self.springs[3]]
        self.springs[2].connections = [self.springs[0], self.springs[1], self.springs[3]]
        self.springs[3].connections = [self.springs[0], self.springs[1], self.springs[2]]

    def draw(self, screen):
        self.update()
        for spring in self.springs:
            spring.draw(screen)

    def update(self):
        for spring in self.springs:
            if not spring.static:
                spring.update()
        self.resolveBounds()

    def resolveBounds(self):
        '''resolve bound collision with softbody'''
        for spring in self.springs:
            if spring.position.x < 0:
                spring.position.x = 0
                spring.acceleration.x += 1

            if spring.position.x > self.ScreenSize[0]:
                spring.position.x = self.ScreenSize[0]
                spring.acceleration.x -= 1

            if spring.position.y < 0:
                spring.position.y = 0
                spring.acceleration.y += 0.5

            if spring.position.y > self.ScreenSize[1]:
                spring.position.y = self.ScreenSize[1]
                spring.acceleration.y -= 0.5

    def handle_event(self, event):
        pass