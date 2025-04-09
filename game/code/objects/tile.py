import pygame
import random
from support import import_image
from config import OBJ_WIDTH, OBJ_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        tile_type: str = "grass",
        width: int = OBJ_WIDTH,
        height: int = OBJ_HEIGHT,
    ) -> None:
        super().__init__()
        self.image = import_image("game", "support", "images", "ground", f"{tile_type}")

        degree_to_rotate = random.choice([0, 90, 180, 270])

        # rotate self.image 90 degrees
        self.image = pygame.transform.rotate(self.image, degree_to_rotate)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def draw(self, surface: pygame.Surface) -> None:
        # Draw the tile on the surface
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Background(pygame.sprite.Sprite):
    def __init__(self, big_tile_surface):
        super().__init__()
        self.image = big_tile_surface
        self.rect = self.image.get_rect()


def create_background(
    window_width: int = WORLD_WIDTH,
    window_height: int = WORLD_HEIGHT,
    tile_width: int = OBJ_WIDTH,
    tile_height: int = OBJ_HEIGHT,
) -> pygame.Surface:
    # Create a new surface that will hold the whole tile grid
    big_tile = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    cols = window_width // tile_width
    rows = window_height // tile_height

    tile_types = [
        "rocks_1",
        "rocks_2",
    ]

    # Fill in the composite surface with the tiles
    for row in range(rows):
        for col in range(cols):
            x = col * tile_width
            y = row * tile_height
            tile_type = random.choice(tile_types)
            tile_sprite = Tile(
                x,
                y,
                tile_type=tile_type,
            )  # Assume Tile sets up tile_sprite.image and tile_sprite.rect
            # Blit the individual tile image onto the big surface
            big_tile.blit(tile_sprite.image, (x, y))

    # Create a Background object with the big tile surface
    background = Background(big_tile)

    background_group = pygame.sprite.Group()
    background_group.add(background)

    return background_group
