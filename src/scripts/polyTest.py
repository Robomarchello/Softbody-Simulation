import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
from polygon import PolygonJson


pygame.init()

class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.poly1 = PolygonJson('src/assets/polygon.json') 
        self.poly2 = PolygonJson('src/assets/polygon1.json') 
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.previous = self.poly1.points[1]
        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            screen.fill((255, 255, 255))

            self.poly1.draw(screen)
            self.poly2.draw(screen)

            movement = Mouse.position  - self.previous
            points = []  
            for point in self.poly1.points:
                points.append(point + movement)
            self.previous = Mouse.position.copy()

            self.poly1.update(points)

            collision1 = self.poly1.collide_polygon(self.poly2)
            collision2 = self.poly2.collide_polygon(self.poly1)
            
            if collision1 != []:
                print(collision1)

            if collision2 != []:
                print(collision2)

            #if collision2 != []:
            #    print(collision2)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((1280, 720), 'Intersection', 60).loop()