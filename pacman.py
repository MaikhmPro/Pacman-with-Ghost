import pygame
import random

# Game constants
TILE_SIZE = 24
MAP_WIDTH = 28
MAP_HEIGHT = 31
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

class GameMap:
    def __init__(self):
        # Simplified map string: 0 = dot, 1 = wall, 2 = empty space (no dot)
        self.layout = [
            "1111111111111111111111111111",
            "1000000000110000000000000001",
            "1011111110110111111111101101",
            "1020000000000000000000000201",
            "1011110111110111110111111101",
            "1000000110000000011000000001",
            "1111011110111111011110111111",
            "0001010000100000010000101000",
            "1111010111111111111110101111",
            "1000000100000000000010000001",
            "1111110110111111011011111111",
            "1000000000110000000000000001",
            "1011111111110111111111111101",
            "1012000000000000000000021101",
            "1111011110110111011110111111",
            "1000010000110000010000100001",
            "1011011111111111111111011011",
            "1000000000002200000000000001",
            "1111111111111111111111111111",
            # Shorter map height for demo
        ]

        self.grid = [list(row) for row in self.layout]

    def is_wall(self, x, y):
        if y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[0]):
            return True
        return self.grid[y][x] == '1'

    def is_dot(self, x, y):
        if y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[0]):
            return False
        return self.grid[y][x] == '0' or self.grid[y][x] == '2'

    def eat_dot(self, x, y):
        if self.is_dot(x, y):
            self.grid[y][x] = '2'
            return True
        return False

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                px = x * TILE_SIZE
                py = y * TILE_SIZE
                if tile == '1':
                    pygame.draw.rect(screen, BLUE, (px, py, TILE_SIZE, TILE_SIZE))
                elif tile == '0':
                    pygame.draw.circle(screen, WHITE,
                                       (px + TILE_SIZE // 2, py + TILE_SIZE // 2), 4)
                elif tile == '2':
                    pass


class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.speed = 4  # pixels per frame
        self.px = x * TILE_SIZE
        self.py = y * TILE_SIZE
        self.radius = TILE_SIZE // 2 - 2
        self.mouth_opening = 0
        self.mouth_open = True

    def update(self, game_map):
        if self.can_move(self.next_dx, self.next_dy, game_map):
            self.dx = self.next_dx
            self.dy = self.next_dy

        if self.can_move(self.dx, self.dy, game_map):
            self.px += self.dx * self.speed
            self.py += self.dy * self.speed

        self.x = (self.px + TILE_SIZE // 2) // TILE_SIZE
        self.y = (self.py + TILE_SIZE // 2) // TILE_SIZE

        game_map.eat_dot(self.x, self.y)

        if self.mouth_open:
            self.mouth_opening += 0.1
            if self.mouth_opening >= 0.25:
                self.mouth_open = False
        else:
            self.mouth_opening -= 0.1
            if self.mouth_opening <= 0:
                self.mouth_open = True

    def can_move(self, dx, dy, game_map):
        if dx == 0 and dy == 0:
            return False
        new_px = self.px + dx * self.speed
        new_py = self.py + dy * self.speed
        future_x = (new_px + TILE_SIZE // 2) // TILE_SIZE
        future_y = (new_py + TILE_SIZE // 2) // TILE_SIZE
        if game_map.is_wall(future_x, future_y):
            return False
        return True

    def draw(self, screen):
        center_x = self.px + TILE_SIZE // 2
        center_y = self.py + TILE_SIZE // 2
        mouth_angle = self.mouth_opening * 45

        dir_angle = 0
        if self.dx == 1:
            dir_angle = 0
        elif self.dx == -1:
            dir_angle = 180
        elif self.dy == 1:
            dir_angle = 90
        elif self.dy == -1:
            dir_angle = 270

        pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), self.radius)
        # Mouth polygon
        pygame.draw.polygon(screen, BLACK, [
            (center_x, center_y),
            (center_x + self.radius * pygame.math.Vector2(1, 0).rotate(-dir_angle - mouth_angle).x,
             center_y + self.radius * pygame.math.Vector2(1, 0).rotate(-dir_angle - mouth_angle).y),
            (center_x + self.radius * pygame.math.Vector2(1, 0).rotate(-dir_angle + mouth_angle).x,
             center_y + self.radius * pygame.math.Vector2(1, 0).rotate(-dir_angle + mouth_angle).y),
        ])


class Ghost:
    COLORS = [RED, PINK, CYAN, ORANGE, GREEN]

    def __init__(self, x, y, idx=0):
        self.x = x
        self.y = y
        self.speed = 2
        self.px = x * TILE_SIZE
        self.py = y * TILE_SIZE
        self.dx = 0
        self.dy = 0
        self.radius = TILE_SIZE // 2 - 2
        self.color = Ghost.COLORS[idx % len(Ghost.COLORS)]
        self.direction_choices = [UP, DOWN, LEFT, RIGHT]

    def update(self, game_map, pacman_pos):
        if self.can_move(self.dx, self.dy, game_map):
            self.px += self.dx * self.speed
            self.py += self.dy * self.speed
        else:
            self.choose_direction(game_map, pacman_pos)

        self.x = (self.px + TILE_SIZE // 2) // TILE_SIZE
        self.y = (self.py + TILE_SIZE // 2) // TILE_SIZE

    def can_move(self, dx, dy, game_map):
        if dx == 0 and dy == 0:
            return False
        new_px = self.px + dx * self.speed
        new_py = self.py + dy * self.speed
        future_x = (new_px + TILE_SIZE // 2) // TILE_SIZE
        future_y = (new_py + TILE_SIZE // 2) // TILE_SIZE
        if game_map.is_wall(future_x, future_y):
            return False
        return True

    def choose_direction(self, game_map, pacman_pos):
        possible_dirs = []
        for d in self.direction_choices:
            if self.can_move(d[0], d[1], game_map):
                possible_dirs.append(d)
        if possible_dirs:
            px, py = pacman_pos
            def dist(dir_vec):
                new_x = self.x + dir_vec[0]
                new_y = self.y + dir_vec[1]
                return abs(new_x - px) + abs(new_y - py)
            possible_dirs.sort(key=dist)
            if random.random() < 0.7:
                self.dx, self.dy = possible_dirs[0]
            else:
                self.dx, self.dy = random.choice(possible_dirs)
        else:
            self.dx, self.dy = (0, 0)

    def draw(self, screen):
        center_x = int(self.px + TILE_SIZE // 2)
        center_y = int(self.py + TILE_SIZE // 2)
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
        eye_radius = self.radius // 3
        eye_offset_x = self.radius // 2
        eye_offset_y = self.radius // 3
        pygame.draw.circle(screen, WHITE, (center_x - eye_offset_x, center_y - eye_offset_y), eye_radius)
        pygame.draw.circle(screen, WHITE, (center_x + eye_offset_x, center_y - eye_offset_y), eye_radius)
        pupil_radius = eye_radius // 2
        pupil_pos_left = (center_x - eye_offset_x, center_y - eye_offset_y)
        pupil_pos_right = (center_x + eye_offset_x, center_y - eye_offset_y)
        pygame.draw.circle(screen, BLACK, pupil_pos_left, pupil_radius)
        pygame.draw.circle(screen, BLACK, pupil_pos_right, pupil_radius)


