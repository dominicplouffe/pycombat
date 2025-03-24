import pygame
import random
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DARK_GREEN,
    OBJ_WIDTH,
    OBJ_HEIGHT,
)

from player import Player
from maze import LevelMaze

random.seed(0)


class Level:

    def __init__(
        self,
        client,
        lobby_name=None,
        username=None,
        vs_computer=False,
        vs_network=False,
        single_player=False,
    ) -> None:

        self.player_score = 0
        self.enemy_score = 0
        self.vs_computer = vs_computer
        self.maze = LevelMaze(self.increase_score)

        self.display_surface = pygame.display.get_surface()
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.bullets = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group(
            *self.maze.obstacles, self.maze.hit_obstacles, self.maze.coin, self.bullets
        )
        self.player = Player(
            self.all_sprites,
            self.maze,
            is_enemy=False,
            bullets=self.bullets,
            all_sprites=self.all_sprites,
        )
        self.enemy = None
        if self.vs_computer and not single_player:
            self.enemy = Player(self.all_sprites, self.maze, is_enemy=True)
        if vs_network and not single_player:
            self.enemy = Player(
                self.all_sprites,
                self.maze,
                is_enemy=False,
                is_networked=True,
            )

        self.client = client
        self.client.update_callback = self.update_callback
        self.lobby_name = lobby_name
        self.username = username

        self.dt_sum = 0

    def update(self, dt, event) -> None:
        self.all_sprites = pygame.sprite.Group(
            *self.maze.hit_obstacles, self.maze.obstacles, self.maze.coin, self.bullets, self.player
        )
        if self.enemy:
            self.all_sprites.add(self.enemy)

        self.world.fill(DARK_GREEN)
        self.all_sprites.update(dt, event)
        self.all_sprites.draw(self.world)
        self.draw_viewport()

        self.dt_sum += dt
        if int(self.dt_sum * 100) % 2 == 0:
            self.client.send_message(
                f"update {self.lobby_name} {self.username} {self.player.rect.x} {self.player.rect.y}"
            )
        self.draw_score()

    def draw_viewport(self) -> None:
        view_x = 0
        view_y = 0
        if self.player.rect.x > WINDOW_WIDTH // 2:
            view_x = self.player.rect.x - (WINDOW_WIDTH // 2)

            if view_x > WINDOW_WIDTH - OBJ_WIDTH:
                view_x = WINDOW_WIDTH - OBJ_WIDTH
        if self.player.rect.y > WINDOW_HEIGHT // 2:
            view_y = self.player.rect.y - (WINDOW_HEIGHT // 2)

            if view_y > WINDOW_HEIGHT - OBJ_HEIGHT:
                view_y = WINDOW_HEIGHT - OBJ_HEIGHT

        self.display_surface.blit(
            self.world,
            (0, 0),
            (view_x, view_y, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

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
