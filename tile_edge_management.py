from settings import *  
import pygame
from raycaster import Raycaster  

def normalize_edge(edge):
    """Sort edge points to make (A, B) and (B, A) equal, and round coordinates to integers."""
    p1 = tuple(round(coord) for coord in edge[0])
    p2 = tuple(round(coord) for coord in edge[1])
    return tuple(sorted([p1, p2]))


def get_adjacent_tiles(tile, grid_obstacles):
    """
    Return a list of tiles that are directly adjacent (sharing a side) to the given tile.
    Diagonal tiles are not considered adjacent here.
    """
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
    """
    Return edges of a tile that are not shared with any of its adjacent neighbors.
    This helps avoid redundant edges that won't affect raycasting.
    """
    all_edges = all_edges_method(tile)
    relevant_edges = []

    # Get tiles that are directly touching the current one
    adjacent_tiles = get_adjacent_tiles(tile, grid_obstacles)

    # Check each edge and remove it if it's shared with any adjacent tile
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


def deduplicate_edges(edges):
    """
    Remove duplicate edges by normalizing them and keeping only unique ones.
    Ensures (A, B) and (B, A) are treated as the same.
    """
    seen = set()
    unique_edges = []
    for edge in edges:
        norm = normalize_edge(edge)
        if norm not in seen:
            seen.add(norm)
            unique_edges.append(edge) 
    return unique_edges


def merge_edges(edges):
    """
    Merge colinear and connected edges into longer lines to reduce the number of edges.
    Only works for horizontal and vertical lines.
    """
    from collections import defaultdict

    def snap(p):
        """Snap a point to the nearest GRID_SIZE multiple to avoid small float mismatches."""
        return (round(p[0] // GRID_SIZE) * GRID_SIZE,
                round(p[1] // GRID_SIZE) * GRID_SIZE)

    # Separate edges into horizontal and vertical lines, grouped by their y or x coordinate
    horizontal_lines = defaultdict(list)
    vertical_lines = defaultdict(list)

    for edge in edges:
        p1, p2 = sorted([snap(edge[0]), snap(edge[1])])
        if p1[1] == p2[1]:  # horizontal
            y = p1[1]
            horizontal_lines[y].append((p1[0], p2[0]))
        elif p1[0] == p2[0]:  # vertical
            x = p1[0]
            vertical_lines[x].append((p1[1], p2[1]))

    def merge_line_segments(segments):
        """Merge overlapping or touching segments into longer continuous ones."""
        if not segments:
            return []
        segments.sort()
        merged = []
        curr_start, curr_end = segments[0]
        for start, end in segments[1:]:
            if start <= curr_end:  # Overlapping or touching
                curr_end = max(curr_end, end)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = start, end
        merged.append((curr_start, curr_end))
        return merged

    # Reconstruct merged horizontal edges
    merged_edges = []

    for y, segments in horizontal_lines.items():
        merged = merge_line_segments(segments)
        for x1, x2 in merged:
            merged_edges.append(((x1, y), (x2, y)))

    # Reconstruct merged vertical edges
    for x, segments in vertical_lines.items():
        merged = merge_line_segments(segments)
        for y1, y2 in merged:
            merged_edges.append(((x, y1), (x, y2)))

    return merged_edges


def get_all_relevant_edges(obstacles, get_edge_func):
    """
    Combines all relevant edges from the obstacle tiles and screen border edges.
    1. Get non-shared edges from each obstacle tile.
    2. Add screen border edges for limiting rays.
    3. Deduplicate and merge final edge list for optimization.
    """
    all_relevant_edges = []

    # Collect relevant (non-shared) edges from all obstacle tiles
    for tile in obstacles:
        edges = get_relevant_edges(tile, obstacles, get_edge_func)
        all_relevant_edges.extend(edges)

    # Add screen borders (so rays don’t go out of bounds)
    screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    all_relevant_edges.extend(Raycaster.get_edges(screen_rect))

    # Optimize the edge list by removing duplicates and merging
    all_relevant_edges = deduplicate_edges(all_relevant_edges)
    all_relevant_edges = merge_edges(all_relevant_edges)

    return all_relevant_edges
