import pygame

pygame.init()

class Debug():
    def __init__(self, font=None):
        self.draw_queue = []

        if not font == None:
            self.font = pygame.font.Font(font, 15)

    def line(self, startPosition, endPosition, color=(0, 0, 0)):
        self.draw_queue.append(['line', startPosition, endPosition, color])

    def vector(self, point, vector: pygame.Vector2, color=(0, 0, 0)):
        self.draw_queue.append(['vector', point, point + vector, color])

    def circle(self, center, radius, width, color=(0, 0, 0)):
        self.draw_queue.append(['circle', center, radius, width, color])

    def point(self, position, color=(0, 0, 0)):
        self.draw_queue.append(['point', position, 3, 0, color])

    def text(self, position, text, color=(0, 0, 0)):
        self.draw_queue.append(['text', text, position, color])

    def draw(self, screen):
        for object in self.draw_queue:
            if object[0] == 'line' or object[0] == 'vector':
                pygame.draw.line(screen, object[3], object[1], object[2])
            
            if object[0] == 'circle' or object[0] == 'point':
                pygame.draw.circle(screen, object[4], object[1], object[2], object[3])

            if object[0] == 'text':
                render = self.font.render(object[1], False, object[3])
                screen.blit(render, object[2])


        self.draw_queue = []