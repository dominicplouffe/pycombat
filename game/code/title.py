import pygame
import time
from config import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT


class Title:
    def __init__(self, start_game: callable, set_seed: callable) -> None:
        self.display_surface = pygame.display.get_surface()
        self.btn_random = None
        self.btn_seed = None
        self.button_handled = False
        self.title_state = "main_menu"

        # Text box for seed input
        self.active = False
        self.input_text = ""
        self.text_box_rect = None
        self.last_input_time = 0  # For debouncing TEXTINPUT events

        self.start_game = start_game
        self.set_seed = set_seed

    def run(self):
        self.display_surface.fill(BLACK)
        title_font = pygame.font.Font(None, 80)  # Larger font for title
        button_font = pygame.font.Font(None, 50)

        # Title Text (centered at top)
        title_surface = title_font.render("PyCombat", True, WHITE)
        title_rect = title_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        )
        self.display_surface.blit(title_surface, title_rect)

        # Button properties
        button_color = WHITE
        button_width, button_height = 300, 70

        # Random Game Button (Centered)
        self.btn_random = pygame.Rect(
            (WINDOW_WIDTH - button_width) // 2,
            (WINDOW_HEIGHT // 2) - 50,
            button_width,
            button_height,
        )
        btn_random_text = "Random Game"
        pygame.draw.rect(self.display_surface, button_color, self.btn_random)
        random_surface = button_font.render(btn_random_text, True, BLACK)
        random_rect = random_surface.get_rect(center=self.btn_random.center)
        self.display_surface.blit(random_surface, random_rect)

        # Seed Game Button (Centered)
        self.btn_seed = pygame.Rect(
            (WINDOW_WIDTH - button_width) // 2,
            (WINDOW_HEIGHT // 2) + 50,
            button_width,
            button_height,
        )
        btn_seed_text = "Your Seed"
        # Gray out the seed button if there is no input
        seed_color = button_color if self.input_text else (100, 100, 100)
        pygame.draw.rect(self.display_surface, seed_color, self.btn_seed)
        seed_surface = button_font.render(btn_seed_text, True, BLACK)
        seed_rect = seed_surface.get_rect(center=self.btn_seed.center)
        self.display_surface.blit(seed_surface, seed_rect)

        # Text box for seed input (Centered below seed button)
        text_box_width, text_box_height = 300, 50
        self.text_box_rect = pygame.Rect(
            (WINDOW_WIDTH - text_box_width) // 2,
            (WINDOW_HEIGHT // 2) + 150,
            text_box_width,
            text_box_height,
        )
        box_color = WHITE if self.active else (150, 150, 150)
        pygame.draw.rect(self.display_surface, box_color, self.text_box_rect, 2)
        input_surface = button_font.render(self.input_text, True, WHITE)
        input_rect = input_surface.get_rect(center=self.text_box_rect.center)
        self.display_surface.blit(input_surface, input_rect)

    def input(self, event, change_state) -> None:
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_random.collidepoint(event.pos):
                self.start_game()
                self.button_handled = True
            elif self.btn_seed.collidepoint(event.pos) and self.input_text:
                self.set_seed(int(self.input_text))
                self.start_game()
                self.button_handled = True
            elif self.text_box_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        # Handle text input (debounced)
        if event.type == pygame.TEXTINPUT and self.active:
            current_time = time.time()
            # Only accept new digit if at least 300ms have passed
            if current_time - self.last_input_time >= 0.1:
                if event.text.isdigit():
                    self.input_text += event.text
                self.last_input_time = current_time

        # Handle special keys (Backspace and Enter)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.input_text:
                    print(f"Seed: {self.input_text}")
                    self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

    def update(self, event, change_state) -> None:
        self.run()
        self.input(event, change_state)
        self.button_handled = False
