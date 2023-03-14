import pygame
from pygame._sdl2 import Renderer, Texture, Window
from pygame.locals import *
from mouse import Mouse

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize 
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)
        self.window = Window.from_display_module()
        self.renderer = Renderer(self.window)

        image = pygame.image.load('src/assets/texture1.png').convert_alpha()
        self.texture = Texture.from_surface(self.renderer, image)

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        renderer = self.renderer
        while True:
            self.clock.tick(self.fps)

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.texture.draw_triangle((300, 300), Mouse.position, (300, 500),
                                       (0.0, 1.0), (0.5, 0.0), (1.0, 1.0))
            renderer.present()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                Mouse.handle_event(event)

            pygame.display.set_caption(str(round(self.clock.get_fps())))


App((1280, 720), 'Texturing', 0).loop()