import pygame
from settings import WIDTH, HEIGHT, FPS
from raycaster import Raycaster
from lighting import LightingEffect


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    obstacles = [
        pygame.Rect(200, 150, 300, 30),
        pygame.Rect(100, 300, 30, 200),
        pygame.Rect(500, 350, 150, 30),
        pygame.Rect(300, 250, 40, 100),
        pygame.Rect(600, 100, 50, 150),
        pygame.Rect(50, 100, 120, 40),
        pygame.Rect(700, 400, 60, 120),
        pygame.Rect(350, 450, 200, 30),
        pygame.Rect(400, 100, 80, 80)
    ]

    lighting = LightingEffect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        player_pos = pygame.Vector2(pygame.mouse.get_pos())
        edges = Raycaster.get_all_edges(obstacles)
        points = Raycaster.find_all_intersects(player_pos, edges)

        lighting.update(player_pos, points)
        lighting.draw(screen)

        pygame.draw.circle(screen, (0, 0, 255), player_pos, 2)

        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
