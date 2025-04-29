import pygame
import numpy as np
from support import show_text

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
MAX_RAY_DIST = 300
RAY_STEP = 2  # Default step size

# Init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Obstacles
obstacles = [
    pygame.Rect(200, 150, 300, 30),
    pygame.Rect(100, 300, 30, 200),
    pygame.Rect(500, 350, 150, 30)
]

# Configurable rays
num_rays = 180  # Starting value

# Mode States
MODE_RAYS = 0
MODE_EXACT_POLYGON = 1
current_mode = MODE_RAYS  # Default mode is ray mode

def cast_ray(origin, dx, dy, obstacles):
    for i in range(1, MAX_RAY_DIST, RAY_STEP):  # Iterate with step size
        x = origin.x + dx * i
        y = origin.y + dy * i
        point = (int(x), int(y))
        if any(rect.collidepoint(point) for rect in obstacles):
            return point
    return (int(origin.x + dx * MAX_RAY_DIST), int(origin.y + dy * MAX_RAY_DIST))

def draw_obstacles(surface, show):
    if not show:
        return
    for rect in obstacles:
        pygame.draw.rect(surface, (100, 100, 100), rect)

def get_light_polygon(player_pos, directions):
    points = []
    for dx, dy in directions:
        hit_point = cast_ray(player_pos, dx, dy, obstacles)
        points.append(hit_point)
    return points

def generate_directions(num_rays):
    # Using numpy for optimized angle and direction calculations
    angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)
    return np.column_stack((np.cos(angles), np.sin(angles)))  # Array of (dx, dy) pairs

def main():
    global num_rays, RAY_STEP, current_mode
    show_obstacles = True
    running = True

    while running:
        screen.fill("black")
        draw_obstacles(screen, show_obstacles)

        # Player position from mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_pos = pygame.Vector2(mouse_x, mouse_y)
        pygame.draw.circle(screen, (0, 255, 0), player_pos, 5)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    current_mode = (current_mode + 1) % 2  # Only two modes now
                elif event.key == pygame.K_RIGHT:
                    num_rays = min(360, num_rays + 10)
                elif event.key == pygame.K_LEFT:
                    num_rays = max(10, num_rays - 10)
                elif event.key == pygame.K_o:
                    show_obstacles = not show_obstacles
                elif event.key == pygame.K_UP:
                    RAY_STEP = max(1, RAY_STEP + 1)  # Increase step size
                elif event.key == pygame.K_DOWN:
                    RAY_STEP = max(1, RAY_STEP - 1)  # Decrease step size

        directions = generate_directions(num_rays)
        points = get_light_polygon(player_pos, directions)

        if current_mode == MODE_RAYS:
            # Draw individual rays
            for dx, dy in directions:
                hit_point = cast_ray(player_pos, dx, dy, obstacles)
                pygame.draw.line(screen, (255, 255, 255), player_pos, hit_point, 1)

        elif current_mode == MODE_EXACT_POLYGON:
            # Draw exact polygon
            if len(points) > 2:
                pygame.draw.polygon(screen, (255, 255, 255), points)

        pygame.draw.circle(screen, "red", pygame.mouse.get_pos(), 4)

        # Show current mode text
        mode_text = "Ray Mode" if current_mode == MODE_RAYS else "Exact Polygon"

        show_text(screen, f"FPS: {clock.get_fps():.1f}")
        show_text(screen, f"Rays: {num_rays}", y=35)
        show_text(screen, f"Ray Step: {RAY_STEP}", y=60)
        show_text(screen, f"Mode: {mode_text}", y=screen.get_height()-30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
