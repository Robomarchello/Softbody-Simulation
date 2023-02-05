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
                distanceVec = self.position - point.position
                normalDist = distanceVec.normalize()
                distance = distanceVec.length() - self.radius

                if distance < 0:
                    #calculating separating force
                    SepForce = normalDist.elementwise() * -(distance * 1.0)
                    point.acceleration -= SepForce
                    #not sure if this is the best solution, but works fine
                    point.position = self.position - normalDist * self.radius