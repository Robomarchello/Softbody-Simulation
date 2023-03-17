import pygame
from .mouse import Mouse
from .debug import Debug


# not separate simulation, but for interaction with softbodies
class HardBall:
    def __init__(self, radius, softbodies, texture=None):
        self.position = Mouse.position
        
        self.radius = radius
        self.softbodies = softbodies

        self.center = self.position - pygame.Vector2(self.radius, self.radius)

        self.texture = texture
        #if texture != None:
        #texture = pygame.image.load(texture).convert_alpha()
        #self.texture = Texture.from_surface(renderer, texture)

    def draw(self, screen):
        pygame.draw.circle(screen, (115, 115, 115), self.position, self.radius)

    def draw_sdl2(self):
        # drawing nothing because can't draw circle
        if self.texture != None:
            self.texture.draw(
                [(0, 0), (160, 160)],
                (self.center, (self.radius * 2, self.radius * 2)))

    def update(self):
        self.center = self.position - pygame.Vector2(self.radius, self.radius)
        for softbody in self.softbodies:
            inside = softbody.polygon.collide_point(self.position)
            if inside:
                continue
            
            for point in softbody.points:
                distanceVec = self.position - point.position
                normalDist = distanceVec.normalize()
                distance = distanceVec.length() - self.radius

                if distance < 0:
                    # calculating separating force
                    SepForce = normalDist.elementwise() * -(distance * 1.0)
                    point.acceleration -= SepForce
                    # not sure if this is the best solution, but works fine
                    point.position = self.position - normalDist * self.radius


from pygame.locals import *


class Settinger:
    def __init__(self, softbody):
        self.softbody = softbody

        self.settings = {'gas_amount': True, 'mass': False, 
                        'stiffness': False, 'damping': False,
                        'gravity': False}
        self.settingsKeys = list(self.settings.keys())
        self.CrntSetting = 0

        self.value = 0

    def draw(self):
        key = self.settingsKeys[self.CrntSetting]
        Debug.text([5, 65], f'Editing {key}={self.value}')
    
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_e:
                if self.CrntSetting < len(self.settings) - 1:
                    self.CrntSetting += 1
                else:
                    self.CrntSetting = 0

            if event.key == K_q:
                if self.CrntSetting > 0:
                    self.CrntSetting -= 1
                else:
                    self.CrntSetting = len(self.settings) - 1

            self.settings = {'gas_amount': False, 'mass': False, 
                            'stiffness': False, 'damping': False,
                            'gravity': False}
            self.settings[self.settingsKeys[self.CrntSetting]] = True

            print(f'editing: {self.settingsKeys[self.CrntSetting]}')
            
        
        if event.type == MOUSEWHEEL:
            if self.settings['gas_amount']:
                self.softbody.gas_amount += event.y * 25 
                if self.softbody.gas_amount < 0:
                    self.softbody.gas_amount = 0

                self.value = self.softbody.gas_amount

            if self.settings['mass']:
                for point in self.softbody.points:
                    point.mass += event.y * 0.1
                    if point.mass < 0.1:
                        point.mass = 0.1

                    point.gravity = pygame.Vector2(0, 0.1) * point.mass

                    self.value = point.mass

            if self.settings['stiffness']:
                for spring in self.softbody.springs:
                    spring.stiffness += event.y * 0.005

                    if spring.stiffness < 0:
                        spring.stiffness = 0

                    self.value = spring.stiffness

            if self.settings['damping']:
                for point in self.softbody.points:
                    point.damping += event.y * 0.005

                    if point.damping < 0:
                        point.damping = 0

                    self.value = point.damping
                
            if self.settings['gravity']:
                self.softbody.gravity += (0, event.y * 0.005)

                self.value = self.softbody.gravity

            print(self.value)
            