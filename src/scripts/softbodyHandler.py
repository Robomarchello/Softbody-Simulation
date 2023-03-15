from .softbody import SoftbodyBall
from .polygon import PolygonJson
import pygame


class SoftbodyHandler:
    def __init__(self, ScreenSize, renderer):
        self.ScreenSize = ScreenSize
        gas_amount = 1500.0
        mass = 5
        stiffness = 1.0
        damping = 0.96

        self.polygons = [PolygonJson('src/assets/polygon.json')]

        texture = pygame.image.load('src/assets/texture2.png').convert_alpha()
        texture1 = pygame.image.load('src/assets/texture.png').convert_alpha()
        self.softbodies = []

        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (150, 50), 30, 16,
            mass, stiffness, damping, gas_amount,
            renderer, self.polygons.copy(), texture
            )
        )

        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (1100, 400), 30, 16,
            mass, stiffness, damping, gas_amount,
            renderer, self.polygons.copy(), texture1
            )
        )

        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (700, 400), 30, 16,
            mass, stiffness, damping, gas_amount,
            renderer, self.polygons.copy(), texture
            )
        )

        softPolygons = [softbody.polygon for softbody in self.softbodies]
        for index, softbody in enumerate(self.softbodies):
            otherPolygons = softPolygons.copy()
            otherPolygons.pop(index)
            softbody.obstacles = softbody.obstacles + otherPolygons

    def draw(self, screen):
        for softbody in self.softbodies:
            softbody.draw(screen)