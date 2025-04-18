import pygame

OBJ_WIDTH = 70
OBJ_HEIGHT = 70

MAZE_WIDTH = 18
MAZE_HEIGHT = 10

WINDOW_WIDTH = 1330
WINDOW_HEIGHT = 770

WORLD_WIDTH = ((MAZE_WIDTH * 2) + 1) * OBJ_WIDTH
WORLD_HEIGHT = ((MAZE_HEIGHT * 2) + 1) * OBJ_HEIGHT

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
CHERRY_RED = (205, 0, 26)
SAND = (237, 201, 175)
BEIGE = (255, 245, 220)
MOSS_GREEN = (86, 112, 68)

BUTTON_BACKGROUND = (24, 22, 21)
BUTTON_BORDER = (146, 122, 40)
BUTTON_TEXT = (239, 171, 104)
LABEL_COLOR = (239, 171, 104)
RECT_BACKGROUND = (24, 22, 21)

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
