import pygame
pygame.init()
font = pygame.font.Font(None, 30)


def show_text(surface, info, x=10, y=10):
    text_surf = font.render(str(info), True, "white")
    text_rect = text_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(surface, "black", text_rect)
    surface.blit(text_surf, text_rect)
