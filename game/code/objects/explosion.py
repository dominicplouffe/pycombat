import pygame
from config import ANIMATION_SPEED
from pygame import Vector2 as vector
from support import import_image, import_folder_dict


class Explosion(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        center: vector = None,
        callback: callable = None,
    ) -> None:
        super().__init__(groups)

        self.frame_index = 0
        self.frames = import_folder_dict("game", "support", "images", "explosion")
        self.image = import_image("game", "support", "images", "explosion", "1")
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.center = center
        self.callback = callback

    def update(self, dt: float, event) -> None:
        self.frame_index += ANIMATION_SPEED * dt

        int_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[f"{int_index}"]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        if int_index == len(self.frames) - 1:
            self.kill()

            if self.callback:
                self.callback()
