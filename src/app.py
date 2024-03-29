import pygame
from pygame._sdl2 import Renderer, Texture, Window
from pygame.locals import *
from src.scripts import *

pygame.init()


class App():
    def __init__(self, ScreenSize, caption, fps):
        self.ScreenSize = ScreenSize
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption(caption)
        self.window = Window.from_display_module()
        self.renderer = Renderer(self.window)

        self.SoftbodyHandler = SoftbodyHandler(self.ScreenSize, self.renderer)
        self.polygons = self.SoftbodyHandler.polygons

        HardBallTexture = Texture.from_surface(
            self.renderer,
            pygame.image.load('src/assets/hardBall.png').convert_alpha()
        )
        self.HardBall = HardBall(75, self.SoftbodyHandler.softbodies, HardBallTexture)
        self.Settinger = Settinger(self.SoftbodyHandler.softbodies[0])

        self.event_handlers = [Mouse, Debug, self.Settinger]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def loop(self):
        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

            self.HardBall.update()

            self.draw()

            pygame.display.set_caption(str(round(self.clock.get_fps())))

    def draw(self):
        #draw with textures
        renderer = self.renderer
        screen = self.screen

        renderer.draw_color = (255, 255, 255, 255)
        renderer.clear()

        self.Settinger.draw()

        for polygon in self.polygons:
            polygon.draw_sdl2(renderer)

        self.SoftbodyHandler.draw(screen)
        self.HardBall.draw_sdl2()
        
        renderer.present()

    def draw_debug(self):
        screen = self.screen

        screen.fill((255, 255, 255))

        for polygon in self.polygons:
            polygon.draw(screen)

        self.HardBall.draw(screen)

        self.SoftbodyHandler.draw(screen)

        Debug.draw(screen)
        pygame.display.update()