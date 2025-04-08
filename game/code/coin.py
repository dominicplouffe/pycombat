import pygame
import random
from config import OBJ_WIDTH, OBJ_HEIGHT
from support import import_image


class Coin(pygame.sprite.Sprite):
    def __init__(
        self,
        size: int,
        obstacles: pygame.sprite.Group,
        grid: list[list[int]] = None,
    ) -> None:
        super().__init__()
        self.image = import_image("game", "support", "images", "coin", "coin")
        self.rect = self.image.get_rect()
        # self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, GOLD, (size // 2, size // 2), size // 2)

        self.size = size
        self.obstacles = obstacles
        self.grid_col = 0
        self.grid_row = 0
        self.grid = grid

    def generate(self, hit, is_enemy=False) -> None:
        valid_coin = False

        while not valid_coin:
            rrow = random.randrange(0, len(self.grid))
            rcol = random.randrange(0, len(self.grid[rrow]))

            if self.grid[rrow][rcol] == 0:
                valid_coin = True
                self.grid_col = rcol
                self.grid_row = rrow
                self.rect.x = rcol * OBJ_WIDTH
                self.rect.y = rrow * OBJ_HEIGHT

        if hit:
            # Do something in the future, like play a soune
            pass

    def __str__(self) -> str:
        return f"Coin => Col: {self.grid_col} Row: {self.grid_row}"
