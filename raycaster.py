import pygame
import math
from settings import WIDTH, HEIGHT

class Raycaster:
    @staticmethod
    def normalize(v):
        if v.length() == 0:
            return pygame.Vector2(0, 0)
        return v.normalize()

    @staticmethod
    def get_edges(rect):
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        return [
            ((x, y), (x + w, y)),
            ((x + w, y), (x + w, y + h)),
            ((x + w, y + h), (x, y + h)),
            ((x, y + h), (x, y))
        ]

    @staticmethod
    def get_all_edges(obstacles):
        edges = []
        for rect in obstacles:
            edges.extend(Raycaster.get_edges(rect))
        screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        edges.extend(Raycaster.get_edges(screen_rect))
        return edges

    @staticmethod
    def find_intersect(edges, ray):
        origin, direction = ray
        r_px, r_py = origin.x, origin.y
        r_dx, r_dy = direction.x, direction.y

        closest_t1 = float("inf")
        closest_point = None

        for (s1, s2) in edges:
            s_px, s_py = s1
            s_dx = s2[0] - s_px
            s_dy = s2[1] - s_py

            denom = s_dx * r_dy - s_dy * r_dx
            if denom == 0:
                continue

            t2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / denom
            t1 = (s_px + s_dx * t2 - r_px) / r_dx if r_dx != 0 else (s_py + s_dy * t2 - r_py) / r_dy

            if t1 > 0 and 0 <= t2 <= 1:
                if t1 < closest_t1:
                    closest_t1 = t1
                    closest_point = pygame.Vector2(r_px + r_dx * t1, r_py + r_dy * t1)

        return closest_point

    @staticmethod
    def get_unique_points(edges):
        seen = set()
        points = []
        for a, b in edges:
            for p in [a, b]:
                if p not in seen:
                    seen.add(p)
                    points.append(p)
        return points

    @staticmethod
    def find_all_intersects(origin, edges):
        epsilon = 0.00001
        points = []

        unique_points = Raycaster.get_unique_points(edges)
        for px, py in unique_points:
            angle = math.atan2(py - origin.y, px - origin.x)

            for offset in [0, -epsilon, epsilon]:
                a = angle + offset
                direction = pygame.Vector2(math.cos(a), math.sin(a))
                ray = (origin, direction)
                intersection = Raycaster.find_intersect(edges, ray)
                if intersection:
                    points.append(intersection)

        points.sort(key=lambda p: math.atan2(p.y - origin.y, p.x - origin.x))
        return points
