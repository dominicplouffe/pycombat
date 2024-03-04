import pygame
import time
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK


class Title:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.btn_vs_computer = None
        self.button_handled = False

        self.title_state = 'main_menu'

    def run(self):
        self.display_surface.fill(BLACK)
        font = pygame.font.Font(None, 36)

        # Button properties
        button_color = WHITE
        self.btn_vs_computer = pygame.Rect(100, 100, 200, 50)
        button_text_computer = "VS Computer"

        self.btn_vs_human = pygame.Rect(100, 200, 200, 50)
        button_text_human = "VS Human"

        # Text input box properties
        # input_box_color = WHITE
        # input_box_rect = pygame.Rect(100, 200, 200, 50)
        # input_text = ""
        # 

        # Draw the button

        if self.title_state == "main_menu":
            pygame.draw.rect(self.display_surface, button_color, self.btn_vs_computer)
            button_surface = font.render(button_text_computer, True, BLACK)
            self.display_surface.blit(
                button_surface, (self.btn_vs_computer.x + 20, self.btn_vs_computer.y + 10)
            )

            pygame.draw.rect(self.display_surface, button_color, self.btn_vs_human)
            button_surface = font.render(button_text_human, True, BLACK)
            self.display_surface.blit(
                button_surface, (self.btn_vs_human.x + 20, self.btn_vs_human.y + 10)
            )

        # Draw the text input box
        # pygame.draw.rect(self.display_surface, input_box_color, input_box_rect)
        # text_surface = font.render(input_text, True, BLACK)
        # self.display_surface.blit(
        #     text_surface, (input_box_rect.x + 5, input_box_rect.y + 5)
        # )

    def input(self, event, change_state) -> None:
        # Button click event
        if event.type == pygame.MOUSEBUTTONDOWN and not self.button_handled:
            if self.btn_vs_computer.collidepoint(event.pos):
                self.button_handled = True
                change_state("vs_computer")
            elif self.btn_vs_human.collidepoint(event.pos):
                self.button_handled = True
                change_state("vs_human")

        # Text input event
        # if event.type == pygame.KEYDOWN:
        #     if input_box_rect.collidepoint(pygame.mouse.get_pos()):
        #         if event.key == pygame.K_BACKSPACE:
        #             input_text = input_text[:-1]
        #         else:
        #             input_text += event.unicode

    def update(self, event, change_state) -> None:
        self.run()
        self.input(event, change_state)

        self.button_handled = False
