import pygame
from support import import_image


class Wall(pygame.sprite.Sprite):

    def __init__(
        self,
        groups: pygame.sprite.Group,
        x: int,
        y: int,
    ) -> None:
        super().__init__(groups)
        self.image = import_image("game", "support", "images", "wall", "wall2")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
