import pygame
from config import OBJ_WIDTH, OBJ_HEIGHT, DARK_GREEN
from sprite import RectSprite
from mazelib.generate.Prims import Prims
from mazelib import Maze
from coin import Coin


class LevelMaze:
    def __init__(self, world_width=18, world_height=10, seed=1240) -> None:
        self.grid = []
        self.hit_grid = []
        self.world_height = world_height
        self.world_width = world_width

        self.obstacles, self.hit_obstacles = self.generate_maze(seed=seed)

        self.coin = self.generate_coin()
        self.coin.generate(False)

    def generate_maze(self, seed=0) -> pygame.sprite.Group:
        m = Maze()
        m.set_seed(seed)
        m.generator = Prims(self.world_height, self.world_width)
        m.generate()
        m.generate_entrances()

        self.grid = m.grid
        self.hit_grid = m.grid

        return self.update_sprites()

    def update_sprites(self) -> None:
        obstacles = pygame.sprite.Group()
        hit_obstacles = pygame.sprite.Group()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    pos_x, pos_y = x * OBJ_WIDTH, y * OBJ_HEIGHT
                    obj_rect = RectSprite(
                        DARK_GREEN, OBJ_WIDTH, OBJ_HEIGHT, pos_x, pos_y
                    )
                    obj_hit = RectSprite(
                        DARK_GREEN,
                        OBJ_WIDTH - 10,
                        OBJ_HEIGHT - 10,
                        pos_x + 5,
                        pos_y + 5,
                    )
                    obstacles.add(obj_rect)
                    hit_obstacles.add(obj_hit)

        return obstacles, hit_obstacles

    def hit_obstacle(self, collider: pygame.sprite.Sprite) -> bool:
        for obstacle in self.hit_obstacles:
            if pygame.sprite.collide_rect(collider, obstacle):
                return True
        return False

    def bullet_hit_obstacle(self, collider: pygame.sprite.Sprite) -> bool:
        for obstacle in self.hit_obstacles:
            if pygame.sprite.collide_rect(collider, obstacle):
                y = int(obstacle.rect.x / OBJ_HEIGHT)
                x = int(obstacle.rect.y / OBJ_WIDTH)

                # We don't want to remove the edges of the maze
                if (
                    x > 0
                    and y > 0
                    and x < ((self.world_height * 2) - 1)
                    and y < ((self.world_width * 2) - 1)
                ):
                    self.grid[x][y] = 0
                    self.obstacles, self.hit_obstacles = self.update_sprites()
                return True
        return False

    def generate_coin(self) -> Coin:
        return Coin(50, self.obstacles, self.grid)

    def collide_coin(self, collider: pygame.sprite.Sprite) -> bool:
        if pygame.sprite.collide_rect(collider, self.coin):
            return True
        return False
