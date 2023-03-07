import pygame
from pygame.locals import *
from src.scripts import *

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.SoftbodyHandler = SoftbodyHandler(self.ScreenSize)
        self.polygons = self.SoftbodyHandler.polygons

        self.HardBall = HardBall(75, self.SoftbodyHandler.softbodies)
        self.Settinger = Settinger(self.SoftbodyHandler.softbodies[0])

        self.event_handlers = [Mouse, Debug, self.Settinger]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            self.Settinger.draw()
            screen.fill((255, 255, 255))

            for polygon in self.polygons:
                polygon.draw(screen)

            self.HardBall.update()
            self.SoftbodyHandler.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Debug.draw(screen)
            self.HardBall.draw(screen)
        
            pygame.display.update()