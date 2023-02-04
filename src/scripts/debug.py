import pygame

pygame.init()


class Debug:
    draw_queue = []
    font = pygame.font.Font('src/assets/font.ttf', 16)
    display = True

    @classmethod
    def line(cls, startPos, endPos, color=(0, 0, 0)):
        cls.draw_queue.append(['line', startPos, endPos, color])

    @classmethod
    def vector(cls, point, vector: pygame.Vector2, color=(0, 0, 0)):
        cls.draw_queue.append(['vector', point, point + vector, color])

    @classmethod
    def circle(cls, center, radius, width, color=(0, 0, 0)):
        cls.draw_queue.append(['circle', center, radius, width, color])

    @classmethod
    def point(cls, position, color=(0, 0, 0)):
        cls.draw_queue.append(['point', position, 3, 0, color])

    @classmethod
    def text(cls, position, text, color=(0, 0, 0)):
        cls.draw_queue.append(['text', text, position, color])
    
    @classmethod
    def draw(cls, screen):
        if not cls.display:
            cls.draw_queue = []

        for object in cls.draw_queue:
            if object[0] == 'line' or object[0] == 'vector':
                pygame.draw.line(screen, object[3], object[1], object[2], 3)
            
            if object[0] == 'circle' or object[0] == 'point':
                pygame.draw.circle(screen, object[4], object[1], object[2], object[3])

            if object[0] == 'text':
                render = cls.font.render(object[1], False, object[3])
                screen.blit(render, object[2])

        cls.draw_queue = []

    @classmethod
    def handle_event(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if cls.display:
                    cls.display = False
                else:
                    cls.display = True