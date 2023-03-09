import pygame
from pygame.locals import *
from mouse import Mouse
import numpy
#from numpy import subtract, take, array

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize 
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.texture = pygame.image.load('src/assets/texture.png').convert()

        self.textureTri = [[0, 80], [80, 0], [160, 80]]
        self.mappedTri = [[300, 170], [330, 50], [410, 130]]

        xPoses = numpy.take(self.mappedTri, 0, axis=1)
        yPoses = numpy.take(self.mappedTri, 1, axis=1)
        self.textureRect = pygame.Rect(
            min(xPoses), min(yPoses), 
            max(xPoses) - min(xPoses), max(yPoses) - min(yPoses)
            )

        self.output = self.TextureMap()

        self.clock = pygame.time.Clock()
        self.fps = fps

    def TextureMap(self):
        pixels = pygame.surfarray.array2d(self.texture)

        xInterps = numpy.linspace(0.0, 1.0, self.textureRect.width)
        yInterps = numpy.linspace(0.0, 1.0, self.textureRect.height)
    
        sideL = numpy.subtract(self.textureTri[0], self.textureTri[1])
        sideR = numpy.subtract(self.textureTri[2], self.textureTri[1])

        yPair = numpy.repeat(yInterps, 2).reshape(yInterps.shape[0], 2)
        sideLinterp = sideL * yPair + self.textureTri[1]
        sideRinterp = sideR * yPair + self.textureTri[1]

        segBetween = numpy.subtract(sideRinterp, sideLinterp)
        allSegments = numpy.repeat(segBetween, xInterps.shape[0], axis=0)
        tileX = numpy.tile(xInterps, segBetween.shape[0])
        tileXPair = numpy.repeat(tileX, 2).reshape(tileX.shape[0], 2)
        
        sideLAll = numpy.repeat(sideLinterp, xInterps.shape[0], axis=0)

        TextureShape = (self.textureRect.height, self.textureRect.width)

        positions = numpy.int_(numpy.multiply(allSegments, tileXPair) + sideLAll)
        xPoses = numpy.take(positions, 0, axis=1) - 1
        yPoses = numpy.take(positions, 1, axis=1) - 1
        newPixels = numpy.array(pixels)[xPoses, yPoses]
        newPixels = newPixels.reshape(TextureShape)
        
        return pygame.surfarray.make_surface(newPixels)


    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            screen.blit(self.texture, (0, 0))

            pygame.draw.polygon(screen, (255, 0, 0), self.textureTri, 2)
            pygame.draw.polygon(screen, (255, 0, 0), self.mappedTri, 2)

            pygame.draw.rect(screen, (255, 0, 0), self.textureRect, 2)

            if self.output != None:
                screen.blit(self.output, (0, 160))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((1280, 720), 'Texturing', 60).loop()