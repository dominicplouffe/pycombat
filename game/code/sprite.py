import pygame


class RectSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        if color:
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class CollideSprite(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect


class RoundedSprite(pygame.sprite.Sprite):
    def __init__(self, color, border_color, width, height, x, y, border=5, radius=10):
        super().__init__()
        self.image = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )  # Use SRCALPHA to support transparency
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.border_color = border_color
        self.border = border
        self.radius = radius
        self.width = width
        self.height = height
        self._draw_rounded()

    def _draw_rounded(self):
        # Draw the border rectangle with rounded edges
        pygame.draw.rect(
            self.image,
            self.border_color,
            (0, 0, self.width, self.height),
            border_radius=self.radius,
        )
        # Draw the inner rectangle with rounded edges, slightly smaller to create the border effect
        inner_rect = pygame.Rect(
            self.border,
            self.border,
            self.width - 2 * self.border,
            self.height - 2 * self.border,
        )
        pygame.draw.rect(
            self.image, self.color, inner_rect, border_radius=self.radius - self.border
        )
