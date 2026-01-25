# python_bomberman/main.py
import pygame
import sys
import os

# Adjust path to allow running as a module or script
if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .constants import *
from .player import Player
from .levels import Level
from .ui import UI
from .entities import Bomb

class BombermanGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman Python - 10 Levels of Bosses")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.state = STATE_START
        self.reset_game()

    def reset_game(self):
        self.player = Player(1, 1)
        self.current_level_num = 1
        self.load_level(self.current_level_num)
        self.player_name = ""

    def load_level(self, num):
        self.level = Level(num, self.player)
        self.player.rect.topleft = (TILE_SIZE + 4, TILE_SIZE + 4)
        self.player.alive = True

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == STATE_START:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_h:
                        self.state = STATE_HIGHSCORES

            elif self.state == STATE_HIGHSCORES:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_START

            elif self.state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.drop_bomb()

            elif self.state == STATE_GAME_OVER or self.state == STATE_VICTORY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.is_highscore():
                            self.state = STATE_NAME_ENTRY
                        else:
                            self.state = STATE_START

            elif self.state == STATE_NAME_ENTRY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name:
                            self.ui.save_score(self.player_name, self.player.score)
                            self.state = STATE_HIGHSCORES
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 10 and event.unicode.isalnum():
                            self.player_name += event.unicode

    def drop_bomb(self):
        if not self.player.alive: return
        if self.player.bombs_dropped < self.player.max_bombs:
            gx, gy = self.player.get_grid_pos()
            # Don't drop two bombs on same spot
            for b in self.level.bombs:
                if b.x == gx and b.y == gy:
                    return

            bomb = Bomb(gx, gy, self.player.bomb_range, self.player)
            self.level.bombs.append(bomb)
            self.player.bombs_dropped += 1

    def is_highscore(self):
        if not self.ui.scores or len(self.ui.scores) < 10:
            return True
        return self.player.score > self.ui.scores[-1]["score"]

    def update(self, dt):
        if self.state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, self.level)
            self.level.update(dt)

            if not self.player.alive:
                self.player.lives -= 1
                if self.player.lives > 0:
                    self.load_level(self.current_level_num)
                else:
                    self.state = STATE_GAME_OVER

            if self.level.is_cleared:
                if self.current_level_num < 10:
                    self.current_level_num += 1
                    self.load_level(self.current_level_num)
                else:
                    self.state = STATE_VICTORY

    def draw(self):
        if self.state == STATE_START:
            self.ui.draw_start_screen()
        elif self.state == STATE_HIGHSCORES:
            self.ui.draw_highscores()
        elif self.state == STATE_PLAYING:
            self.level.draw(self.screen)
            self.ui.draw_hud(self.current_level_num, self.player.score, self.player.lives)
        elif self.state == STATE_GAME_OVER:
            self.ui.draw_game_over(self.player.score)
        elif self.state == STATE_VICTORY:
            self.ui.draw_victory(self.player.score)
        elif self.state == STATE_NAME_ENTRY:
            self.ui.draw_name_entry(self.player_name)

        pygame.display.flip()

if __name__ == "__main__":
    game = BombermanGame()
    game.run()
