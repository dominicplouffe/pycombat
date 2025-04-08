import pygame
import time


class TextBox:
    def __init__(
        self,
        text,
        color,
        top,
        left,
        width=None,
        height=None,
        font_name=None,
        font_size=20,
        text_color="black",
        border_thickness=2,
        border_color="black",
        active_border_color="blue",
        padding=10,
        disabled=False,
        on_change=None,
        on_submit=None,
        on_click=None,
        owner=None,
    ) -> None:
        """
        Initializes the TextBox.

        Parameters:
            text (str): Initial text to display in the textbox.
            color (str): Background color of the textbox.
            top (int): Top position of the textbox.
            left (int): Left position of the textbox.

            width (int, optional): Width of the textbox (if None, auto-computed from text and padding).
            height (int, optional): Height of the textbox (if None, auto-computed from text and padding).
            font_name (str, optional): A font file or None to use the default font.
            font_size (int, optional): Font size used for the text.
            text_color (str, optional): Color of the displayed text.
            border_thickness (int, optional): Thickness of the textbox border.
            border_color (str, optional): Color of the border when the textbox is inactive.
            active_border_color (str, optional): Border color when the textbox is active (focused).
            padding (int, optional): Space between the text and the edge of the textbox.
            disabled (bool, optional): If True, the textbox ignores events.
            on_change (callable, optional): Callback when the text changes. It receives the TextBox instance.
            on_submit (callable, optional): Callback when the ENTER key is pressed. It receives the TextBox instance.
            owner (object, optional): An optional reference to the calling object.
        """
        self.text = text
        self.bg_color = pygame.Color(color)
        self.top = top
        self.left = left
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = pygame.Color(text_color)
        self.border_thickness = border_thickness
        self.border_color = pygame.Color(border_color)
        self.active_border_color = pygame.Color(active_border_color)
        self.padding = padding
        self.disabled = disabled
        self.on_change = on_change
        self.on_submit = on_submit
        self.on_click = on_click
        self.owner = owner

        # Whether the textbox is focused and accepting keyboard input.
        self.active = False

        # Initialize font and render the initial text surface.
        self.font = (
            pygame.font.Font(self.font_name, self.font_size)
            if self.font_name
            else pygame.font.Font(None, self.font_size)
        )
        self.text_surface = self.font.render(self.text, True, self.text_color)

        # If dimensions are not provided, calculate them from the text size and padding.
        if width is None:
            self.width = self.text_surface.get_width() + 2 * self.padding
        else:
            self.width = width

        if height is None:
            self.height = self.text_surface.get_height() + 2 * self.padding
        else:
            self.height = height

        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        # Cursor state for a blinking cursor while editing.
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # milliseconds
        self.last_input_time = 0  # For debouncing TEXTINPUT events
        self.last_char = None  # For debouncing backspace

    def handle_event(self, event):
        """
        Processes events for focus and text input.
        """
        if self.disabled:
            return

        # Handle mouse events to manage focus.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.on_click()  # Trigger the click callback on mouse up

        # When active, handle keyboard events.
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_time = time.time()
                if current_time - self.last_input_time >= 0.15:
                    self.text = self.text[:-1]
                    self.last_input_time = current_time
                    if self.on_change:
                        self.on_change(self)

            elif event.key == pygame.K_RETURN:
                if self.on_submit:
                    self.on_submit(self)
                self.active = False  # Optionally lose focus after submission.
        elif event.type == pygame.TEXTINPUT:
            current_time = time.time()
            if (
                current_time - self.last_input_time >= 0.15
                or self.last_char != event.text[0]
            ):
                self.text += event.text
                self.last_char = event.text[0]
                self.last_input_time = current_time
                if self.on_change:
                    self.on_change(self)

        # Re-render the text after any change.
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def update(self, dt) -> None:
        """
        Updates the cursor blinking state.

        Args:
            dt (int): The time in milliseconds since the last update.
        """
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer %= self.cursor_interval
        else:
            self.cursor_visible = False

    def draw(self, surface) -> None:
        """
        Renders the textbox on the given surface.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Draw the textbox background.
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Choose border color based on whether the textbox is active.
        current_border_color = (
            self.active_border_color if self.active else self.border_color
        )
        pygame.draw.rect(
            surface, current_border_color, self.rect, self.border_thickness
        )

        # Draw the text at the specified padding.
        surface.blit(
            self.text_surface, (self.rect.x + self.padding, self.rect.y + self.padding)
        )

        # Draw a blinking cursor if the textbox is active.
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + self.padding + self.text_surface.get_width() + 2
            cursor_y = self.rect.y + self.padding
            cursor_height = self.text_surface.get_height()
            pygame.draw.line(
                surface,
                self.text_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                2,
            )
