import pygame
from settings import WINDOW_SIZE

class LightingEffect:
    def __init__(self):
        self.effect_size = (500, 500)
        self.light_effect = pygame.Surface(self.effect_size)
        self.light_effect.fill((0, 0, 0))
        pygame.draw.circle(self.light_effect, (255, 255, 255), (self.effect_size[0] // 2, self.effect_size[1] // 2), 250)
        self.light_effect.set_alpha(255)
        self.mouse_pos = None
        self.polygon = []

    def update(self, mouse_pos, polygon):
        self.mouse_pos = mouse_pos
        self.polygon = polygon

    def draw(self, surface):
        if self.mouse_pos is not None:
            new_surface = pygame.Surface(WINDOW_SIZE)
            new_surface.fill((0, 0, 0))
            if self.polygon:
                pygame.draw.polygon(new_surface, (0, 255, 0), self.polygon)
            new_surface.set_colorkey((0, 255, 0))

            effect_pos = (self.mouse_pos[0] - self.effect_size[0] // 2,
                          self.mouse_pos[1] - self.effect_size[1] // 2)

            surface.blit(self.light_effect, effect_pos)
            surface.blit(new_surface, (0, 0))