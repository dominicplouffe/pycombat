import pygame
import random
from config import OBJ_WIDTH, OBJ_HEIGHT
from support import import_image


class Ammo(pygame.sprite.Sprite):
    def __init__(
        self,
        obstacles: pygame.sprite.Group,
        grid: list[list[int]] = None,
    ) -> None:
        super().__init__(obstacles)
        self.image = import_image("game", "support", "images", "ammo", "ammo")
        self.rect = self.image.get_rect()
        self.obstacles = obstacles
        self.grid_col = 0
        self.grid_row = 0
        self.grid = grid

    def generate(self) -> None:
        valid_ammo = False

        while not valid_ammo:
            rrow = random.randrange(0, len(self.grid))
            rcol = random.randrange(0, len(self.grid[rrow]))

            if self.grid[rrow][rcol] == 0:
                valid_ammo = True
                self.grid_col = rcol
                self.grid_row = rrow
                self.rect.x = rcol * OBJ_WIDTH + ((OBJ_WIDTH - self.rect.width) // 2)
                self.rect.y = rrow * OBJ_HEIGHT + ((OBJ_HEIGHT - self.rect.width) // 2)

    def __str__(self) -> str:
        return f"Ammo => Col: {self.grid_col} Row: {self.grid_row}"
