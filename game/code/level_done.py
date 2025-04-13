import time
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, MOSS_GREEN, LABEL_COLOR
from player_stats import PlayerStats
from objects.modal import Modal
from controls.label import Label


class LevelDone:
    def __init__(
        self,
        start_game: callable,
        restart_level: callable,
        reset_game: callable,
        player_stats: PlayerStats,
        game_mode: str = "vs_bot",
        get_total_time: callable = 0,
        difficulty: str = "easy",
    ) -> None:
        self.display_surface = pygame.display.get_surface()
        self.btn_vs_computer = None
        self.button_handled = False
        self.get_total_time = get_total_time

        self.title_state = "level_done"
        self.start_time = time.time()

        self.countdown_time = 5
        self.restart_level = restart_level
        self.reset_game = reset_game
        self.start_game = start_game
        self.player_stats = player_stats
        self.game_mode = game_mode
        self.difficulty = difficulty

        self.settings_sprites = pygame.sprite.Group()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.settings_sprites = pygame.sprite.Group()
        self.settings_modal = Modal(
            self.settings_sprites,
            width=500,
            height=600,
            top=WINDOW_HEIGHT // 2 - 300,
            left=WINDOW_WIDTH // 2 - 250,
            surface=self.display_surface,
            title="Settings",
        )

    def run(self) -> None:
        stats_text = f"Total Coins: {self.player_stats.coins}"
        stats_label = Label(
            stats_text,
            top=WINDOW_HEIGHT // 2 - 300 + 120,
            left=WINDOW_WIDTH // 2 - 200 + 75,
            font_size=30,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )
        stats_label.draw(self.display_surface)

        if self.title_state == "game_over" or self.game_mode == "time_attack":
            self.settings_title = Label(
                "Game Over!",
                top=WINDOW_HEIGHT // 2 - 300 + 25,
                left=WINDOW_WIDTH // 2 - 200 + 100,
                font_size=40,
                text_color=LABEL_COLOR,
                font_name="Menlo",
            )
            self.settings_title.draw(self.display_surface)

            self.r_text = Label(
                "R to restart the same seed",
                top=WINDOW_HEIGHT // 2 - 300 + 200,
                left=WINDOW_WIDTH // 2 - 200 + 40,
                font_size=20,
                text_color=LABEL_COLOR,
                font_name="Menlo",
            )
            self.r_text.draw(self.display_surface)
        elif self.title_state == "level_done":
            self.settings_title = Label(
                "Level Completed!",
                top=WINDOW_HEIGHT // 2 - 300 + 25,
                left=WINDOW_WIDTH // 2 - 200 + 20,
                font_size=40,
                text_color=LABEL_COLOR,
                font_name="Menlo",
            )
            self.settings_title.draw(self.display_surface)

            elapsed_time = time.time() - self.start_time
            remaining_time = int(self.countdown_time - elapsed_time)
            if remaining_time > 0:
                self.time_text = Label(
                    f"Next level in {remaining_time} seconds",
                    top=WINDOW_HEIGHT // 2 - 300 + 200,
                    left=WINDOW_WIDTH // 2 - 200 + 60,
                    font_size=20,
                    text_color=LABEL_COLOR,
                    font_name="Menlo",
                )
                self.time_text.draw(self.display_surface)
            else:
                self.restart_level(self.difficulty)
            self.settings_title.draw(self.display_surface)

        self.m_text = Label(
            "M to return to the main menu",
            top=WINDOW_HEIGHT // 2 - 300 + 240,
            left=WINDOW_WIDTH // 2 - 200 + 20,
            font_size=20,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )
        self.m_text.draw(self.display_surface)

        # Display the messages
        # for i, message in enumerate(self.messages):
        #     font_size = 20 if message != "Game Over!" else 30
        #     left = 450 if message != "Game Over!" else WINDOW_WIDTH // 2 - 200 + 100
        #     label = Label(
        #         message,
        #         top=WINDOW_HEIGHT // 2 - 300 + 200 + i * 40,
        #         left=left,
        #         font_size=font_size,
        #         text_color=LABEL_COLOR,
        #         font_name="Menlo",
        #     )
        #     label.draw(self.display_surface)

        # text = font.render(self.message, True, WHITE)
        # text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        # self.display_surface.blit(text, text_rect)

        # if self.game_mode == "time_attack":
        #     time_text = f"Finish Time: {self.get_total_time():.2f} seconds"
        #     time_surface = font.render(time_text, True, WHITE)
        #     time_rect = time_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
        #     self.display_surface.blit(time_surface, time_rect)

    def update(self, event, change_state) -> None:
        self.display_surface.fill(MOSS_GREEN)
        self.settings_sprites.update(None, event)
        self.settings_sprites.draw(self.display_surface)
        # self.settings_title.draw(self.display_surface)

        self.input(event)

        # if (
        #     self.title_state == "game_over"
        #     or self.game_mode == "time_attack"
        #     and not self.messages_added
        # ):
        #     self.messages.append("Game Over!")
        #     self.messages.append("R to restart the same seed")
        #     self.messages.append("M to return to the main menu")
        #     self.messages_added = True
        # elif self.title_state == "level_done":
        #     elapsed_time = time.time() - self.start_time
        #     remaining_time = int(self.countdown_time - elapsed_time)
        #     if remaining_time > 0:
        #         self.message = (
        #             f"Level Completed! Next level in {remaining_time} seconds"
        #         )
        #     else:
        #         self.restart_level(self.difficulty)
        self.run()

    def input(self, event) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.start_game(self.difficulty)
        elif keys[pygame.K_m]:
            self.reset_game()

    def reset_state(self) -> None:
        self.player_stats.power_ups.clear_power_ups()
        self.start_time = time.time()
