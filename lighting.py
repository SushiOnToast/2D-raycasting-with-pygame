import pygame
from settings import WINDOW_SIZE

class LightingEffect:
    def __init__(self):
        
        self.light_effect = pygame.transform.scale_by(pygame.image.load("./light_effect.png").convert_alpha(), 0.75)
        self.effect_size = self.light_effect.get_size()
        self.mouse_pos = None
        self.polygon = []

    def update(self, mouse_pos, polygon):
        self.mouse_pos = mouse_pos
        self.polygon = polygon

    def draw(self, surface, circle):
        if self.mouse_pos is not None:
            new_surface = pygame.Surface(WINDOW_SIZE)
            new_surface.fill((0, 0, 0))
            if self.polygon:
                if not circle:
                    color = (255, 255, 255)
                else:
                    color = (0, 255, 0)
                pygame.draw.polygon(new_surface, color, self.polygon)
                # for point in self.polygon:
                #     pygame.draw.line(new_surface, (0, 255, 0), self.mouse_pos, point)
            new_surface.set_colorkey((0, 255, 0))

            effect_pos = (self.mouse_pos[0] - self.effect_size[0] // 2,
                          self.mouse_pos[1] - self.effect_size[1] // 2)
            if circle:
                surface.blit(self.light_effect, effect_pos)
            surface.blit(new_surface, (0, 0))
