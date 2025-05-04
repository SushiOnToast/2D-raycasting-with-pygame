import pygame
import math
from settings import WIDTH, HEIGHT

class Raycaster:
    @staticmethod
    def normalize(v):
        """
        Normalize a vector safely.
        Returns a zero vector if input has zero length.
        """
        if v.length() == 0:
            return pygame.Vector2(0, 0)
        return v.normalize()

    @staticmethod
    def get_edges(rect):
        """
        Return the 4 edges of a rectangle as a list of (point1, point2) tuples.
        Used for raycasting bounds like screen edges.
        """
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        return [
            ((x, y), (x + w, y)),             # Top edge
            ((x + w, y), (x + w, y + h)),     # Right edge
            ((x + w, y + h), (x, y + h)),     # Bottom edge
            ((x, y + h), (x, y))              # Left edge
        ]
    
    @staticmethod
    def find_intersect(edges, ray):
        """
        Find the closest intersection point between a ray and a list of edges.
        Returns the closest intersection point or None if no intersection found.
        """
        origin, direction = ray
        r_px, r_py = origin.x, origin.y
        r_dx, r_dy = direction.x, direction.y

        closest_t1 = float("inf")
        closest_point = None

        for (s1, s2) in edges:
            s_px, s_py = s1
            s_dx = s2[0] - s_px
            s_dy = s2[1] - s_py

            denom = s_dx * r_dy - s_dy * r_dx  # Cross product to check for parallel lines
            if denom == 0:
                continue  # Lines are parallel and won't intersect

            # Solving for intersection point using parametric equations
            t2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / denom
            t1 = (s_px + s_dx * t2 - r_px) / r_dx if r_dx != 0 else (s_py + s_dy * t2 - r_py) / r_dy

            # Check if intersection is valid
            if t1 > 0 and 0 <= t2 <= 1:
                if t1 < closest_t1:
                    closest_t1 = t1
                    closest_point = pygame.Vector2(r_px + r_dx * t1, r_py + r_dy * t1)

        return closest_point

    @staticmethod
    def get_unique_points(edges):
        """
        Return a list of unique points from a list of edges.
        Used to determine where to cast rays.
        """
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
        """
        Cast rays from the origin toward every unique edge point (plus small offsets),
        and collect the resulting intersection points.
        Sorts points by angle to prepare for polygon drawing.
        """
        epsilon = 0.00001  # Small offset to cast slightly left and right of points to avoid gaps
        points = []

        unique_points = Raycaster.get_unique_points(edges)
        for px, py in unique_points:
            angle = math.atan2(py - origin.y, px - origin.x)

            # Cast 3 rays per point: directly, slightly left, and slightly right
            for offset in [0, -epsilon, epsilon]:
                a = angle + offset
                direction = pygame.Vector2(math.cos(a), math.sin(a))
                ray = (origin, direction)
                intersection = Raycaster.find_intersect(edges, ray)
                if intersection:
                    points.append(intersection)

        # Sort points counter-clockwise for drawing polygon
        points.sort(key=lambda p: math.atan2(p.y - origin.y, p.x - origin.x))
        return points
