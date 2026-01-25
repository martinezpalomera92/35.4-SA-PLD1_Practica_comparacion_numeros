# python_bomberman/player.py
import pygame
from .constants import *

class Player:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.speed = 3
        self.bomb_range = 2
        self.max_bombs = 1
        self.bombs_dropped = 0
        self.alive = True
        self.radius = TILE_SIZE // 2 - 4
        self.rect = pygame.Rect(self.pixel_x + 4, self.pixel_y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        self.score = 0
        self.lives = 3

    def handle_input(self, keys, level):
        if not self.alive: return

        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.speed

        if dx != 0:
            self.move(dx, 0, level)

        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.speed

        if dy != 0:
            self.move(0, dy, level)

    def move(self, dx, dy, level):
        new_rect = self.rect.move(dx, dy)

        # Simple collision detection with blocks and bombs
        can_move = True
        for block in level.blocks.values():
            if new_rect.colliderect(block.rect):
                can_move = False
                break

        if can_move:
            for bomb in level.bombs:
                # Allow player to walk away from a bomb they just placed, but not back into it
                if new_rect.colliderect(bomb.rect):
                    # Check if we were already colliding with this bomb
                    if not self.rect.colliderect(bomb.rect):
                        can_move = False
                        break

        if can_move:
            # Boundary check
            if new_rect.left < 0 or new_rect.right > SCREEN_WIDTH or \
               new_rect.top < 0 or new_rect.bottom > SCREEN_HEIGHT - 60:
                can_move = False

        if can_move:
            self.rect = new_rect
            self.pixel_x = self.rect.x - 4
            self.pixel_y = self.rect.y - 4
            self.grid_x = round(self.pixel_x / TILE_SIZE)
            self.grid_y = round(self.pixel_y / TILE_SIZE)

    def draw(self, surface):
        if not self.alive: return
        # Draw player as a character
        center = self.rect.center
        pygame.draw.circle(surface, BLUE, center, self.radius)
        # Eyes
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 5), 3)
        pygame.draw.circle(surface, WHITE, (center[0] + 5, center[1] - 5), 3)
        pygame.draw.circle(surface, BLACK, (center[0] - 5, center[1] - 5), 1)
        pygame.draw.circle(surface, BLACK, (center[0] + 5, center[1] - 5), 1)

    def get_grid_pos(self):
        return round(self.rect.centerx / TILE_SIZE), round(self.rect.centery / TILE_SIZE)
