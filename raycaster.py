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
        Improved version with better precision handling and corner cases.
        """
        origin, direction = ray
        r_px, r_py = origin.x, origin.y
        r_dx, r_dy = direction.x, direction.y

        EPSILON = 1e-10  # Small value for floating point comparisons
        closest_t1 = float("inf")
        closest_point = None

        for (s1, s2) in edges:
            s_px, s_py = s1
            s_dx = s2[0] - s_px
            s_dy = s2[1] - s_py

            # Calculate determinant for intersection
            denom = s_dx * r_dy - s_dy * r_dx

            # Skip if lines are parallel (near zero determinant)
            if abs(denom) < EPSILON:
                continue

            # Calculate intersection parameters
            t2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / denom
            
            # Skip if intersection is outside the edge segment
            if t2 < -EPSILON or t2 > 1 + EPSILON:
                continue

            # Calculate t1 more robustly by choosing the more numerically stable calculation
            if abs(r_dx) > abs(r_dy):
                t1 = (s_px + s_dx * t2 - r_px) / r_dx
            else:
                t1 = (s_py + s_dy * t2 - r_py) / r_dy

            # Skip if intersection is behind the ray origin
            if t1 < EPSILON:
                continue

            # Update closest intersection if this one is closer
            if t1 < closest_t1:
                closest_t1 = t1
                # Use precise intersection calculation
                px = s_px + s_dx * t2
                py = s_py + s_dy * t2
                closest_point = pygame.Vector2(px, py)

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
        Cast rays from the origin toward every unique edge point and corner.
        Improved version with better corner handling and more precise angles.
        """
        points = []
        EPSILON = 0.0001  # Smaller epsilon for tighter ray spread
        unique_points = Raycaster.get_unique_points(edges)

        def add_ray_at_angle(angle):
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            ray = (origin, direction)
            intersection = Raycaster.find_intersect(edges, ray)
            if intersection:
                points.append(intersection)

        # Cast rays to all unique points
        for px, py in unique_points:
            base_angle = math.atan2(py - origin.y, px - origin.x)
            
            # Cast 5 rays around each corner point for better coverage
            angles = [
                base_angle,  # Direct ray
                base_angle - EPSILON,  # Slightly left
                base_angle + EPSILON,  # Slightly right
                base_angle - 2 * EPSILON,  # Further left
                base_angle + 2 * EPSILON,  # Further right
            ]
            
            for angle in angles:
                add_ray_at_angle(angle)

        # Sort points by angle for proper polygon rendering
        # Use a more precise sorting method
        def get_angle(point):
            dx = point.x - origin.x
            dy = point.y - origin.y
            angle = math.atan2(dy, dx)
            return angle if angle >= 0 else angle + 2 * math.pi

        points.sort(key=get_angle)
        
        # Remove duplicate points that are very close to each other
        filtered_points = []
        for i, point in enumerate(points):
            if not filtered_points or (point - filtered_points[-1]).length() > EPSILON:
                filtered_points.append(point)

        return filtered_points
    
    
