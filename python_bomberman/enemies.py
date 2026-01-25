# python_bomberman/enemies.py
import pygame
import random
import math
from .constants import *

class Enemy:
    def __init__(self, x, y, color, speed, health=1):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.color = color
        self.speed = speed
        self.health = health
        self.invulnerable_timer = 0
        self.rect = pygame.Rect(self.pixel_x + 4, self.pixel_y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.move_timer = 0

    def update(self, dt, level):
        if self.health <= 0: return False
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

        # Simple AI: Move until hit a wall, then change direction
        dx = self.direction[0] * self.speed
        dy = self.direction[1] * self.speed

        new_rect = self.rect.move(dx, dy)
        collision = False

        for block in level.blocks.values():
            if new_rect.colliderect(block.rect):
                collision = True
                break

        if not collision:
            for bomb in level.bombs:
                if new_rect.colliderect(bomb.rect):
                    collision = True
                    break

        if collision or random.random() < 0.01:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        else:
            self.rect = new_rect
            self.pixel_x = self.rect.x - 4
            self.pixel_y = self.rect.y - 4

        return True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        # Eyes
        eye_color = WHITE
        pygame.draw.circle(surface, eye_color, (self.rect.centerx - 5, self.rect.centery - 2), 3)
        pygame.draw.circle(surface, eye_color, (self.rect.centerx + 5, self.rect.centery - 2), 3)

class Slime(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, 1, 1)

class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE, 1.5, 1)

    def update(self, dt, level):
        # Ghosts move through blocks occasionally? No, let's keep it simple but faster
        return super().update(dt, level)

class Boss(Enemy):
    def __init__(self, x, y, level_num):
        color = PURPLE if level_num < 10 else RED
        speed = 1 + (level_num * 0.1)
        health = 5 + level_num * 2
        super().__init__(x, y, color, speed, health)
        self.level_num = level_num
        # Boss is slightly larger but fits in corridors
        self.rect = pygame.Rect(self.pixel_x + 2, self.pixel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
        self.max_health = health

    def update(self, dt, level):
        if self.health <= 0: return False
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

        # Boss AI: Chase player slowly or move randomly
        px, py = level.player.rect.center
        bx, by = self.rect.center

        if random.random() < 0.02: # Occasional target change
             dx = 1 if px > bx else -1
             dy = 1 if py > by else -1
             self.direction = (dx, dy)

        dx = self.direction[0] * self.speed
        dy = self.direction[1] * self.speed

        new_rect = self.rect.move(dx, dy)
        collision = False

        # Bosses can destroy blocks they touch? Or just collide. Let's say collide with permanent walls.
        for block in level.blocks.values():
            if not block.destructible and new_rect.colliderect(block.rect):
                collision = True
                break

        if not collision:
            self.rect = new_rect
        else:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)])

        return True

    def draw(self, surface):
        # Larger and more menacing
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)

        # Health bar
        bar_width = self.rect.width
        health_width = bar_width * (self.health / self.max_health)
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, health_width, 5))

        # Scary Eyes
        eye_y = self.rect.y + 15
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx - 10, eye_y), 6)
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx + 10, eye_y), 6)
        pygame.draw.circle(surface, BLACK, (self.rect.centerx - 10, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (self.rect.centerx + 10, eye_y), 2)
