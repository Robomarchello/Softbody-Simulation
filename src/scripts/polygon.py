import pygame
from pygame import Vector2
from json import loads
from .debug import Debug


class Polygon:
    def __init__(self, points, indices):
        self.points = points
        self.points = [Vector2(point) for point in self.points]
        
        self.indices = indices
        self.edges = []
        for index in indices:
            edge = [self.points[index[0]], self.points[index[1]]]
            
            self.edges.append(edge)

        self.rect = self.get_rect()

        self.static = True
    
    def update(self, points):
        '''
        update the polygon points, rect...
        used for softbody - softbody collision
        '''
        self.points = points
        self.points = [Vector2(point) for point in self.points]

        self.edges = []
        for index in self.indices:
            edge = [self.points[index[0]], self.points[index[1]]]
            
            self.edges.append(edge)

        self.rect = self.get_rect()

    def indicesToEdges(self, indices):
        '''updating edges'''
        edges = []

        for index in indices:
            edge = [self.points[index[0]], self.points[index[1]]]
            
            edges.append(edge)

        return edges

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.points, 1)

    def get_rect(self):
        xPoses = [point.x for point in self.points]
        yPoses = [point.y for point in self.points]

        topleft = [min(xPoses), min(yPoses)] #min poses
        size = [max(xPoses) - topleft[0], max(yPoses) - topleft[1]]

        return pygame.Rect(topleft, size)
    
    def collide_point(self, point):
        '''point - polygon collision check'''
        Checkline = [Vector2(self.rect.left, point.y), Vector2(point.x, point.y)]  
        
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
            #self.collisionResolve(point)
            return True
        
        return False 
    
    '''def collisionResolve(self, point):
        #additional collision step for performance
        collideRect = self.rect.collidepoint(point)

        if collideRect and self.collide_point(point):
            points = []
            normal = []
            distances = []
            for edge in self.edges:
                edgeClosest = self.getClosest(point, edge)
                
                points.append(edgeClosest[0])
                normal.append(edgeClosest[1])
                distances.append((edgeClosest[0] - point).magnitude())
                
                Debug.circle(edgeClosest[0], 3, 0, (0, 255, 0))

            edgeIndex = distances.index(min(distances))
            closestPoint = points[edgeIndex]
            normalVec = normal[edgeIndex]

            return [edgeIndex, closestPoint, normalVec]

        #no collision
        return False'''

    def CollisionResolve(self, point):
        '''return closest point and normal vec'''
        #additional collision step for performance
        collideRect = self.rect.collidepoint(point)

        if collideRect and self.collide_point(point):
            points = []
            normals = []
            distances = []
            for edge in self.edges:
                edgeClosest = self.getClosest(point, edge)
                points.append(edgeClosest[0])
                normals.append(edgeClosest[1])
                distances.append((edgeClosest[0] - point).magnitude())

            distance = min(distances)
            index = distances.index(distance)
            edge = self.edges[index]

            if self.static:
                edgeIndex = distances.index(min(distances))
                closestPoint = points[edgeIndex]
                normalVec = normal[edgeIndex]

                #apply here???
                return [edgeIndex, closestPoint, normalVec, None]

            interp = (points[index].x - edge[0].x) / (edge[1].x - edge[0].x)
                
            normal = Vector2(normals[index].y, -normals[index].x)
            #if not polygon.static:
            newEdge = [
                edge[0] - normal * distance * interp,
                edge[1] - normal * distance * (1 - interp)
            ]
            newVec = newEdge[1] - newEdge[0]

            pointNew = newVec * interp + newEdge[0]
            #---

            pointVel = normal
            #if not polygon.static:
            edgeVel = -normal
            #apply here???
            return [edgeIndex, pointNew, pointVel, edgeVel]

        return False
        
    def getClosest(self, position, edge):
          #Hope you get this
        '''Returns the closest point on a line segment from point'''
        TargetPointPos = position - edge[0] 

        EdgeVec = (edge[1] - edge[0])
        VecNormal = EdgeVec.normalize()
        normal = Vector2(VecNormal.y, -VecNormal.x)            

        distanceX = (EdgeVec - TargetPointPos).x * VecNormal.y
        distanceY = -(EdgeVec - TargetPointPos).y * VecNormal.x

        ClosestPos = normal * (distanceX + distanceY)
        ClosestPos += position

        #not that important - check if point is on the line
        minPos = [min((edge[0].x, edge[1].x)), min((edge[0].y, edge[1].y))]
        maxPos = [max((edge[0].x, edge[1].x)), max((edge[0].y, edge[1].y))]

        if ClosestPos.x < minPos[0]:
            ClosestPos.x = minPos[0]

        elif ClosestPos.x > maxPos[0]:
            ClosestPos.x = maxPos[0]

        if ClosestPos.y < minPos[1]:
            ClosestPos.y = minPos[1]

        elif ClosestPos.y > maxPos[1]:
            ClosestPos.y = maxPos[1]

        return [ClosestPos, VecNormal]

    def collide_polygon(self, polygon):
        '''
        for every point in other polygon class collide_point
        return colliding points 
        Could be used for softbodies collision later
        '''
        
        collisions = []

        for point in polygon.points:
            collision = self.collisionResolve(point)
            
            if collision != False:
                collisions.append(collision)

        return collisions

class PolygonJson(Polygon):
    def __init__(self, file):
        with open(file, 'r') as polyFile:
            data = loads(polyFile.read())

            points = data['points']
            edges = data['edges']

        super().__init__(points, edges)
