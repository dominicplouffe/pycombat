import sys
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

        self.seed = 1240
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PyCombat")

        self.player_stats = PlayerStats()

        self.game_state = "title"
        self.clock = pygame.time.Clock()
        self.level_number = 8
        self.title = Title(self.start_game, self.set_seed)

    def start_game(self) -> None:
        random.seed(0)
        self.level_number = 8
        self.level = Level(
            self.display_level_done,
            self.player_stats,
            level_number=self.level_number,
            seed=self.seed,
        )
        self.level_done = LevelDone(
            self.start_game, self.restart_level, self.player_stats
        )
        self.game_state = "playing"

    def restart_level(self) -> None:
        random.seed(0)
        self.level_number += 1
        self.level = Level(
            self.display_level_done,
            self.player_stats,
            self.level_number,
            seed=self.seed,
        )
        self.level_done = LevelDone(
            self.start_game, self.restart_level, self.player_stats
        )
        self.game_state = "playing"

    def set_seed(self, seed: int) -> None:
        self.seed = seed

    def display_level_done(self, player_win: bool) -> None:
        self.game_state = "level_done"
        if player_win:
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
                self.title.run()
                self.title.update(event, self.start_game)
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
