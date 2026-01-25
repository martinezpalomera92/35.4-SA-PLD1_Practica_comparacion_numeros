# python_bomberman/levels.py
import random
import pygame
from .constants import *
from .entities import Block, Bomb, Explosion, Portal
from .enemies import Slime, Ghost, Boss

class Level:
    def __init__(self, level_num, player):
        self.level_num = level_num
        self.player = player
        self.blocks = {} # (x, y) -> Block
        self.bombs = []
        self.explosions = []
        self.enemies = []
        self.portal = None
        self.boss = None
        self.is_cleared = False
        self.background_color = self.get_bg_color()
        self.generate_level()

    def get_bg_color(self):
        colors = [
            (44, 62, 80),  # Midnight Blue
            (39, 174, 96), # Nephritis
            (41, 128, 185), # Belize Hole
            (142, 68, 173), # Wisteria
            (211, 84, 0),   # Pumpkin
            (127, 140, 141), # Asbestos
            (22, 160, 133), # Green Sea
            (192, 57, 43),  # Pomegranate
            (44, 62, 80),   # Midnight Blue (Repeat/Dark)
            (20, 20, 25)    # Black (Final)
        ]
        return colors[(self.level_num - 1) % len(colors)]

    def generate_level(self):
        # Clear existing
        self.blocks = {}
        self.bombs = []
        self.enemies = []

        # 1. Permanent Walls
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
                    self.blocks[(x, y)] = Block(x, y, destructible=False)
                elif x % 2 == 0 and y % 2 == 0:
                    self.blocks[(x, y)] = Block(x, y, destructible=False)

        # 2. Destructible Blocks
        for x in range(1, GRID_WIDTH - 1):
            for y in range(1, GRID_HEIGHT - 1):
                if (x, y) in self.blocks: continue
                # Don't place near player start (1, 1)
                if (x <= 2 and y <= 2): continue

                if random.random() < 0.6:
                    self.blocks[(x, y)] = Block(x, y, destructible=True)

        # 3. Enemies
        num_enemies = 2 + self.level_num
        spawn_points = []
        for x in range(1, GRID_WIDTH - 1):
            for y in range(1, GRID_HEIGHT - 1):
                if (x, y) not in self.blocks and (x > 3 or y > 3):
                    spawn_points.append((x, y))

        random.shuffle(spawn_points)
        for i in range(min(num_enemies, len(spawn_points))):
            x, y = spawn_points.pop()
            if random.random() < 0.3:
                self.enemies.append(Ghost(x, y))
            else:
                self.enemies.append(Slime(x, y))

        # 4. Boss
        bx, by = GRID_WIDTH - 2, GRID_HEIGHT - 2
        if bx % 2 == 0: bx -= 1
        if by % 2 == 0: by -= 1

        # Ensure boss area is clear
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (bx+dx, by+dy) in self.blocks:
                    if self.blocks[(bx+dx, by+dy)].destructible:
                        del self.blocks[(bx+dx, by+dy)]

        self.boss = Boss(bx, by, self.level_num)
        self.enemies.append(self.boss)

        # 5. Portal (hidden until boss is dead)
        self.portal = Portal(bx, by)

    def update(self, dt):
        # Update bombs
        for bomb in self.bombs[:]:
            if bomb.update(dt):
                self.explode(bomb)
                self.bombs.remove(bomb)
                bomb.owner.bombs_dropped -= 1

        # Update explosions
        for expl in self.explosions[:]:
            if expl.update(dt):
                self.explosions.remove(expl)

        # Update enemies
        for enemy in self.enemies[:]:
            if not enemy.update(dt, self):
                self.enemies.remove(enemy)
                self.player.score += 100 * self.level_num
            else:
                # Collision with player
                if enemy.rect.colliderect(self.player.rect):
                    self.player.alive = False

        # Check for explosions hitting player or enemies
        for expl in self.explosions:
            if expl.rect.colliderect(self.player.rect):
                self.player.alive = False
            for enemy in self.enemies:
                if enemy.invulnerable_timer <= 0 and expl.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    enemy.invulnerable_timer = 500 # half second

        # Check boss status
        if self.boss not in self.enemies:
            self.portal.active = True

        # Check portal collision
        if self.portal.active and self.portal.rect.colliderect(self.player.rect):
            self.is_cleared = True

    def explode(self, bomb):
        # Center
        self.explosions.append(Explosion(bomb.x, bomb.y))

        # 4 Directions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for r in range(1, bomb.range_dist + 1):
                nx, ny = bomb.x + dx * r, bomb.y + dy * r
                if (nx, ny) in self.blocks:
                    block = self.blocks[(nx, ny)]
                    if block.destructible:
                        self.explosions.append(Explosion(nx, ny))
                        del self.blocks[(nx, ny)]
                    break # Hit a block, stop in this direction
                self.explosions.append(Explosion(nx, ny))

    def draw(self, surface):
        # Draw floor
        surface.fill(self.background_color)

        # Draw blocks
        for block in self.blocks.values():
            block.draw(surface)

        # Draw portal
        self.portal.draw(surface)

        # Draw bombs
        for bomb in self.bombs:
            bomb.draw(surface)

        # Draw explosions
        for expl in self.explosions:
            expl.draw(surface)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface)

        # Draw player
        self.player.draw(surface)
