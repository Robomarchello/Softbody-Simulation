from .softbody import SoftbodyBall
from .polygon import PolygonJson


class SoftbodyHandler:
    def __init__(self, ScreenSize):
        self.ScreenSize = ScreenSize
        gas_amount = 1500.0
        mass = 5
        stiffness = 1.0
        damping = 0.96

        self.polygons = [PolygonJson('src/assets/polygon.json')]

        self.softbodies = []
        
        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (150, 50), 30, 16,
            mass, stiffness, damping, gas_amount, 
            self.polygons.copy()
            )
        )

        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (1100, 400), 30, 16,
            mass, stiffness, damping, gas_amount,
            self.polygons.copy()
            )
        )

        self.softbodies.append(
            SoftbodyBall(
            self.ScreenSize, (700, 400), 30, 16,
            mass, stiffness, damping, gas_amount,
            self.polygons.copy()
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