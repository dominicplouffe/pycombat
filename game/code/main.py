import sys
import time
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level
from title import Title
import random
from level_done import LevelDone
from player_stats import PlayerStats


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.seed = 0
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PyCombat")

        self.player_stats = PlayerStats()

        self.game_state = "title"
        self.clock = pygame.time.Clock()
        self.level_number = 1
        self.game_mode = "vs_bot"
        self.title = Title(self.start_game, self.set_seed, self.set_game_mode)
        self.level_start_time = time.time()
        self.level_total_time = 0

    def start_game(self, difficulty: str) -> None:
        random.seed(0)
        self.level_number = 1
        self.level_start_time = time.time()
        self.level_total_time = 0
        self.level = Level(
            self.display_level_done,
            self.player_stats,
            level_number=self.level_number,
            seed=self.seed,
            game_mode=self.game_mode,
            get_total_time=self.get_total_time,
            set_total_time=self.set_total_time,
            start_game=self.start_game,
            reset_game=self.reset_game,
            difficulty=difficulty,
        )
        # self.level.generate()
        self.level_done = LevelDone(
            self.start_game,
            self.restart_level,
            self.reset_game,
            self.player_stats,
            game_mode=self.game_mode,
            get_total_time=self.get_total_time,
            difficulty=difficulty,
        )
        self.game_state = "playing"

    def restart_level(self, difficulty) -> None:
        random.seed(0)
        self.level_number += 1
        self.level_start_time = time.time()
        self.level_total_time = 0
        self.level = Level(
            self.display_level_done,
            self.player_stats,
            self.level_number,
            seed=self.seed,
            game_mode=self.game_mode,
            get_total_time=self.get_total_time,
            set_total_time=self.set_total_time,
            start_game=self.start_game,
            reset_game=self.reset_game,
            difficulty=difficulty,
        )
        self.level_done = LevelDone(
            self.start_game,
            self.restart_level,
            self.reset_game,
            self.player_stats,
            game_mode=self.game_mode,
            get_total_time=self.get_total_time,
            difficulty=difficulty,
        )
        self.game_state = "playing"

    def reset_game(self) -> None:
        self.game_state = "title"
        del self.level
        del self.level_done

    def set_seed(self, seed: int) -> None:
        self.seed = seed

    def set_game_mode(self, mode: str) -> None:
        self.game_mode = mode

    def set_total_time(self) -> None:
        self.level_total_time = time.time() - self.level_start_time

    def get_total_time(self) -> float:
        return self.level_total_time

    def display_level_done(self, player_win: bool) -> None:
        self.game_state = "level_done"
        if player_win and self.level_number < 10:
            self.level_done.title_state = "level_done"
            self.level_done.reset_state()
        else:
            self.level_done.title_state = "game_over"

    def run(self) -> None:
        running = True

        while running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_state == "title":
                self.title.title_state = "main_menu"
                self.title.update(dt, event, self.start_game)
            if self.game_state == "playing":
                self.player_stats.power_ups.update()
                self.level.update(dt, event)
            elif self.game_state == "level_done":
                self.level_done.update(event, self.start_game)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
