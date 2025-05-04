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

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Snap click to nearest grid cell
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                    grid_obstacles.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))

        screen.fill("black")  

        all_relevant_edges = get_all_relevant_edges(grid_obstacles, Raycaster.get_edges)

        player_pos = pygame.Vector2(pygame.mouse.get_pos())

        points = Raycaster.find_all_intersects(player_pos, all_relevant_edges)

        pygame.draw.circle(screen, (0, 0, 255), player_pos, 2)

        for obstacle in grid_obstacles:
            pygame.draw.rect(screen, (0, 0, 0), obstacle)

        # Update lighting polygon based on new intersections and draw it
        lighting.update(player_pos, points)
        lighting.draw(screen)

        for i, edge in enumerate(all_relevant_edges):
            pygame.draw.line(screen, (0, 255, 255), edge[0], edge[1], 3)

        pygame.display.flip()  
        clock.tick(FPS)        

    pygame.quit()  


if __name__ == "__main__":
    main()
