import pygame
from .mouse import Mouse


#not separate simulation, but for interaction with softbodies
class HardBall:
    def __init__(self, radius, softbodies):
        self.position = Mouse.position
        self.radius = radius
        self.softbodies = softbodies

    def draw(self, screen):
        pygame.draw.circle(screen, (115, 115, 115), self.position, self.radius)

    def update(self):
        for softbody in self.softbodies:
            for point in softbody.points:
                distance = self.position - point.position

                if distance.length() - self.radius < 0:
                    #calculating separating force
                    point.acceleration -= distance * 0.05
                    #not sure if this is the best solution, but works fine
                    point.position = self.position - distance.normalize() * self.radius
