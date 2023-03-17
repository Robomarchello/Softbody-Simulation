import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
from polygon import PolygonJson
from copy import copy

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

            #if going to be used not only for softbodies, then add polygon.static
            #and if it's static, then resolve only softbody.
            #also add rect collision chech back
            if self.poly.collide_point(position):
                closest = []
                distances = []
                for edge in self.poly.edges:
                    edgeClosest = self.poly.getClosest(position, edge)
                    closest.append(edgeClosest)
                    distances.append((edgeClosest[0] - position).magnitude())

                distance = min(distances)
                index = distances.index(distance)
                edge = self.poly.edges[index]

                interp = (closest[index][0].x - edge[0].x) / (edge[1].x - edge[0].x)
                
                normal = Vector2(closest[index][1].y, -closest[index][1].x)
                #if not polygon.static:
                newEdge = [
                    edge[0] - normal * distance * interp,
                    edge[1] - normal * distance * (1 - interp)
                ]
                newVec = newEdge[1] - newEdge[0]

                pointNew = newVec * interp + newEdge[0]
                #---

                pygame.draw.line(screen, (150, 150, 150), newEdge[0], newEdge[1])
                pygame.draw.circle(screen, (0, 255, 0), pointNew, 2)

                #find velocities here
                #Use some better way (later💋)
                pointVel = normal
                #if not polygon.static:
                edgeVel = -normal

                #return [pointVel, edgeVel]


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.update()


App((1280, 720), 'Intersection', 60).loop()