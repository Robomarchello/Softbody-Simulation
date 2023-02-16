import pygame
from pygame import Vector2
from json import loads


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
        '''
        My solution to get intersection between horizontal line and any line
        not cleanest one, but works
        '''
        #return intersection point + force normal to edge of the collision
        Checkline = [Vector2(0, point.y), Vector2(point.x, point.y)]  

        intersections = []
        for edgeLine in self.edges:
            EdgeVec = (edgeLine[1] - edgeLine[0]).normalize()
            EdgeY = [vec.y for vec in edgeLine]

            #0 length check
            if edgeLine[0].xy == edgeLine[1].xy:
                continue
            
            #Check if line segment positions intersect in y
            if not (min(EdgeY) < Checkline[0].y and
                    max(EdgeY) > Checkline[0].y):
                continue

            #check if lines are parallel
            if EdgeVec.y == 0:
                continue
            
            HeightBtwn = Checkline[0].y - edgeLine[0].y

            #check if line y direction has the same sign(+/-) height difference 
            if not (HeightBtwn > 0 and EdgeVec.y > 0) and not (
                HeightBtwn < 0 and EdgeVec.y < 0):
                continue
                
            position = EdgeVec * HeightBtwn / EdgeVec.y
            position += edgeLine[0]

            if position.x > Checkline[0].x and position.x < Checkline[1].x:
                intersections.append(position)

        print(len(intersections))

        if (len(intersections) % 2) == 1:
            return True

            #true/false
            #or return intersection points
            #or return closest intersection and edge
        
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

#class PolyRect
#size, center, angle?

'''
def getIntersection():
    \'''
    My solution to get intersection between horizontal line and any line
    not cleanest one, but works
    \'''
    self.TargetLine[1] = Mouse.position
    TargetVec = (self.TargetLine[1] - self.TargetLine[0]).normalize()
    TargetY = [vec.y for vec in self.TargetLine]

    #0 length check
    if self.TargetLine[0] == self.TargetLine[1].xy:
        return None

    #DO THE CHECK IF LINE INTERSECTS Y POSITION
    if not (min(TargetY) < self.Checkline[0].y and
            max(TargetY) > self.Checkline[0].y):
        return None

        #check if lines are parallel
    if TargetVec.y == 0:
        return None
    
    HeightBtwn = self.Checkline[0].y - self.TargetLine[0].y

    #check if line y direction has the same sign(+/-) height difference 
    if not (HeightBtwn > 0 and TargetVec.y > 0) and not (
        HeightBtwn < 0 and TargetVec.y < 0):
        
        return None
        
    position = TargetVec * HeightBtwn / TargetVec.y
    position += self.TargetLine[0]

    if position.x > self.Checkline[0].x and position.x < self.Checkline[1].x:
        return position
    else:
        return None
'''