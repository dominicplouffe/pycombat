import pygame
from support import import_image


class Background(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        super().__init__()
        self.image = import_image(
            "game", "support", "images", "ground", "rocks_background"
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
