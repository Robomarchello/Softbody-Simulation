import pygame
from pygame import Vector2
from json import loads
from .debug import Debug


#could be also named obstacle.py
#also, thats for static objects, could also want collision between two softbodies
class Polygon:
    def __init__(self, points, indices):
        self.points = points
        self.points = [Vector2(point) for point in self.points]

        self.edges = []
        for index in indices:
            edge = [self.points[index[0]], self.points[index[1]]]
            
            self.edges.append(edge)
    
    def indicesToEdges(self, indices):
        edges = []

        for index in indices:
            edge = [self.points[index[0]], self.points[index[1]]]
            
            edges.append(edge)

        return edges

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.points, 1)

        #or draw
        #points as circles
        #edges as lines

    def get_rect(self):
        topleft = [0, 0] #min poses
        size = [0, 0] #max poses - min poses

        return pygame.Rect(topleft[0], topleft[1], size[0], size[1])
    
    def collide_point(self, point):
        Checkline = [Vector2(0, point.y), Vector2(point.x, point.y)]  
        
        intersections = []
        for edgeLine in self.edges:
            EdgeVec = (edgeLine[1] - edgeLine[0]).normalize()

            #check if lines are parallel
            if edgeLine[0].y == edgeLine[1].y:
                continue

            #0 length check
            if EdgeVec.y == 0:
                continue
            
            HeightBtwn = Checkline[0].y - edgeLine[0].y
                
            position = EdgeVec * HeightBtwn / EdgeVec.y
            position += edgeLine[0]

            interp = (position[1] - edgeLine[0].y) / (edgeLine[1].y - edgeLine[0].y)
            if round(interp, 4) > 1 or round(interp, 4) < 0:
                continue

            if position.x >= Checkline[0].x and position.x <= Checkline[1].x:
                intersections.append(position)
                Debug.circle(position, 2, 0)


        Debug.text((5, 5), str(len(intersections)))

        result = []
        for intersection in intersections:
            if intersection in result:
                result = []
                break
            else:
                result.append(intersection)

        if (len(result) % 2) == 1:
            return True
        
        return False 

    def collide_polygon(self, polygon):
        #run collide_point for every point of the other polygon
        pass


class PolygonJson(Polygon):
    def __init__(self, file):
        with open(file, 'r') as polyFile:
            data = loads(polyFile.read())

            self.points = data['points']
            self.edges = data['edges']

        super().__init__(self.points, self.edges)