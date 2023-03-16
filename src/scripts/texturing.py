import pygame
import numpy
from pygame._sdl2 import Texture


class TextureMapper:
    def __init__(self, renderer, texture, UVTris, mappedTris):
        #Tris means triangles
        self.texture = Texture.from_surface(renderer, texture)
        self.pixels = pygame.surfarray.array2d(texture)

        self.renderer = renderer

        self.UVTris = UVTris
        self.mappedTris = mappedTris

    def draw_sdl2(self):
        for index, uvTri in enumerate(self.UVTris):
            mappedTri = self.mappedTris[index]

            self.texture.draw_triangle(
                mappedTri[0], mappedTri[1], mappedTri[2],
                uvTri[0], uvTri[1], uvTri[2]
            )
            
    def updateMapped(self, mappedTris):
        self.mappedTris = mappedTris

    def updateUV(self, UVTris):
        self.UVTris = UVTris
        


    # ----
    def textureTri(self, UVTri, mappedTri):
        xPoses = numpy.take(mappedTri, 0, axis=1)
        yPoses = numpy.take(mappedTri, 1, axis=1)
        textureRect = pygame.Rect(
            min(xPoses), min(yPoses), 
            max(xPoses) - min(xPoses), max(yPoses) - min(yPoses)
            )

        MappedPixels = numpy.zeros(textureRect.size, int)
        pixels = self.pixels 

        xInterps = numpy.linspace(0.0, 1.0, textureRect.width)
        yInterps = numpy.linspace(0.0, 1.0, textureRect.height)
    
        sideL = numpy.subtract(UVTri[0], UVTri[1])
        sideR = numpy.subtract(UVTri[2], UVTri[1])

        yPair = numpy.repeat(yInterps, 2).reshape(yInterps.shape[0], 2)
        sideLinterp = sideL * yPair + UVTri[1]
        sideRinterp = sideR * yPair + UVTri[1]

        segBetween = numpy.subtract(sideRinterp, sideLinterp)
        
        sideLAll = numpy.repeat(sideLinterp, xInterps.shape[0], axis=0)
        positions = numpy.kron(xInterps, segBetween).reshape(sideLAll.shape) + sideLAll
        positions = numpy.int_(positions)

        xPoses = numpy.take(positions, 0, axis=1) - 1
        yPoses = numpy.take(positions, 1, axis=1) - 1
        newPixels = numpy.array(pixels)[xPoses, yPoses]

        #  ---- 
        sideL = numpy.subtract(mappedTri[0], mappedTri[1])
        sideR = numpy.subtract(mappedTri[2], mappedTri[1])

        yPair = numpy.repeat(yInterps, 2).reshape(yInterps.shape[0], 2)
        sideLinterp = sideL * yPair + mappedTri[1] - textureRect.topleft
        sideRinterp = sideR * yPair + mappedTri[1] - textureRect.topleft

        segBetween = numpy.subtract(sideRinterp, sideLinterp)

        sideLAll = numpy.repeat(sideLinterp, xInterps.shape[0], axis=0)

        positions = numpy.kron(xInterps, segBetween).reshape(sideLAll.shape) + sideLAll
        positions = numpy.int_(positions)

        xPoses = numpy.take(positions, 0, axis=1) - 2
        yPoses = numpy.take(positions, 1, axis=1) - 2
        MappedPixels[xPoses, yPoses] = newPixels

        surf = pygame.Surface(textureRect.size)
        surf.set_colorkey((0, 0, 0))
        pygame.surfarray.blit_array(surf, MappedPixels)
        
        return [surf, textureRect.topleft]