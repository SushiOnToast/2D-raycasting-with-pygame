import pygame


def draw_obstacles(surface, obstacles, show=True):
    if show:
        for rect in obstacles:
            pygame.draw.rect(surface, (100, 100, 100), rect)


def draw_rays(surface, player_pos, directions, obstacles, cast_ray_func):
    for dx, dy in directions:
        hit_point = cast_ray_func(player_pos, dx, dy, obstacles)
        pygame.draw.line(surface, (255, 255, 255), player_pos, hit_point, 1)


def draw_polygon(surface, points):
    if len(points) > 2:
        pygame.draw.polygon(surface, (255, 255, 255), points)
