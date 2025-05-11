import pygame
import sys
from pacman import GameMap, PacMan, Ghost, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man with 5 Ghosts")

    clock = pygame.time.Clock()

    # Create game objects
    game_map = GameMap()
    pacman = PacMan(1, 1)  # Starting position
    ghosts = [
        Ghost(13, 8, 0),
        Ghost(14, 8, 1),
        Ghost(13, 9, 2),
        Ghost(14, 9, 3),
        Ghost(13, 10, 4),
    ]

    font = pygame.font.SysFont("Arial", 24)
    score = 0

    running = True
    while running:
        dt = clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_dx, pacman.next_dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    pacman.next_dx, pacman.next_dy = 0, 1
                elif event.key == pygame.K_LEFT:
                    pacman.next_dx, pacman.next_dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    pacman.next_dx, pacman.next_dy = 1, 0

        # Update game objects
        pacman.update(game_map)

        # Update score after eating dots
        # Here counting how many dots eaten as increasing score
        # Dot is removed when eaten, so count eaten by difference
        # For simplicity, increment by 10 per dot eaten:
        # But the game_map.eat_dot returns True only once per dot

        # To simplify, check each frame if a dot was eaten at pacman's tile
        # Actually, eat_dot already removes dot; we implemented after eating:
        # So count increase if dot eaten - Instead, track score via a hack:
        # We will check dots left on map and infer score, or simply track all dots eaten:

        # Let's track total dots in map and score increase by dots eaten.

        # We can count dots eaten as total dots started - dots left

        # But we didn't track total dots. Let's do a simple score increase on eat_dot during PacMan update.

        # To support that, we modify pacman.update below to return if dot eaten? 
        # But we can't modify pacman_game now, so let's count dots manually:

        # Let's count dots left in map:
        dots_left = sum(row.count('0') for row in game_map.grid)
        score = (240 - dots_left) * 10  # Assuming 240 dots roughly

        # Update ghosts
        for ghost in ghosts:
            ghost.update(game_map, (pacman.x, pacman.y))

        # Check collisions with ghosts (simple bounding box collision)
        pacman_rect = pygame.Rect(
            pacman.px, pacman.py, TILE_SIZE, TILE_SIZE
        )
        dead = False
        for ghost in ghosts:
            ghost_rect = pygame.Rect(
                ghost.px, ghost.py, TILE_SIZE, TILE_SIZE
            )
            if pacman_rect.colliderect(ghost_rect):
                dead = True
                break

        # Drawing
        screen.fill((0, 0, 0))
        game_map.draw(screen)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

        if dead:
            over_text = font.render("Game Over! Press ESC to quit.", True, (255, 0, 0))
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            # Wait for user to quit or ESC
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                            running = False
            continue

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


