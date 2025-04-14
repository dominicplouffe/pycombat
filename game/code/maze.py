import pygame
import random
from config import OBJ_WIDTH, OBJ_HEIGHT, DARK_GREEN, MAZE_WIDTH, MAZE_HEIGHT
from sprite import RectSprite
from mazelib.generate.Prims import Prims
from mazelib import Maze
from game.code.objects.coin import Coin
from objects.ammo import Ammo
from objects.path import Path
from objects.wall import Wall
from objects.explosion import Explosion


class LevelMaze:
    def __init__(
        self,
        world_width=MAZE_WIDTH,
        world_height=MAZE_HEIGHT,
        seed=1240,
        game_mode="vs_bot",
    ) -> None:
        self.grid = []
        self.hit_grid = []
        self.world_height = world_height
        self.world_width = world_width
        self.game_mode = game_mode

        self.generate_maze(seed=seed)

        self.coin = self.generate_coin()
        self.coin.generate(False)

        self.has_ammo_box = False
        self.ammo_box = Ammo(self.obstacles, self.grid)

        self.has_path = False
        self.path = Path(self.obstacles, self.grid)

    def generate_maze(self, seed=0) -> pygame.sprite.Group:
        m = Maze()
        m.set_seed(seed)
        m.generator = Prims(self.world_height, self.world_width)
        m.generate()
        m.generate_entrances()
        self.grid = m.grid
        self.hit_grid = m.grid
        self.generate_sprites()

    def generate_sprites(self) -> None:
        self.obstacles, self.hit_obstacles = self.update_sprites()

    def update_sprites(self) -> None:
        obstacles = pygame.sprite.Group()
        hit_obstacles = pygame.sprite.Group()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    pos_x, pos_y = x * OBJ_WIDTH, y * OBJ_HEIGHT
                    Wall(obstacles, pos_x, pos_y)
                    obj_hit = RectSprite(
                        DARK_GREEN,
                        OBJ_WIDTH - 10,
                        OBJ_HEIGHT - 10,
                        pos_x + 5,
                        pos_y + 5,
                    )
                    hit_obstacles.add(obj_hit)

        return obstacles, hit_obstacles

    def add_obstacle(self, x: int, y: int) -> None:
        obstacles = self.obstacles.copy()
        hit_obstacles = self.hit_obstacles.copy()
        pos_x, pos_y = x * OBJ_WIDTH, y * OBJ_HEIGHT
        Wall(obstacles, pos_x, pos_y)
        obj_hit = RectSprite(
            DARK_GREEN,
            OBJ_WIDTH - 10,
            OBJ_HEIGHT - 10,
            pos_x + 5,
            pos_y + 5,
        )
        hit_obstacles.add(obj_hit)

        return obstacles, hit_obstacles

    def hit_obstacle(self, collider: pygame.sprite.Sprite) -> bool:
        for obstacle in self.hit_obstacles:
            if pygame.sprite.collide_rect(collider, obstacle):
                return True
        return False

    def bullet_hit_obstacle(self, collider: pygame.sprite.Sprite) -> bool:
        hit_obstable = None

        for o in self.hit_obstacles:
            if pygame.sprite.collide_rect(collider, o):
                y = int(o.rect.x / OBJ_HEIGHT)
                x = int(o.rect.y / OBJ_WIDTH)

                # We don't want to remove the edges of the maze
                if (
                    x > 0
                    and y > 0
                    and x < ((self.world_height * 2) - 1)
                    and y < ((self.world_width * 2) - 1)
                ):
                    hit_obstable = o
                    break

        if hit_obstable:
            obstacle_x = hit_obstable.rect.x - 5
            obstacle_y = hit_obstable.rect.y - 5
            obstacle = None

            for i, o in enumerate(self.obstacles.sprites()):
                if o.rect.x == obstacle_x and o.rect.y == obstacle_y:
                    obstacle = o
                    break

            for i, o in enumerate(self.hit_obstacles.sprites()):
                if o.rect.x == hit_obstable.rect.x and o.rect.y == hit_obstable.rect.y:
                    if obstacle:
                        self.obstacles.remove(obstacle)
                    self.hit_obstacles.remove(hit_obstable)
                    Explosion(
                        self.obstacles,
                        o.rect.center,
                    )
                    break
            return True

        return False

    def generate_coin(self) -> Coin:
        return Coin(50, self.obstacles, self.grid)

    def collide_coin(self, collider: pygame.sprite.Sprite) -> bool:
        if pygame.sprite.collide_rect(collider, self.coin):
            r = random.random()
            if r < 0.3 and self.game_mode == "vs_bot":
                power_up = random.choice([self.make_ammo_box, self.make_path])
                power_up()
            return True
        return False

    def make_ammo_box(self) -> None:
        if not self.has_ammo_box:
            self.ammo_box.generate()
            self.has_ammo_box = True

    def collide_ammo(self, collider: pygame.sprite.Sprite) -> bool:
        if pygame.sprite.collide_rect(collider, self.ammo_box):
            self.has_ammo_box = False
            self.ammo_box.kill()
            self.ammo_box = Ammo(self.obstacles, self.grid)
            return True
        return False

    def make_path(self) -> None:
        if not self.has_path:
            self.path.generate()
            self.has_path = True

    def collide_path(self, collider: pygame.sprite.Sprite) -> bool:
        if pygame.sprite.collide_rect(collider, self.path):
            self.has_path = False
            self.path.kill()
            self.path = Path(self.obstacles, self.grid)
            return True
        return False
