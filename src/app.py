import pygame
from pygame.locals import *
from src.scripts.spring import Spring

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.spring = Spring(
            pygame.Vector2(640, 100), pygame.Vector2(840, 350), 5, 0.1, 350)

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            self.spring.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
            
            pygame.display.update()