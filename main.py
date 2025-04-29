import pygame
from settings import *
from rays import *
from visuals import *
from utils import show_text


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    obstacles = [
        pygame.Rect(200, 150, 300, 30),
        pygame.Rect(100, 300, 30, 200),
        pygame.Rect(500, 350, 150, 30)
    ]

    num_rays = NUM_RAYS
    ray_step = RAY_STEP
    current_mode = MODE_RAYS
    show_obstacles = True

    running = True
    while running:
        screen.fill("black")
        draw_obstacles(screen, obstacles, show_obstacles)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_pos = pygame.Vector2(mouse_x, mouse_y)
        pygame.draw.circle(screen, (0, 255, 0), player_pos, 5)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    current_mode = (current_mode + 1) % 2
                elif event.key == pygame.K_RIGHT:
                    num_rays = min(360, num_rays + 10)
                elif event.key == pygame.K_LEFT:
                    num_rays = max(10, num_rays - 10)
                elif event.key == pygame.K_o:
                    show_obstacles = not show_obstacles
                elif event.key == pygame.K_UP:
                    ray_step = max(1, ray_step + 1)
                elif event.key == pygame.K_DOWN:
                    ray_step = max(1, ray_step - 1)

        directions = generate_directions(num_rays)
        points = get_light_polygon(player_pos, directions, obstacles)

        if current_mode == MODE_RAYS:
            draw_rays(screen, player_pos, directions, obstacles, cast_ray)
        elif current_mode == MODE_EXACT_POLYGON:
            draw_polygon(screen, points)

        pygame.draw.circle(screen, "red", pygame.mouse.get_pos(), 4)

        # UI
        mode_text = "Ray Mode" if current_mode == MODE_RAYS else "Exact Polygon"
        show_text(screen, f"FPS: {clock.get_fps():.1f}")
        show_text(screen, f"Rays: {num_rays}", y=35)
        show_text(screen, f"Ray Step: {ray_step}", y=60)
        show_text(screen, f"Mode: {mode_text}", y=100)

        show_text(screen, "O to toggle object visibility", y=screen.get_height()-120)
        show_text(screen, "M to toggle mode", y=screen.get_height()-90)
        show_text(screen, "Up/Down arrow keys to increase/decrease ray step", y=screen.get_height()-60)
        show_text(screen, "Left/Right arow keys to increase/decrease number of rays", y=screen.get_height()-30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
