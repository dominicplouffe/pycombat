import pygame
from pygame import Vector2 as vector
from support import import_folder_dict, find_x_y_in_grid
from copy import deepcopy
from config import ANIMATION_SPEED, BLACK
from sprite import RectSprite
from bullet import Bullet
from maze import LevelMaze
from game_timer import Timer
from ai import find_path, find_direction


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        maze: LevelMaze,
        is_bot: bool = True,
        start_pos: vector = vector(75, 75),
        bullets: pygame.sprite.Group = pygame.sprite.Group(),
        all_sprites: pygame.sprite.Group = pygame.sprite.Group(),
        collect_coin_callback: callable = None,
        speed: int = 350,
    ) -> None:
        super().__init__(groups)

        self.frame_index = 0
        self.frames = import_folder_dict("game", "support", "images", "tank")
        self.image = self.frames[f"tank-{self.frame_index}"]
        self.original_image = deepcopy(self.image)
        self.maze = maze
        self.rect = self.image.get_frect(topleft=(start_pos))
        self.direction = vector(0, 0)
        self.speed = speed
        self.gun_pos = vector(1, 0)
        self.is_bot = is_bot
        self.previous_direction = vector()
        self.collide_dir = None
        self.bullets = bullets
        self.all_sprites = all_sprites
        self.bullet_pressed = False
        self.collect_coin_callback = collect_coin_callback
        self.score = 0

        self.hit_rect = RectSprite(
            BLACK, self.rect.width - 10, self.rect.height - 10, 0, 0
        )
        self.hit_rect.rect.center = self.rect.center

        self.view_x = 0
        self.view_y = 0

        self.topleft_grid_col = None
        self.topleft_grid_row = None
        self.bottomright_grid_col = None
        self.bottomright_grid_row = None
        self.grid_to_use = "topleft"
        self.calculate_grid_position()

        self.bullet_timer = Timer(2000)
        self.bullet_timer.activate()

        self.path = []
        self.path_index = 0
        self.compute_path()

    def update(self, dt: float, event) -> None:
        self.animate(dt)
        if not self.is_bot:
            self.direction = self.input(dt, event)
        else:
            self.direction = self.choose_enemy_move()
        self.move(dt)

        self.bullet_timer.update()

    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def increment_score(self) -> None:
        self.score += 1

    def input(self, dt, event) -> vector:
        input_vector = vector(0, 0)

        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            if self.gun_pos.x != 1:
                self.change_gun_direction(vector(1, 0))

        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            if self.gun_pos.x != -1:
                self.change_gun_direction(vector(-1, 0))

        if keys[pygame.K_UP]:
            input_vector.y -= 1
            if self.gun_pos.y != -1:
                self.change_gun_direction(vector(0, -1))

        if keys[pygame.K_DOWN]:
            input_vector.y += 1
            if self.gun_pos.y != 1:
                self.change_gun_direction(vector(0, 1))

        if keys[pygame.K_SPACE]:
            if not self.bullet_timer.active and not self.bullet_pressed:
                self.bullet_pressed = True
                self.bullet_timer.activate()
                self.bullets.add(
                    Bullet(
                        self.all_sprites,
                        self.maze,
                        self.gun_pos,
                        self.rect.topleft,
                        callback=self.stop_bullet,
                    )
                )

        direction = vector(input_vector.x, input_vector.y)
        direction.x = input_vector.normalize().x if input_vector else input_vector.x
        direction.y = input_vector.normalize().y if input_vector else input_vector.y

        self.view_x = max(self.view_x + direction.x, 0)
        self.view_y = max(self.view_y + direction.y, 0)

        return direction

    def animate(self, dt: float) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[f"tank-{int(self.frame_index % len(self.frames))}"]
        self.original_image = deepcopy(self.image)
        self.change_gun_direction(self.gun_pos)

    def move(self, dt: float) -> None:
        self.rect.topleft += self.direction * self.speed * dt
        self.hit_rect.rect.center = self.rect.center
        if self.maze.hit_obstacle(self.hit_rect):
            self.rect.topleft -= self.direction * self.speed * dt
            self.hit_rect.rect.center = self.rect.center
            if abs(self.direction.x) > 0:
                self.view_x = self.view_x - self.direction.x
            if abs(self.direction.y) > 0:
                self.view_y = self.view_y - self.direction.y

            if self.is_bot:
                if self.grid_to_use == "topleft":
                    self.grid_to_use = "bottomright"
                else:
                    self.grid_to_use = "topleft"
        else:
            self.calculate_grid_position()

        if self.maze.collide_coin(self) and self.collect_coin_callback:
            self.collect_coin_callback(self.is_bot)

    def stop_bullet(self) -> None:
        self.bullet_pressed = False
        self.bullet_timer.deactivate()

    def change_gun_direction(self, v: vector):
        if v.x == 1:
            self.image = pygame.transform.rotate(self.original_image, 270)
        elif v.x == -1:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif v.y == 1:
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif v.y == -1:
            self.image = pygame.transform.rotate(self.original_image, 0)

        self.gun_pos = v

    def choose_enemy_move(self) -> None:
        idx = self.path_index

        if idx >= len(self.path):
            self.compute_path()
            return vector(0, 0)

        target_row, target_col = self.path[idx][0], self.path[idx][1]

        if target_col == self.topleft_grid_col and target_row == self.topleft_grid_row:
            if (
                target_col == self.bottomright_grid_col
                and target_row == self.bottomright_grid_row
            ):
                self.path_index += 1

                return vector(0, 0)

        top_direction = find_direction(
            self.topleft_grid_col, self.topleft_grid_row, target_col, target_row
        )
        bottom_direction = find_direction(
            self.bottomright_grid_col, self.bottomright_grid_row, target_col, target_row
        )

        if top_direction.x == 0 and top_direction.y == 0:
            if bottom_direction.x != 0 or bottom_direction.y != 0:
                self.grid_to_use = "bottomright"
        elif bottom_direction.x == 0 and bottom_direction.y == 0:
            if top_direction.x != 0 or top_direction.y != 0:
                self.grid_to_use = "topleft"

        direction = bottom_direction
        if self.grid_to_use == "topleft":
            direction = top_direction

        if direction.x == 1:
            self.change_gun_direction(vector(1, 0))
        elif direction.x == -1:
            self.change_gun_direction(vector(-1, 0))
        elif direction.y == 1:
            self.change_gun_direction(vector(0, 1))
        elif direction.y == -1:
            self.change_gun_direction(vector(0, -1))

        return direction

    def calculate_grid_position(self) -> None:
        self.topleft_grid_col, self.topleft_grid_row = find_x_y_in_grid(
            self.rect.topleft[0], self.rect.topleft[1]
        )
        self.bottomright_grid_col, self.bottomright_grid_row = find_x_y_in_grid(
            self.rect.bottomright[0], self.rect.bottomright[1]
        )

    def compute_path(self) -> None:
        if not self.is_bot:
            return []

        self.path = find_path(
            self.maze.grid,
            (self.topleft_grid_row, self.topleft_grid_col),
            (self.maze.coin.grid_row, self.maze.coin.grid_col),
        )
        self.path_index = 0
