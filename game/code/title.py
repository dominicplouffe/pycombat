import pygame
import time
import hashlib
from config import (
    MOSS_GREEN,
    DARK_GREEN,
    BEIGE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BUTTON_BACKGROUND,
    BUTTON_BORDER,
    BUTTON_TEXT,
    LABEL_COLOR,
    RECT_BACKGROUND,
)
from controls.button import Button
from controls.textbox import TextBox
from controls.label import Label
from objects.star import Star
from objects.modal import Modal


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

        self.show_settings = False

        self.setup_ui()
        self.setup_settings()

    def setup_ui(self) -> None:
        self.display_surface.fill(MOSS_GREEN)

        # Create a rectangle for the title
        self.title_rect = pygame.Rect(
            0,
            140,
            WINDOW_WIDTH,
            120,
        )

        self.title_label = Label(
            "PyCombat",
            top=150,
            left=WINDOW_WIDTH // 2 - 200,
            font_size=80,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )

        self.ui_sprites = pygame.sprite.Group()
        star = Star(self.ui_sprites, self.title_label.rect.left - 85, 170)
        self.ui_sprites.add(star)
        star = Star(self.ui_sprites, self.title_label.rect.right + 25, 170)
        self.ui_sprites.add(star)

        button_width, button_height = 250, 50
        self.btn_vs_bot = Button(
            "Play Bot",
            BUTTON_BACKGROUND,
            self.on_vs_bot_click,
            top=(WINDOW_HEIGHT // 2) - 90,
            left=WINDOW_WIDTH // 2 - button_width // 2,
            width=button_width,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
        )

        self.btn_time = Button(
            "Time Attack",
            BUTTON_BACKGROUND,
            self.on_time_click,
            top=(WINDOW_HEIGHT // 2) - 15,
            left=WINDOW_WIDTH // 2 - button_width // 2,
            width=button_width,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
        )

        self.btn_options = Button(
            "Options",
            BUTTON_BACKGROUND,
            self.on_settings_click,
            top=(WINDOW_HEIGHT // 2) + 60,
            left=WINDOW_WIDTH // 2 - button_width // 2,
            width=button_width,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
            disabled=False,
        )

    def setup_settings(self) -> None:
        button_height = 50
        # Settings UI Elements
        self.settings_sprites = pygame.sprite.Group()
        self.settings_modal = Modal(
            self.settings_sprites,
            width=400,
            height=600,
            top=WINDOW_HEIGHT // 2 - 300,
            left=WINDOW_WIDTH // 2 - 200,
            surface=self.display_surface,
            title="Settings",
        )
        self.settings_title = Label(
            "Options",
            top=WINDOW_HEIGHT // 2 - 300 + 25,
            left=WINDOW_WIDTH // 2 - 200 + 110,
            font_size=40,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )
        self.btn_settings_ok = Button(
            "Ok",
            BUTTON_BACKGROUND,
            self.on_settings_click,
            top=(WINDOW_HEIGHT // 2) + 180,
            left=WINDOW_WIDTH // 2 - 200 // 2,
            width=200,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
        )
        self.custom_seed_label = Label(
            "Custom Seed",
            top=WINDOW_HEIGHT // 2 - 300 + 110,
            left=WINDOW_WIDTH // 2 - 200 + 25,
            font_size=30,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )
        self.seed_textbox = TextBox(
            "",
            BUTTON_BACKGROUND,
            top=WINDOW_HEIGHT // 2 - 300 + 160,
            left=WINDOW_WIDTH // 2 - 200 + 30,
            width=340,
            height=50,
            font_size=35,
            text_color=MOSS_GREEN,
            border_thickness=1,
            border_color=BEIGE,
            active_border_color=DARK_GREEN,
            padding=15,
            disabled=False,
            on_change=self.on_seed_change,
            on_submit=None,
            on_click=self.on_seed_click,
            owner=self,
        )
        self.custom_seed_labe_help = Label(
            "Enter text to generate a custom seed",
            top=WINDOW_HEIGHT // 2 - 300 + 220,
            left=WINDOW_WIDTH // 2 - 200 + 30,
            font_size=15,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )

        self.difficulty_label = Label(
            "Difficulty",
            top=WINDOW_HEIGHT // 2 - 300 + 280,
            left=WINDOW_WIDTH // 2 - 200 + 25,
            font_size=30,
            text_color=LABEL_COLOR,
            font_name="Menlo",
        )

        self.btn_easy = Button(
            "Easy",
            BUTTON_BACKGROUND,
            self.on_difficulty_click,
            top=(WINDOW_HEIGHT // 2) + 30,
            left=WINDOW_WIDTH // 2 - 200 + 30,
            width=150,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
        )

        self.btn_hard = Button(
            "Hard",
            BUTTON_BACKGROUND,
            self.on_difficulty_click,
            top=(WINDOW_HEIGHT // 2) + 30,
            left=WINDOW_WIDTH // 2 - 200 + 220,
            width=150,
            height=button_height,
            font_size=30,
            font_name="Menlo",
            text_color=BUTTON_TEXT,
            border_thickness=1,
            border_color=BUTTON_BORDER,
            hover_border_color=BEIGE,
            click_border_color=BEIGE,
            padding=5,
        )

    def run(self) -> None:
        self.display_surface.fill(MOSS_GREEN)
        pygame.draw.rect(self.display_surface, RECT_BACKGROUND, self.title_rect)
        self.btn_vs_bot.draw(self.display_surface)
        self.btn_time.draw(self.display_surface)
        self.btn_options.draw(self.display_surface)
        self.title_label.draw(self.display_surface)

    def draw_settings(self, dt, event) -> None:
        self.settings_sprites.update(dt, event)
        self.settings_sprites.draw(self.display_surface)

        self.settings_title.draw(self.display_surface)
        self.btn_settings_ok.draw(self.display_surface)
        self.custom_seed_label.draw(self.display_surface)
        self.seed_textbox.draw(self.display_surface)
        self.custom_seed_labe_help.draw(self.display_surface)

        self.difficulty_label.draw(self.display_surface)
        self.btn_easy.draw(self.display_surface)
        self.btn_hard.draw(self.display_surface)

    def update(self, dt, event, change_state) -> None:
        self.run()
        if self.title_state == "main_menu":
            self.btn_vs_bot.handle_event(event)
            self.btn_time.handle_event(event)
            self.btn_options.handle_event(event)
            self.btn_settings_ok.handle_event(event)
            self.seed_textbox.handle_event(event)

            self.ui_sprites.update(dt, event)
            self.ui_sprites.draw(self.display_surface)

            if self.show_settings:
                self.draw_settings(dt, event)

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

    def on_settings_click(self) -> None:
        self.show_settings = not self.show_settings

    def on_difficulty_click(self) -> None:
        pass

    def on_seed_change(self, textbox) -> None:
        try:
            self.input_text = textbox.text
        except ValueError:
            pass

    def on_seed_click(self) -> None:
        pass
