import pygame
from player import Player
import random
import numpy as np
from noise import pnoise2
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DARK_BROWN,
    DARK_GREEN,
    KHAKI,
    DARK_BLUE,
    OBSTACLE,
)
from sprite import RoundedSprite, RectSprite
from coin import Coin
from support import check_overlap

random.seed(0)


class Level:

    def __init__(
        self,
        client,
        lobby_name=None,
        username=None,
        vs_computer=False,
        vs_network=False,
    ) -> None:
        octaves = 12
        freq = 240
        scale = 500

        self.player_score = 0
        self.enemy_score = 0
        self.vs_computer = vs_computer

        self.display_surface = pygame.display.get_surface()
        self.obstacles = self.generate_obstacles(10 if self.vs_computer else 0)
        self.coin = self.generate_coin()
        self.coin.generate(False)

        self.terrain = self.generate_terrain(
            WINDOW_WIDTH, WINDOW_HEIGHT, octaves, freq, scale
        )

        self.all_sprites = pygame.sprite.Group(*self.obstacles, self.coin)
        self.player = Player(
            self.all_sprites, self.obstacles, self.coin, is_enemy=False
        )
        self.enemy = None
        if self.vs_computer:
            self.enemy = Player(
                self.all_sprites, self.obstacles, self.coin, is_enemy=True
            )
        if vs_network:
            self.enemy = Player(
                self.all_sprites,
                self.obstacles,
                self.coin,
                is_enemy=False,
                is_networked=True,
            )

        self.client = client
        self.client.update_callback = self.update_callback
        self.lobby_name = lobby_name
        self.username = username

        self.dt_sum = 0

    def update(self, dt) -> None:
        self.display_surface.fill(DARK_GREEN)
        self.draw_terrain(self.display_surface, self.terrain)
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
        self.draw_score()

        self.dt_sum += dt
        if int(self.dt_sum * 100) % 2 == 0:
            self.client.send_message(
                f"update {self.lobby_name} {self.username} {self.player.rect.x} {self.player.rect.y}"
            )

    def generate_obstacles(self, num_obstacles) -> None:
        obstacles = pygame.sprite.Group()

        for _ in range(num_obstacles):
            size = random.randint(50, 50)
            valid_square = False

            while not valid_square:
                x = random.randint(
                    100, WINDOW_WIDTH - size - 100
                )  # Ensure square is not in the top left corner
                y = random.randint(100, WINDOW_HEIGHT - size - 100)

                new_square = RectSprite(OBSTACLE, size, size, x, y)
                if (
                    not check_overlap(new_square, obstacles, inflate=True)
                    and x > 100
                    and y > 100
                ):
                    valid_square = True
                    obstacles.add(new_square)

        return obstacles

    def generate_terrain(self, width, height, octaves, freq, scale):
        terrain = np.zeros((width, height, 3), dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                # Generate noise value
                noise_val = pnoise2(x / freq, y / freq, octaves=octaves) * scale

                # Map the noise value to a color
                if noise_val < 30:
                    color = DARK_GREEN
                elif 30 <= noise_val < 40:
                    color = DARK_BROWN
                elif 40 <= noise_val < 70:
                    color = KHAKI
                else:
                    color = DARK_BLUE

                terrain[x, y] = color
        return terrain

    def draw_terrain(self, screen, terrain):
        pygame.surfarray.blit_array(screen, terrain)

    def generate_coin(self) -> Coin:
        return Coin(50, self.obstacles, self.increase_score)

    def draw_score(self) -> None:
        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f"Score: {self.player_score} - Enemy: {self.enemy_score}",
            True,
            (255, 255, 255),
        )
        self.display_surface.blit(score_text, (10, 10))

    def increase_score(self, is_enemy) -> None:
        if not is_enemy:
            self.player_score += 1
        else:
            self.enemy_score += 1

    def update_callback(self, x: int, y: int) -> None:
        self.enemy.rect.x = int(x)
        self.enemy.rect.y = int(y)
