import pygame
from settings import *
from raycaster import Raycaster
from lighting import LightingEffect

def normalize_edge(edge):
    """Sort edge points and round them to avoid float/direction issues."""
    p1 = tuple(round(coord) for coord in edge[0])
    p2 = tuple(round(coord) for coord in edge[1])
    return tuple(sorted([p1, p2]))


def get_adjacent_tiles(tile, grid_obstacles):
    """Returns tiles that are directly adjacent to the given tile (sharing a side)."""
    adjacent_tiles = []
    for other in grid_obstacles:
        if tile == other:
            continue
        if (
            (tile.x == other.x and abs(tile.y - other.y) == GRID_SIZE) or
            (tile.y == other.y and abs(tile.x - other.x) == GRID_SIZE)
        ):
            adjacent_tiles.append(other)
    return adjacent_tiles


def get_relevant_edges(tile, grid_obstacles, all_edges_method):
    """Get edges that are relevant for raycasting (not shared with adjacent tiles)."""
    all_edges = all_edges_method(tile)
    relevant_edges = []

    adjacent_tiles = get_adjacent_tiles(tile, grid_obstacles)

    for edge in all_edges:
        norm_edge = normalize_edge(edge)
        is_shared = False
        for adj_tile in adjacent_tiles:
            adj_edges = all_edges_method(adj_tile)
            for adj_edge in adj_edges:
                if norm_edge == normalize_edge(adj_edge):
                    is_shared = True
                    break
            if is_shared:
                break
        if not is_shared:
            relevant_edges.append(edge)

    return relevant_edges

def normalize_edge(edge):
    """Sort edge points to make (A, B) and (B, A) the same."""
    p1 = tuple(round(coord) for coord in edge[0])
    p2 = tuple(round(coord) for coord in edge[1])
    return tuple(sorted([p1, p2]))


def deduplicate_edges(edges):
    """Remove duplicate edges by normalizing and using a set."""
    seen = set()
    unique_edges = []
    for edge in edges:
        norm = normalize_edge(edge)
        if norm not in seen:
            seen.add(norm)
            unique_edges.append(edge)  # Keep original direction for drawing/raycasting
    return unique_edges


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    grid_obstacles = []  # List to keep track of obstacles placed on the grid

    lighting = LightingEffect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Calculate grid cell based on the mouse position
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                    # Create a red obstacle (tile) in that cell
                    grid_obstacles.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))

        screen.fill("black")

        # all_relevant_edges = Raycaster.get_all_edges(grid_obstacles)
        all_relevant_edges = []
        for tile in grid_obstacles:
            relevant_edges = get_relevant_edges(tile, grid_obstacles, Raycaster.get_edges)
            all_relevant_edges.extend(relevant_edges)

        all_relevant_edges = deduplicate_edges(all_relevant_edges)


        player_pos = pygame.Vector2(pygame.mouse.get_pos())
        points = Raycaster.find_all_intersects(player_pos, all_relevant_edges)  # Use only relevant edges

        lighting.update(player_pos, points)
        lighting.draw(screen)

        pygame.draw.circle(screen, (0, 0, 255), player_pos, 2)

        # Draw the obstacles (only the grid-based obstacles)
        for obstacle in grid_obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)
        for edge in all_relevant_edges:
            pygame.draw.line(screen, (0, 255, 255), edge[0], edge[1], 5)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
