import pygame


class Button:
    def __init__(
        self,
        text,
        color,
        on_click,
        top,
        left,
        width=None,
        height=None,
        font_name=None,
        font_size=20,
        text_color="black",
        border_thickness=2,
        border_color="black",
        hover_border_color="gray",
        click_border_color="darkgray",
        padding=10,
        disabled=False,
        on_hover=None,
        owner=None,
    ) -> None:
        """
        Initializes the button.

        Parameters:
            text (str): The text displayed on the button.
            color (str): Background color of the button.
            on_click (callable): Callback function for mouse up event.
            top (int): Top position of the button.
            left (int): Left position of the button.

            width (int, optional): Width of the button.
            height (int, optional): Height of the button.
            font_name (str, optional): Font file or None for default.
            font_size (int, optional): Font size for the text.
            text_color (str, optional): Color of the button text.
            border_thickness (int, optional): Thickness of the border.
            border_color (str, optional): Border color in idle state.
            hover_border_color (str, optional): Border color when hovered.
            click_border_color (str, optional): Border color when clicked.
            padding (int, optional): Padding between text and border.
            disabled (bool, optional): If True, the button is inactive.
            on_hover (callable, optional): Callback when mouse hovers over the button.
        """
        self.text = text
        self.bg_color = pygame.Color(color)
        self.on_click = on_click
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.hover_border_color = hover_border_color
        self.click_border_color = click_border_color
        self.padding = padding
        self.disabled = disabled
        self.on_hover = on_hover

        # Initialize font and render the text
        self.font = (
            pygame.font.Font(self.font_name, self.font_size)
            if self.font_name
            else pygame.font.Font(None, self.font_size)
        )
        self.text_surf = self.font.render(
            self.text, True, pygame.Color(self.text_color)
        )
        text_width, text_height = self.text_surf.get_size()

        # Determine button size based on text size and padding if not explicitly provided
        if self.width is None:
            self.width = text_width + 2 * self.padding
        if self.height is None:
            self.height = text_height + 2 * self.padding

        # Button rectangle
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.hover = False
        self.pressed = False

    def handle_event(self, event) -> None:
        """
        Handles Pygame events.

        Only processes events if the button is not disabled.
        """
        if self.disabled:
            return

        if event.type == pygame.MOUSEMOTION:
            # Update hover status
            if self.rect.collidepoint(event.pos):
                if not self.hover and self.on_hover:
                    self.on_hover()
                self.hover = True
            else:
                self.hover = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.pressed and self.rect.collidepoint(event.pos):
                    self.on_click()  # Trigger the click callback on mouse up
                self.pressed = False

    def draw(self, surface) -> None:
        """
        Draws the button on the given surface.
        """
        # Draw the background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Determine border color based on state
        if self.disabled:
            current_border_color = pygame.Color("gray")
        elif self.pressed:
            current_border_color = pygame.Color(self.click_border_color)
        elif self.hover:
            current_border_color = pygame.Color(self.hover_border_color)
        else:
            current_border_color = pygame.Color(self.border_color)

        # Draw the border
        pygame.draw.rect(
            surface, current_border_color, self.rect, self.border_thickness
        )

        # Center the text and draw it
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, text_rect)
