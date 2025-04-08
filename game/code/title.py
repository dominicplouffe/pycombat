import pygame
import time
import hashlib
from config import (
    WHITE,
    BLACK,
    MOSS_GREEN,
    SAND,
    DARK_GREEN,
    BEIGE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from controls.button import Button
from controls.textbox import TextBox


class Title:
    def __init__(
        self, start_game: callable, set_seed: callable, set_game_mode: callable
    ) -> None:
        self.display_surface = pygame.display.get_surface()
        self.title_state = "main_menu"
        self.input_text = "Custom Seed"
        self.start_game = start_game
        self.set_seed = set_seed
        self.set_game_mode = set_game_mode

        self.setup_ui()

    def setup_ui(self) -> None:
        self.display_surface.fill(MOSS_GREEN)
        title_font = pygame.font.Font(None, 80)  # Larger font for title
        title_surface = title_font.render("PyCombat", True, SAND)
        title_rect = title_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        )
        self.display_surface.blit(title_surface, title_rect)

        button_width, button_height = 300, 70
        left_center_x = WINDOW_WIDTH // 2
        right_center_x = (3 * WINDOW_WIDTH) // 2
        self.btn_vs_bot = Button(
            "Vs. Bot",
            SAND,
            self.on_vs_bot_click,
            top=(WINDOW_HEIGHT // 2) - 50,
            left=left_center_x - button_width // 2,
            width=button_width,
            height=button_height,
            font_size=50,
            text_color=BLACK,
            border_thickness=3,
            border_color=BLACK,
            hover_border_color=DARK_GREEN,
            click_border_color=BEIGE,
            padding=10,
        )

        self.btn_time = Button(
            "Time Attack",
            SAND,
            self.on_time_click,
            top=(WINDOW_HEIGHT // 2) + 50,
            left=left_center_x - button_width // 2,
            width=button_width,
            height=button_height,
            font_size=50,
            text_color=BLACK,
            border_thickness=3,
            border_color=BLACK,
            hover_border_color=DARK_GREEN,
            click_border_color=BEIGE,
            padding=10,
        )

        self.seed_textbox = TextBox(
            "Custom Seed",
            WHITE,
            top=(WINDOW_HEIGHT // 2) - 15,
            left=right_center_x - button_width // 2,
            width=400,
            height=50,
            font_size=35,
            text_color=MOSS_GREEN,
            border_thickness=1,
            border_color=BLACK,
            active_border_color=DARK_GREEN,
            padding=15,
            disabled=False,
            on_change=self.on_seed_change,
            on_submit=None,
            on_click=self.on_seed_click,
            owner=self,
        )
        self.seed_textbox.text = self.input_text  # Set initial text

        # button_font = pygame.font.Font(None, 50)
        # title_pref = button_font.render("Options", True, SAND)
        # title_pref_rect = pygame.Rect(
        #     right_center_x - button_width // 2,
        #     ((WINDOW_HEIGHT // 2) - button_height // 2) - 25,
        #     button_width,
        #     button_height,
        # )
        # self.display_surface.blit(title_pref, title_pref_rect)

        self.btn_vs_bot.draw(self.display_surface)
        self.btn_time.draw(self.display_surface)
        self.seed_textbox.draw(self.display_surface)

    def run(self) -> None:
        pass

    def update(self, event, change_state) -> None:
        self.run()
        if self.title_state == "main_menu":
            self.btn_vs_bot.handle_event(event)
            self.btn_time.handle_event(event)
            self.seed_textbox.handle_event(event)

    def get_seed(self) -> int:
        if self.input_text == "Custom Seed":
            return int(time.time())
        else:
            hash_obj = hashlib.sha256(self.input_text.encode("utf-8"))
            return abs(int(hash_obj.hexdigest(), 16) % 1000000)

    def on_vs_bot_click(self) -> None:
        self.set_seed(self.get_seed())
        self.title_state = "playing"
        self.start_game()

    def on_time_click(self) -> None:
        self.set_game_mode("time_attack")
        self.set_seed(self.get_seed())
        self.title_state = "playing"
        self.start_game()

    def on_seed_change(self, textbox) -> None:
        try:
            self.input_text = textbox.text
        except ValueError:
            pass

    def on_seed_click(self) -> None:
        pass
