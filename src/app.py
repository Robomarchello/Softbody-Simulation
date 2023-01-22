import pygame
from pygame.locals import *
from src.scripts.spring import SoftbodySquare, SoftbodyBall
from src.scripts.mouse import Mouse

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        rect = pygame.Rect(540, 200, 300, 300)
        self.softbody = SoftbodyBall(self.ScreenSize, (640, 300), 50, 8)

        self.event_handlers = [
            Mouse, self.softbody
        ]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            self.softbody.draw(screen)
            #self.spring.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)
            
            pygame.display.update()