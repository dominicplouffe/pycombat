import pygame
from support import import_image


class Modal(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        top: int,
        left: int,
        width: int,
        height: int,
        title: str = "",
        font_name=None,
        font_size=20,
        text_color="white",
        antialias=True,
        bg_color=None,
        surface: pygame.Surface = None,
    ) -> None:
        super().__init__(groups)

        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.title = title
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.antialias = antialias
        self.padding = 10
        self.bg_color = bg_color
        self.image = import_image("game", "support", "images", "ui", "modal")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(
            center=(left + width // 2, top + height // 2),
        )
        if font_name:
            self.font = pygame.font.SysFont(font_name, self.font_size)
        else:
            self.font = (
                pygame.font.Font(self.font_name, self.font_size)
                if self.font_name
                else pygame.font.Font(None, self.font_size)
            )
