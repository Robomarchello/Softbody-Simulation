import pygame
from pygame import Vector2

#could be also named obstacle.py
#also, thats for static objects, we could also want collision between two softbodies
class Polygon:
    def __init__(self, points):
        self.points = points
        self.edges = [] #[point1, point2], ...

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.points, 3)

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
                break

            #DO THE CHECK IF LINE INTERSECTS Y POSITION
            if not (min(EdgeY) < Checkline[0].y and
                    max(EdgeY) > Checkline[0].y):
                break

                #check if lines are parallel
            if EdgeVec.y == 0:
                break
            
            HeightBtwn = Checkline[0].y - edgeLine[0].y

            #check if line y direction has the same sign(+/-) height difference 
            if not (HeightBtwn > 0 and EdgeVec.y > 0) and not (
                HeightBtwn < 0 and EdgeVec.y < 0):
                
                break
                
            position = EdgeVec * HeightBtwn / EdgeVec.y
            position += edgeLine[0]

            if position.x > Checkline[0].x and position.x < Checkline[1].x:
                intersections.append(position)
        
    def collide_polygon(self, polygon):
        #run collide_point for every point of the other polygon
        pass

#class PolygonJson
#reads polygon data from json

#

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