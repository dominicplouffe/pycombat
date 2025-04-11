import pygame


class Label:
    def __init__(
        self,
        text,
        top,
        left,
        font_name=None,
        font_size=20,
        text_color="black",
        bg_color=None,
        padding=0,
        owner=None,
        antialias=True,
    ):
        """
        Initializes a Label.

        Parameters:
            text (str): The text to display.
            top (int): The vertical position on the screen.
            left (int): The horizontal position on the screen.

            font_name (str, optional): The font file to use (or None for default).
            font_size (int, optional): The size of the text font.
            text_color (str, optional): The color of the text.
            bg_color (str, optional): The background color of the label.
                                      If None, the label is rendered transparent.
            padding (int, optional): Padding (in pixels) around the text.
            owner (object, optional): Reference to the object that owns this label.
            antialias (bool, optional): Whether to render text with antialiasing.
        """
        self.text = text
        self.top = top
        self.left = left
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = pygame.Color(text_color)
        # If a background color is provided, store it as a pygame.Color; otherwise keep as None.
        self.bg_color = pygame.Color(bg_color) if bg_color is not None else None
        self.padding = padding
        self.owner = owner
        self.antialias = antialias

        # Initialize the font and render the text.
        if self.font_name:
            self.font = pygame.font.SysFont(font_name, self.font_size)
        else:
            self.font = (
                pygame.font.Font(self.font_name, self.font_size)
                if self.font_name
                else pygame.font.Font(None, self.font_size)
            )
        self.render_text()

    def render_text(self):
        """
        Renders the text surface using the current text and settings. Also computes
        the bounding rectangle for the label including padding.
        """
        # Render the text; if bg_color is set, it will be used as the background for the text.
        self.text_surface = self.font.render(
            self.text, self.antialias, self.text_color, self.bg_color
        )
        text_rect = self.text_surface.get_rect()

        # Apply padding if needed. This creates a rectangle larger than the text.
        if self.padding:
            self.rect = pygame.Rect(
                self.left,
                self.top,
                text_rect.width + 2 * self.padding,
                text_rect.height + 2 * self.padding,
            )
        else:
            self.rect = self.text_surface.get_rect(topleft=(self.left, self.top))

    def draw(self, surface):
        """
        Draws the label on the given surface.

        Parameters:
            surface: The Pygame surface on which to draw the label.
        """
        # If a bg_color is provided and padding is set, optionally draw a background rect.
        # (Even if bg_color is provided in render, drawing a filled rectangle can give more control,
        # for example if you want to include padding.)
        if self.bg_color and self.padding:
            pygame.draw.rect(surface, self.bg_color, self.rect)
        # Blit the rendered text onto the surface, offset by the padding.
        surface.blit(
            self.text_surface, (self.left + self.padding, self.top + self.padding)
        )

    def set_text(self, new_text):
        """
        Updates the label text and re-renders the text surface.

        Parameters:
            new_text (str): The new text string.
        """
        self.text = new_text
        self.render_text()
