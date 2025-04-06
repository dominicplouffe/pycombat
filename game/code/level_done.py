import time
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK
from player_stats import PlayerStats


class LevelDone:
    def __init__(
        self, start_game: callable, restart_level: callable, player_stats: PlayerStats
    ) -> None:
        self.display_surface = pygame.display.get_surface()
        self.btn_vs_computer = None
        self.button_handled = False

        self.title_state = "level_done"
        self.message = ""
        self.start_time = time.time()

        self.countdown_time = 5
        self.restart_level = restart_level
        self.start_game = start_game
        self.player_stats = player_stats

    def run(self) -> None:
        self.display_surface.fill(BLACK)
        font = pygame.font.Font(None, 36)

        # Display self.player_stats.coin in the center top of the screen
        stats_text = f"Total Coins: {self.player_stats.coins}"
        stats_surface = font.render(stats_text, True, WHITE)
        stats_rect = stats_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.display_surface.blit(stats_surface, stats_rect)

        text = font.render(self.message, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(text, text_rect)

    def update(self, event, change_state) -> None:
        self.input(event)

        if self.title_state == "game_over":
            self.message = "Game Over! Press R to restart"
        elif self.title_state == "level_done":
            elapsed_time = time.time() - self.start_time
            remaining_time = int(self.countdown_time - elapsed_time)
            if remaining_time > 0:
                self.message = (
                    f"Level Completed! Next level in {remaining_time} seconds"
                )
            else:
                self.restart_level()
        self.run()

    def input(self, event) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.start_game()

    def reset_state(self) -> None:
        self.player_stats.power_ups.clear_power_ups()
        self.start_time = time.time()
