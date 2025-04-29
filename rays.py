import numpy as np
import pygame
from settings import *

def cast_ray(origin, dx, dy, obstacles):
    for i in range(1, MAX_RAY_DIST, RAY_STEP):
        x = origin.x + dx * i
        y = origin.y + dy * i
        point = (int(x), int(y))
        if any(rect.collidepoint(point) for rect in obstacles):
            return point
    return (int(origin.x + dx * MAX_RAY_DIST), int(origin.y + dy * MAX_RAY_DIST))

def generate_directions(num_rays):
    angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)
    return np.column_stack((np.cos(angles), np.sin(angles)))

def get_light_polygon(player_pos, directions, obstacles):
    return [cast_ray(player_pos, dx, dy, obstacles) for dx, dy in directions]
