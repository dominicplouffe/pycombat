import pygame
from support import import_image


class Powerup:
    def __init__(
        self,
        display_surface: pygame.Surface,
        x: int,
        y: int,
        powerup_type: str,
        value: int,
    ) -> None:
        self.display_surface = display_surface
        # Create a white rectangle with a black border or 40 x 40
        self.image = pygame.Surface((40, 42))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 2)

        if powerup_type == "bullet":
            self.power_image = import_image(
                "game", "support", "images", "bullet", "bullet_small"
            )
            # 1dd self.power_image to the image
            self.image.blit(
                self.power_image, (20 - (self.power_image.get_width() // 2), 7)
            )
        elif powerup_type == "path":
            self.power_image = import_image(
                "game", "support", "images", "path", "path_small"
            )
            # Resize the image to 20 x 20
            self.power_image = pygame.transform.scale(self.power_image, (10, 10))
            self.image.blit(
                self.power_image, (20 - (self.power_image.get_width() // 2), 7)
            )

        # Draw black text with the value
        font = pygame.font.Font(None, 25)
        text_surface = font.render(str(value), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(20, 30))
        self.image.blit(text_surface, text_rect)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.powerup_type = powerup_type
        self.value = value

        self.display_surface.blit(self.image, self.rect)
