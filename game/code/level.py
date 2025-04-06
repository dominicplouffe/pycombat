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
    MOSS_GREEN,
    BOT_DIFFICULTY,
    RANKS,
)

from player import Player
from maze import LevelMaze
from sprite import RectSprite
from player_stats import PlayerStats
from power_ups import PowerUpChoices


class Level:
    def __init__(
        self,
        display_level_done: callable,
        player_stats: PlayerStats,
        level_number: int = 1,
        seed: int = 0,
    ) -> None:
        self.maze = LevelMaze(seed=seed)
        self.level_number = level_number
        self.seed = seed

        self.display_surface = pygame.display.get_surface()
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.bullets = pygame.sprite.Group()
        self.path = pygame.sprite.Group()
        self.player_stats = player_stats

        self.all_sprites = pygame.sprite.Group(
            *self.maze.obstacles,
            self.maze.hit_obstacles,
            self.maze.coin,
            self.bullets,
            self.path,
        )
        self.player = Player(
            self.all_sprites,
            self.maze,
            player_stats,
            is_bot=False,
            bullets=self.bullets,
            all_sprites=self.all_sprites,
            collect_coin_callback=self.collect_coin,
        )
        self.bot = Player(
            self.all_sprites,
            self.maze,
            player_stats,
            is_bot=True,
            bullets=self.bullets,
            all_sprites=self.all_sprites,
            collect_coin_callback=self.collect_coin,
            speed=BOT_DIFFICULTY[level_number],
        )

        self.draw_path()
        self.dt_sum = 0
        self.display_level_done = display_level_done

    def update(self, dt, event) -> None:
        if self.has_path_power_up() and len(self.path) == 0:
            self.player.compute_path()
            self.draw_path()

        if not self.has_path_power_up() and len(self.path) > 0:
            self.path = []

        if self.has_ice_power_up():
            self.bot.set_speed(BOT_DIFFICULTY[1])
        else:
            self.bot.set_speed(BOT_DIFFICULTY[self.level_number])

        self.all_sprites = pygame.sprite.Group(
            *self.maze.hit_obstacles,
            self.maze.obstacles,
            self.path,
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

        # Coins Text
        coins_text = font.render(
            f"Coins: {self.player.coins} - Bot: {self.bot.coins}", True, BLACK
        )
        coins_rect = coins_text.get_rect()
        coins_rect.topleft = (10, 13)

        level_text = font.render(f"Level: {self.level_number:.0f}", True, BLACK)
        level_rect = level_text.get_rect()
        level_rect.topleft = (220, 13)

        seed_text = font.render(f"Seed: {self.seed}", True, BLACK)
        seed_rect = seed_text.get_rect()
        seed_rect.topleft = (340, 13)

        rank_text = font.render(f"Rank: {RANKS[self.level_number]}", True, BLACK)
        rank_rect = rank_text.get_rect()
        rank_rect.topleft = (500, 13)

        # Draw background boxes with blue borders
        padding = 8
        box_color = WHITE
        border_color = BLACK

        # Draw the box for the coins
        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                coins_rect.x - padding,
                coins_rect.y - padding,
                coins_rect.width + 2 * padding,
                coins_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                coins_rect.x - padding + 2,
                coins_rect.y - padding + 2,
                coins_rect.width + 2 * (padding - 2),
                coins_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(coins_text, coins_rect)

        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                level_rect.x - padding,
                level_rect.y - padding,
                level_rect.width + 2 * padding,
                level_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                level_rect.x - padding + 2,
                level_rect.y - padding + 2,
                level_rect.width + 2 * (padding - 2),
                level_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(level_text, level_rect)

        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                rank_rect.x - padding,
                rank_rect.y - padding,
                rank_rect.width + 2 * padding,
                rank_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                rank_rect.x - padding + 2,
                rank_rect.y - padding + 2,
                rank_rect.width + 2 * (padding - 2),
                rank_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(rank_text, rank_rect)

        pygame.draw.rect(
            self.display_surface,
            border_color,
            (
                seed_rect.x - padding,
                seed_rect.y - padding,
                seed_rect.width + 2 * padding,
                seed_rect.height + 2 * padding,
            ),
            2,  # Border thickness
        )
        pygame.draw.rect(
            self.display_surface,
            box_color,
            (
                seed_rect.x - padding + 2,
                seed_rect.y - padding + 2,
                seed_rect.width + 2 * (padding - 2),
                seed_rect.height + 2 * (padding - 2),
            ),
        )
        self.display_surface.blit(seed_text, seed_rect)

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

        self.player.compute_path()
        self.draw_path()

        if self.bot:
            self.bot.compute_path()

        if not is_bot:
            self.player_stats.add_coins(1)
            self.player.increment_coins()
        else:
            self.bot.increment_coins()

        if self.player.coins >= 5:
            self.display_level_done(True)
        elif self.bot.coins >= 5:
            self.display_level_done(False)

    def draw_path(self) -> None:
        self.path = pygame.sprite.Group()
        if not self.has_path_power_up():
            return

        for row, col in self.player.path:
            pos_x, pos_y = col * OBJ_WIDTH, row * OBJ_HEIGHT

            path_rect = RectSprite(
                MOSS_GREEN,
                OBJ_WIDTH // 4,
                OBJ_HEIGHT // 4,
                pos_x + (OBJ_WIDTH // 2 - OBJ_WIDTH // 8),
                pos_y + (OBJ_HEIGHT // 2 - OBJ_HEIGHT // 8),
            )
            # check if path_rect collides with self.maze.obstacles
            for obstacle in self.maze.obstacles:
                if path_rect.rect.colliderect(obstacle.rect):
                    path_rect.kill()
                    break
            else:
                # If no collision, add the path_rect to the path_group
                self.path.add(path_rect)

    def has_path_power_up(self) -> bool:
        return self.player_stats.power_ups.has_power_up(
            PowerUpChoices.PATH
        ) or self.player_stats.power_ups.has_power_up(PowerUpChoices.PATH_PLUS)

    def has_ice_power_up(self) -> bool:
        return self.player_stats.power_ups.has_power_up(
            PowerUpChoices.ICE
        ) or self.player_stats.power_ups.has_power_up(PowerUpChoices.ICE_PLUS)
