import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
from polygon import PolygonJson


pygame.init()

class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.poly = PolygonJson('src/assets/polygon1.json') 
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            position = Mouse.position

            self.poly.draw(screen)
            pygame.draw.circle(screen, (255, 0, 0), position, 3)

            if self.poly.collide_point(position):
                closest = []
                distances = []
                for edge in self.poly.edges:
                    edgeClosest = self.poly.getClosest(position, edge)
                    closest.append(edgeClosest)
                    distances.append((edgeClosest[0] - position).magnitude())

                distanceMin = min(distances)
                index = distances.index(distanceMin)
                pygame.draw.circle(screen, (255, 0, 0), closest[index][0], 3)

                # Move points here later

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((1280, 720), 'Intersection', 60).loop()