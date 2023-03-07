import pygame
from pygame.locals import *
from mouse import Mouse
import numpy

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize 
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.texture = pygame.image.load('src/assets/texture.png').convert()

        self.textureTri = [[0, 80], [80, 0], [160, 80]]
        self.mappedTri = [[300, 170], [330, 50], [410, 130]]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def TextureMap(self):
        pixels = pygame.PixelArray(self.texture)
    
        side1 = numpy.subtract(self.textureTri[0], self.textureTri[1])
        side2 = numpy.subtract(self.textureTri[2], self.textureTri[1])


    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            screen.blit(self.texture, (0, 0))

            pygame.draw.polygon(screen, (255, 0, 0), self.textureTri, 2)
            pygame.draw.polygon(screen, (255, 0, 0), self.mappedTri, 2)

            self.TextureMap()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((1280, 720), 'Texturing', 60).loop()