import pygame
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GOLD, WORLD_WIDTH, WORLD_HEIGHT
from support import check_overlap


class Coin(pygame.sprite.Sprite):
    def __init__(
        self, size: int, obstacles: pygame.sprite.Group, increase_score: callable
    ) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, GOLD, (size // 2, size // 2), size // 2)

        self.size = size
        self.obstacles = obstacles
        self.increase_score = increase_score

    def generate(self, hit, is_enemy=False) -> None:
        valid_coin = False

        while not valid_coin:
            self.rect.x = random.randint(0, WORLD_WIDTH - self.size) + (self.size // 4)
            self.rect.y = random.randint(0, WORLD_HEIGHT - self.size) + (
                self.size // 4
            )

            if not check_overlap(self, self.obstacles):
                valid_coin = True

        if hit:
            self.increase_score(is_enemy)
