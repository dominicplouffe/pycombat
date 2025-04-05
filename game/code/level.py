import math
import pygame
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DARK_GREEN,
    OBJ_WIDTH,
    OBJ_HEIGHT,
    RED,
    WHITE,
    BLACK,
)

from player import Player
from maze import LevelMaze


BOT_DIFFICULTY = {
    1: 170,
    2: 200,
    3: 230,
    4: 260,
    5: 290,
    6: 320,
    7: 350,
    8: 380,
    9: 410,
    10: 440,
}


class Level:
    def __init__(
        self,
        display_level_done: callable,
        level_number: int = 1,
    ) -> None:
        self.maze = LevelMaze()
        self.level_number = level_number

        self.display_surface = pygame.display.get_surface()
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.bullets = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group(
            *self.maze.obstacles, self.maze.hit_obstacles, self.maze.coin, self.bullets
        )
        self.player = Player(
            self.all_sprites,
            self.maze,
            is_bot=False,
            bullets=self.bullets,
            all_sprites=self.all_sprites,
            collect_coin_callback=self.collect_coin,
        )
        self.bot = Player(
            self.all_sprites,
            self.maze,
            is_bot=True,
            bullets=self.bullets,
            all_sprites=self.all_sprites,
            collect_coin_callback=self.collect_coin,
            speed=BOT_DIFFICULTY[level_number],
        )

        self.dt_sum = 0
        self.display_level_done = display_level_done

    def update(self, dt, event) -> None:
        self.all_sprites = pygame.sprite.Group(
            *self.maze.hit_obstacles,
            self.maze.obstacles,
            self.maze.coin,
            self.bullets,
            self.player,
        )
        if self.bot:
            self.all_sprites.add(self.bot)

        self.world.fill(DARK_GREEN)
        self.all_sprites.update(dt, event)
        self.all_sprites.draw(self.world)
        self.draw_viewport()

        self.dt_sum += dt
        self.draw_ui()

        self.draw_arrow_in_circle()

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

    def draw_ui(self) -> None:
        font = pygame.font.Font(None, 36)

        # Score Text
        score_text = font.render(
            f"Score: {self.player.score} - Bot: {self.bot.score}", True, BLACK
        )
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 13)

        distance_text = font.render(f"Level: {self.level_number:.0f}", True, BLACK)
        distance_rect = distance_text.get_rect()
        distance_rect.topleft = (220, 13)

        # Draw background boxes with blue borders
        padding = 8
        box_color = WHITE
        border_color = BLACK

        # Draw the box for the score
        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                score_rect.x - padding,
                score_rect.y - padding,
                score_rect.width + 2 * padding,
                score_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                score_rect.x - padding + 2,
                score_rect.y - padding + 2,
                score_rect.width + 2 * (padding - 2),
                score_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(score_text, score_rect)

        # Draw the box for the distance
        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                distance_rect.x - padding,
                distance_rect.y - padding,
                distance_rect.width + 2 * padding,
                distance_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                distance_rect.x - padding + 2,
                distance_rect.y - padding + 2,
                distance_rect.width + 2 * (padding - 2),
                distance_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(distance_text, distance_rect)

    def calculate_angle(self, x1, y1, x2, y2) -> float:
        # Calculate the difference in coordinates
        delta_x = x2 - x1
        delta_y = y2 - y1

        # Get the angle in radians and convert to degrees
        angle = math.degrees(
            math.atan2(-delta_y, delta_x)
        )  # Negative delta_y for pygame's coordinate system
        angle = (angle + 360) % 360  # Normalize to 0-360 degrees

        return angle

    def draw_arrow_in_circle(self) -> None:
        coin_player_angle = self.calculate_angle(
            self.player.rect.x,
            self.player.rect.y,
            self.maze.coin.rect.x,
            self.maze.coin.rect.y,
        )

        circle_radius = 50
        circle_center = (
            WINDOW_WIDTH - circle_radius - 10,
            WINDOW_HEIGHT - circle_radius - 10,
        )

        # Calculate arrow endpoints based on angle
        arrow_length = (
            circle_radius - 10
        )  # Shorter than the radius to stay inside the circle
        x_end = circle_center[0] + arrow_length * math.cos(
            math.radians(coin_player_angle)
        )
        y_end = circle_center[1] - arrow_length * math.sin(
            math.radians(coin_player_angle)
        )

        # Draw blue circle
        pygame.draw.circle(self.display_surface, WHITE, circle_center, circle_radius)

        # Draw arrow pointing outward from the center
        pygame.draw.line(self.display_surface, RED, circle_center, (x_end, y_end), 3)

        # Arrowhead wings pointing outward
        arrowhead_length = 10
        left_wing = (
            x_end + arrowhead_length * math.cos(math.radians(coin_player_angle - 150)),
            y_end - arrowhead_length * math.sin(math.radians(coin_player_angle - 150)),
        )
        right_wing = (
            x_end + arrowhead_length * math.cos(math.radians(coin_player_angle + 150)),
            y_end - arrowhead_length * math.sin(math.radians(coin_player_angle + 150)),
        )

        pygame.draw.line(self.display_surface, RED, (x_end, y_end), left_wing, 3)
        pygame.draw.line(self.display_surface, RED, (x_end, y_end), right_wing, 3)

    def collect_coin(self, is_bot: bool) -> None:
        self.maze.coin.generate(True)
        if self.bot:
            self.bot.compute_path()

        if not is_bot:
            self.player.increment_score()
        else:
            self.bot.increment_score()

        if self.player.score >= 5:
            self.display_level_done(True)
        elif self.bot.score >= 5:
            self.display_level_done(False)
