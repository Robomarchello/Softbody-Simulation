import pygame
from pygame.locals import *
from src.scripts import *

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        gas_amount = 1500.0
        mass = 5
        stiffness = 1.0
        damping = 0.96

        #-- polygon --
        self.polygons = [PolygonJson('src/assets/polygon.json')]

        self.softbody = SoftbodyBall(self.ScreenSize, (150, 50), 30, 16,
                                    mass, stiffness, damping, gas_amount,
                                    self.polygons.copy())

        self.softbody1 = SoftbodyBall(self.ScreenSize, (1100, 400), 30, 16,
                                    mass, stiffness, damping, gas_amount,
                                    self.polygons.copy())
        self.softbody2 = SoftbodyBall(self.ScreenSize, (700, 400), 30, 16,
                                    mass, stiffness, damping, gas_amount,
                                    self.polygons.copy())

        #i know,
        self.softbody.obstacles.append(self.softbody1.polygon)
        self.softbody.obstacles.append(self.softbody2.polygon)
        self.softbody1.obstacles.append(self.softbody.polygon)
        self.softbody1.obstacles.append(self.softbody2.polygon)
        self.softbody2.obstacles.append(self.softbody.polygon)
        self.softbody2.obstacles.append(self.softbody1.polygon)

        self.HardBall = HardBall(100, [self.softbody, self.softbody1, self.softbody2])
        self.Settinger = Settinger(self.softbody)

        self.event_handlers = [Mouse, Debug, self.Settinger]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            self.Settinger.draw()
            screen.fill((255, 255, 255))

            #collision = self.Polygon.collisionResolve(Mouse.position)
            #if collision != False:
            #    screen.fill((255, 0, 0))

            for polygon in self.polygons:
                polygon.draw(screen)
            #pygame.draw.line(screen, (0, 0, 0), (0, Mouse.position.y), Mouse.position)

            self.HardBall.update()
            self.softbody.draw(screen)
            self.softbody1.draw(screen)
            self.softbody2.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Debug.draw(screen)
            self.HardBall.draw(screen)
        
            pygame.display.update()