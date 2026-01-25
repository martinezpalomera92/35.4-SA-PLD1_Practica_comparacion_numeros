# python_bomberman/entities.py
import pygame
from .constants import *

class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Block(Entity):
    def __init__(self, x, y, destructible=True):
        color = BLOCK_COLOR if destructible else WALL_COLOR
        super().__init__(x, y, color)
        self.destructible = destructible

    def draw(self, surface):
        # Refined drawing for blocks
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 1)
        # Add some "texture"
        if self.destructible:
            pygame.draw.line(surface, WHITE, (self.rect.x + 5, self.rect.y + 5), (self.rect.right - 5, self.rect.bottom - 5), 2)
            pygame.draw.line(surface, WHITE, (self.rect.right - 5, self.rect.y + 5), (self.rect.x + 5, self.rect.bottom - 5), 2)
        else:
            pygame.draw.rect(surface, DARK_GRAY, self.rect.inflate(-10, -10), 2)

class Bomb:
    def __init__(self, x, y, range_dist, owner):
        self.x = x
        self.y = y
        self.range_dist = range_dist
        self.owner = owner
        self.timer = BOMB_TIMER
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def update(self, dt):
        self.timer -= dt
        return self.timer <= 0

    def draw(self, surface):
        # Pulse effect
        import math
        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
        center = self.rect.center
        pygame.draw.circle(surface, BLACK, center, TILE_SIZE // 2 - 5 + pulse)
        pygame.draw.circle(surface, RED, center, TILE_SIZE // 3 + pulse // 2)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = EXPLOSION_DURATION
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def update(self, dt):
        self.timer -= dt
        return self.timer <= 0

    def draw(self, surface):
        alpha = min(255, max(0, int(255 * (self.timer / EXPLOSION_DURATION))))
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        color = (*ORANGE, alpha)
        pygame.draw.rect(s, color, (0, 0, TILE_SIZE, TILE_SIZE))
        surface.blit(s, self.rect.topleft)

class Portal(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PURPLE)
        self.active = False

    def draw(self, surface):
        if not self.active: return
        # Swirling portal effect
        import math
        angle = pygame.time.get_ticks() * 0.005
        center = self.rect.center
        for i in range(5):
            radius = (TILE_SIZE // 2 - 5) - i * 4
            offset_x = math.cos(angle + i) * 5
            offset_y = math.sin(angle + i) * 5
            pygame.draw.circle(surface, PURPLE, (center[0] + offset_x, center[1] + offset_y), radius, 2)
