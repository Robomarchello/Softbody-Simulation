import pygame
from pygame import Vector2
from pygame.locals import *
from mouse import Mouse
from json import dump

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)

        self.radius = 10

        self.points = []
        self.connections = []

        self.holding = None

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        print(
        ''' 
        Be careful placing and connecting points,
        polygon shouldn't be self-intersecting,
        double connection innt't handeled, those will break the collision
        ''')

        screen = self.screen
        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                Mouse.handle_event(event)
                self.editing(event)

            screen.fill((255, 255, 255))

            for point in self.points:
                pygame.draw.circle(screen, (0, 0, 0), point, self.radius)

            for connection in self.connections:
                point1 = self.points[connection[0]]
                point2 = self.points[connection[1]]
                
                pygame.draw.line(screen, (50, 50, 50), point1, point2)
            if self.holding != None:
                pygame.draw.circle(screen, (255, 0, 0), self.holding, self.radius)
            
            pygame.display.update()

    def editing(self, event):
        if event.type == KEYDOWN:
            if event.key == K_s:
                #so it's not pygame.Vector2
                if len(self.points) <= 2:
                    print('You need atleast 3 points')
                if len(self.connections) <= 2:
                    print('You need atleast three connections')
                
                else:
                    points = [[point.x, point.y] for point in self.points]
                    data = {
                        'points': points,
                        'edges': self.connections
                    }
                    with open('output.json', 'w') as file: 
                        dump(data, file)
                        print('file saved')

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pressed = False
                for point in self.points:
                    vecDiff = Mouse.position - point

                    distance = vecDiff.length()
                    if distance < self.radius: 
                        pressed = True

                        if self.holding != None:
                            if self.holding == point:
                                break
                            
                            self.connections.append([
                                self.points.index(self.holding),
                                self.points.index(point)
                                ])
                                                    
                        self.holding = point
                        
                        break
                
                if not pressed:
                    self.holding = None

                if self.holding == None:
                    self.points.append(Mouse.position.copy())

            if event.button == 3:
                self.holding = None
                for point in self.points:
                    vecDiff = Mouse.position - point

                    distance = vecDiff.length()

                    if distance < self.radius:
                        self.points.remove(point)



App((1280, 720), 'PolyEditor', 0).loop()