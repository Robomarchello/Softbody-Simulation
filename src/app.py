import pygame
from pygame.locals import *
from src.scripts.softbody import SoftbodyBall
from src.scripts.mouse import Mouse
from src.scripts.debug import Debug
from src.scripts.interaction import HardBall, Settinger

pygame.init()

#cool settings
#gas, mass, stiffness, damping, radius, points
#2500.0, 5, 1.0, 0.96, 75, 16
#3500, 2.5, 1.0, 0.96, 50, 32
#3000, 4.0, 1.1. 0.97, 75, 16

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

        self.event_handlers = [Mouse, Debug, self.Settinger]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            self.Settinger.draw()
            screen.fill((255, 255, 255))
            
            self.HardBall.update()
            self.softbody.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Debug.draw(screen)
            self.HardBall.draw(screen)

            pygame.display.update()