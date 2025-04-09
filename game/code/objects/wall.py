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

        # print(x + y, x, y, (x + y) % 2)
        if (x + y) % 9 == 0:
            wall_name = "wall4"
        else:
            wall_name = "wall3"

        self.image = import_image("game", "support", "images", "wall", wall_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
