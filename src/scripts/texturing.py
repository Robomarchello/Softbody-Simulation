import pygame
import numpy
#import pygame._sdl2.video #don't think this required


class TextureMapper:
    def __init__(self, texture, textureTris, mappedTris):
        #Tris means triangles
        self.texture = texture
        self.pixels = pygame.surfarray.array2d(self.texture)

        self.textureTris = textureTris
        self.mappedTris = mappedTris

    def draw(self, screen):
        for index, txtrTri in enumerate(self.textureTris):
            mappedTri = self.mappedTris[index]

            textured = self.textureTri(txtrTri, mappedTri)
            screen.blit(textured[0], textured[1])
            
    def updateMapped(self, mappedTris):
        self.mappedTris = mappedTris

    def textureTri(self, textureTri, mappedTri):
        xPses = numpy.take(mappedTri, 0, axis=1)
        yPses = numpy.take(mappedTri, 1, axis=1)
        textureRect = pygame.Rect(
            min(xPses), min(yPses), 
            max(xPses) - min(xPses), max(yPses) - min(yPses)
            )

        MappedPixels = numpy.zeros(textureRect.size, int)
        pixels = self.pixels 

        xInterps = numpy.linspace(0.0, 1.0, textureRect.width)
        yInterps = numpy.linspace(0.0, 1.0, textureRect.height)
    
        sideL = numpy.subtract(textureTri[0], textureTri[1])
        sideR = numpy.subtract(textureTri[2], textureTri[1])

        yPair = numpy.repeat(yInterps, 2).reshape(yInterps.shape[0], 2)
        sideLinterp = sideL * yPair + textureTri[1]
        sideRinterp = sideR * yPair + textureTri[1]

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