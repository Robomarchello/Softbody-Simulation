import pygame
from pygame.locals import *
from src.scripts.softbody import SoftbodyBall
from src.scripts.mouse import Mouse
from src.scripts.debug import Debug

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        gas_amount = 5000.0
        mass = 10
        stiffness = 1.0
        damping = 0.92

        self.softbody = SoftbodyBall(self.ScreenSize, (640, 300), 150, 8,
                                    mass, stiffness, damping, gas_amount)

        self.event_handlers = [Mouse]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            self.softbody.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            Debug.draw(screen)

            pygame.display.update()