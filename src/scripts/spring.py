import pygame
from pygame.locals import *
import math


#spring force = -stiffness * extension
#force = mass * acc
#acc = force / mass 
class Spring:
    def __init__(self, PivotPos, position, mass, stiffness, extension):
        self.PivotPos = PivotPos

        self.position = position
        self.mass = mass
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
        self.stiffness = stiffness
        self.extension = extension

        self.gravity = pygame.Vector2(0, 0.5)
        self.damping = pygame.Vector2(0.98, 0.98)

    def draw(self, screen):
        self.update()

        pygame.draw.line(screen, (0, 0, 0), self.PivotPos, self.position, 3)

        pygame.draw.circle(screen, (100, 100, 100), self.PivotPos, 6)
        pygame.draw.circle(screen, (255, 0, 0), self.position, 6)

    def update(self):
        distance = self.position - self.PivotPos
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

    def handle_event(self, event): #not sure for now
        pass