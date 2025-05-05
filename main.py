import pygame
from settings import *
from raycaster import Raycaster
from lighting import LightingEffect
from tile_edge_management import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    grid_obstacles = []

    lighting = LightingEffect()

    dragging = False  # Track whether the mouse is being held down
    solid_mode = False
    is_radial = True

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True  # Start dragging
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False  # Stop dragging
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Toggle solid mode with spacebar
                    solid_mode = not solid_mode
                if event.key == pygame.K_e:
                    is_radial = not is_radial

        if dragging:
            # Add tile under mouse position during drag
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
            grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
            new_tile = pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE)
            if new_tile not in grid_obstacles:
                grid_obstacles.append(new_tile)

        screen.fill("black")

        all_relevant_edges = get_all_relevant_edges(grid_obstacles, Raycaster.get_edges)

        player_pos = pygame.Vector2(pygame.mouse.get_pos())

        points = Raycaster.find_all_intersects(player_pos, all_relevant_edges)

        pygame.draw.circle(screen, (0, 0, 255), player_pos, 2)

        if solid_mode:
            lighting.update(player_pos, points)
            lighting.draw(screen, is_radial)

            mode_color = (255, 0, 0) if solid_mode else (0, 0, 0)
            for obstacle in grid_obstacles:
                pygame.draw.rect(screen, mode_color, obstacle)
        else:
            mode_color = (255, 0, 0) if solid_mode else (0, 0, 0)
            for obstacle in grid_obstacles:
                pygame.draw.rect(screen, mode_color, obstacle)

            lighting.update(player_pos, points)
            lighting.draw(screen, is_radial)

        for i, edge in enumerate(all_relevant_edges):
            pygame.draw.line(screen, (0, 255, 255), edge[0], edge[1], 3)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
