import pygame
from pygame import Vector2 as vector
from support import import_image
from sprite import CollideSprite
from maze import LevelMaze


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        maze: LevelMaze,
        gun_pos: vector,
        player_topleft: vector,
        callback: callable = None,
    ) -> None:
        super().__init__(groups)
        self.direction = vector(gun_pos[0], gun_pos[1])
        self.image = import_image("game", "support", "images", "bullet", "bullet")
        self.rect = self.image.get_rect()
        self.rect.x = player_topleft[0] - 7.5
        self.rect.y = player_topleft[1] - 7.5

        self.collider_rect = pygame.Rect(0, 0, 15, 15)
        self.collider_rect.x = self.rect.x + 33
        self.collider_rect.y = self.rect.y + 33

        if self.direction.x == 1:
            self.rect.x += 50
        elif self.direction.x == -1:
            self.rect.x -= 50
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction.y == 1:
            self.rect.y += 50
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direction.y == -1:
            self.rect.y -= 50
            self.image = pygame.transform.rotate(self.image, 90)
        self.speed = 500
        self.maze = maze

        self.callback = callback

    def update(self, dt: float, event) -> None:
        self.move(dt)

    def move(self, dt: float) -> None:
        self.rect.topleft += self.direction * self.speed * dt
        self.collider_rect.topleft += self.direction * self.speed * dt

        if self.maze.bullet_hit_obstacle(CollideSprite(self.collider_rect)):
            self.kill()

            if self.callback:
                self.callback()
