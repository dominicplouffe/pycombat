import pygame

WINDOW_WIDTH = 1330
WINDOW_HEIGHT = 770
WORLD_WIDTH = 2660
WORLD_HEIGHT = 1440

ANIMATION_SPEED = 6
WHITE = (255, 255, 255)
DARK_BROWN = (96, 68, 57)  # Ground
DARK_GREEN = (65, 83, 59)  # Grass
KHAKI = (158, 154, 117)  # Paths
DARK_BLUE = (28, 34, 46)  # Water
OBSTACLE = pygame.Color("#9E9E9E")  # Obstacles
GOLD = (255, 223, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SAND = (237, 201, 175)
BEIGE = (255, 245, 220)
MOSS_GREEN = (126, 140, 84)

OBJ_WIDTH = 70
OBJ_HEIGHT = 70

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

RANKS = {
    1: "Private",
    2: "Private First Class",
    3: "Specialist",
    4: "Sergeant",
    5: "Staff Sergeant",
    6: "Sergeant First Class",
    7: "Second Lieutenant",
    8: "Captain",
    9: "Lieutenant Colonel",
    10: "General",
}
