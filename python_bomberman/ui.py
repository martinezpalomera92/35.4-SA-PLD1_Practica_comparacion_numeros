# python_bomberman/ui.py
import pygame
import json
import os
from .constants import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.highscore_file = "python_bomberman/scores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]
        with open(self.highscore_file, "w") as f:
            json.dump(self.scores, f)

    def draw_text(self, text, font, color, y_offset=0, x_offset=0):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_WIDTH // 2 + x_offset, (SCREEN_HEIGHT - 60) // 2 + y_offset))
        self.screen.blit(img, rect)

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("BOMBERMAN PYTHON", self.font_large, BLUE, -100)
        self.draw_text("Press ENTER to Start", self.font_medium, WHITE, 20)
        self.draw_text("Press H for Highscores", self.font_small, GRAY, 80)

        # Draw a little bomberman decoration
        pygame.draw.circle(self.screen, BLUE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150), 30)
        pygame.draw.circle(self.screen, RED, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150), 15)

    def draw_highscores(self):
        self.screen.fill(BLACK)
        self.draw_text("HIGH SCORES", self.font_large, YELLOW, -150)
        for i, entry in enumerate(self.scores):
            text = f"{i+1}. {entry['name']} - {entry['score']}"
            self.draw_text(text, self.font_small, WHITE, -80 + i * 30)
        self.draw_text("Press ESC to Back", self.font_small, GRAY, 200)

    def draw_game_over(self, score):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.font_large, RED, -50)
        self.draw_text(f"Final Score: {score}", self.font_medium, WHITE, 20)
        self.draw_text("Press ENTER to Continue", self.font_small, GRAY, 80)

    def draw_victory(self, score):
        self.screen.fill(BLACK)
        self.draw_text("VICTORY!", self.font_large, GREEN, -50)
        self.draw_text(f"Final Score: {score}", self.font_medium, WHITE, 20)
        self.draw_text("Press ENTER to Continue", self.font_small, GRAY, 80)

    def draw_name_entry(self, current_name):
        self.screen.fill(BLACK)
        self.draw_text("NEW RECORD!", self.font_large, YELLOW, -100)
        self.draw_text("Enter your name:", self.font_small, WHITE, -20)
        self.draw_text(current_name + "_", self.font_medium, BLUE, 40)
        self.draw_text("Press ENTER to Save", self.font_small, GRAY, 120)

    def draw_hud(self, level_num, score, lives):
        hud_rect = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, DARK_GRAY, hud_rect)
        pygame.draw.line(self.screen, WHITE, (0, SCREEN_HEIGHT - 60), (SCREEN_WIDTH, SCREEN_HEIGHT - 60), 2)

        level_txt = self.font_small.render(f"LEVEL: {level_num}", True, WHITE)
        score_txt = self.font_small.render(f"SCORE: {score}", True, WHITE)
        lives_txt = self.font_small.render(f"LIVES: {lives}", True, RED)

        self.screen.blit(level_txt, (20, SCREEN_HEIGHT - 40))
        self.screen.blit(score_txt, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))
        self.screen.blit(lives_txt, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40))
