import pygame
from pygame import Vector2 as vector
from support import import_folder_dict
from copy import deepcopy
from config import ANIMATION_SPEED
from sprite import CollideSprite
import random
from bullet import Bullet
from maze import LevelMaze
from game_timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        maze: LevelMaze,
        is_enemy: bool = True,
        is_networked: bool = False,
        start_pos: vector = vector(75, 75),
        bullets: pygame.sprite.Group = pygame.sprite.Group(),
        all_sprites: pygame.sprite.Group = pygame.sprite.Group(),
    ) -> None:
        super().__init__(groups)

        self.frame_index = 0
        self.frames = import_folder_dict("game", "support", "images", "tank")
        self.image = self.frames[f"tank-{self.frame_index}"]
        self.original_image = deepcopy(self.image)
        self.maze = maze
        self.rect = self.image.get_frect(topleft=(start_pos))
        self.direction = vector(0, 0)
        self.speed = 350 if not is_enemy else 200
        self.gun_pos = vector(1, 0)
        self.is_enemy = is_enemy
        self.previous_direction = vector()
        self.collide_dir = None
        self.is_networked = is_networked
        self.bullets = bullets
        self.all_sprites = all_sprites
        self.bullet_pressed = False

        self.view_x = 0
        self.view_y = 0
        self.bullet_timer = Timer(2000)
        self.bullet_timer.activate()

    def update(self, dt: float, event) -> None:
        self.animate(dt)
        if not self.is_enemy:
            self.direction = self.input(dt, event)
        else:
            self.direction = self.choose_enemy_move()
        self.move(dt)

        self.bullet_timer.update()

    def input(self, dt, event) -> None:
        if self.is_networked:
            return vector(0, 0)
        input_vector = vector(0, 0)

        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        # if event.type == pygame.TEXTINPUT:
        #     print(event.type)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.bullet_timer.active and event.button == pygame.BUTTON_LEFT and not self.bullet_pressed:
                self.bullet_pressed = True
                self.bullet_timer.activate()
                self.bullets.add(
                    Bullet(
                        self.all_sprites,
                        self.maze,
                        self.gun_pos,
                        self.rect.topleft,
                    )
                )
            if event.button == pygame.BUTTON_RIGHT:
                self.is_moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.bullet_pressed = False
            if event.button == pygame.BUTTON_RIGHT:
                self.is_moving = False

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
        if self.maze.hit_obstacle(self):
            self.rect.topleft -= self.direction * self.speed * dt
            if abs(self.direction.x) > 0:
                self.view_x = self.view_x - self.direction.x
            if abs(self.direction.y) > 0:
                self.view_y = self.view_y - self.direction.y

        if self.maze.collide_coin(self):
            self.maze.coin.generate(True, is_enemy=self.is_enemy or self.is_networked)

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

        new_rect = CollideSprite(self.rect.copy())
        if self.collide_dir:
            if self.collide_dir == "x":
                new_rect.rect.x += 1
                new_rect.rect.y += self.previous_direction[1]
                if self.collision(new_rect):
                    return vector(0, self.previous_direction[1] * 1.1)
                self.collide_dir = None
                return vector(1, self.previous_direction[1])
            elif self.collide_dir == "-x":
                new_rect.rect.x -= 1
                new_rect.rect.y += self.previous_direction[1]
                if self.collision(new_rect):
                    return vector(0, self.previous_direction[1] * 1.1)
                self.collide_dir = None
                return vector(-1, self.previous_direction[1])
            elif self.collide_dir == "y":
                new_rect.rect.x += self.previous_direction[0]
                new_rect.rect.y += 1
                if self.collision(new_rect):
                    return vector(self.previous_direction[0] * 1.1, 0)
                self.collide_dir = None
                return vector(self.previous_direction[0], 1)
            elif self.collide_dir == "-y":
                new_rect.rect.x += self.previous_direction[0]
                new_rect.rect.y -= 1
                if self.collision(new_rect):
                    return vector(self.previous_direction[0] * 1.1, 0)
                self.collide_dir = None
                return vector(self.previous_direction[0], -1)

        self.collide_dir = None

        move_x, move_y = 0, 0
        if new_rect.rect.x < self.coin.rect.x:
            move_x = 1
        elif new_rect.rect.x > self.coin.rect.x:
            move_x = -1
        if new_rect.rect.y < self.coin.rect.y:
            move_y = 1
        elif new_rect.rect.y > self.coin.rect.y:
            move_y = -1

        new_rect.rect.x += move_x
        if self.collision(new_rect):
            if move_x < 0:
                self.collide_dir = "-x"
            else:
                self.collide_dir = "x"
            new_rect.rect.x -= move_x
            move_x = 0

        new_rect.rect.y += move_y
        if self.collision(new_rect):
            if move_y < 0:
                self.collide_dir = "-y"
            else:
                self.collide_dir = "y"
            new_rect.rect.y -= move_y
            move_y = 0

        if move_x == 0 and move_y == 0:
            move_x, move_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_rect.rect.x += move_x
            new_rect.rect.y += move_y

        if self.collision(new_rect):
            move_x = 0
            move_y = 0

        direction = vector(move_x, move_y)
        if self.collide_dir:
            self.previous_direction = direction.copy()

        return direction
