import pygame
from pygame.locals import *
from src.scripts import *

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        gas_amount = 2500.0
        mass = 5
        stiffness = 1.0
        damping = 0.96

        self.softbody = SoftbodyBall(self.ScreenSize, (640, 300), 75, 16,
                                    mass, stiffness, damping, gas_amount)

        self.HardBall = HardBall(100, [self.softbody])
        self.Settinger = Settinger(self.softbody)

        #-- polygon --
        indices = [[0, 1], [1, 2], [2, 3], [3, 0]]
        self.Polygon = PolygonJson('src/assets/polygon.json')

        self.event_handlers = [Mouse, Debug]#, self.Settinger]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            #self.Settinger.draw()
            screen.fill((255, 255, 255))

            if self.Polygon.collide_point(Mouse.position):
                screen.fill((255, 0, 0))
            self.Polygon.draw(screen)
            pygame.draw.line(screen, (0, 0, 0), (0, Mouse.position.y), Mouse.position)

            #self.HardBall.update()
            #self.softbody.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Debug.draw(screen)
            #self.HardBall.draw(screen)

            pygame.display.update()