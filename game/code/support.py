import pygame
from os import walk
from os.path import join
from config import OBJ_WIDTH, OBJ_HEIGHT


def import_image(*path, alpha=True, format="png") -> pygame.Surface:
    full_path = join(*path) + f".{format}"
    return (
        pygame.image.load(full_path).convert_alpha()
        if alpha
        else pygame.image.load(full_path).convert()
    )


def import_folder(*path) -> list:
    frames = []
    for folder_path, subfolders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key=lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames


def import_folder_dict(*path) -> dict:
    frame_dict = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frame_dict[image_name.split(".")[0]] = surface
    return frame_dict


def import_sub_folders(*path) -> dict:
    frame_dict = {}
    for _, sub_folders, __ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict


def check_overlap(new_square, group, inflate=False) -> bool:
    if inflate:
        test_rect = new_square.rect.inflate(100, 100)
    else:
        test_rect = new_square.rect

    for sprite in group:
        if test_rect.colliderect(sprite.rect):
            return True
    return False


def find_x_y_in_grid(
    rect_x: int,
    rect_y: int,
) -> tuple[int, int]:
    x = int(rect_x / OBJ_WIDTH)
    y = int(rect_y / OBJ_HEIGHT)

    return (x, y)


# NOT USED:
def get_angle_to_mouse(image_rect, mouse_position):
    import math

    """Calculate the angle between the image's position and the mouse cursor."""
    offset_x, offset_y = (
        mouse_position[0] - image_rect.centerx,
        mouse_position[1] - image_rect.centery,
    )
    angle_rad = math.atan2(-offset_y, offset_x)
    angle_deg = (
        math.degrees(angle_rad) - 90
    )  # Adjust the angle so that 0 degrees is upwards
    return angle_deg


def angle_to_direction_vector(angle_degrees) -> tuple[float, float]:
    import math

    # Convert angle to radians
    angle_radians = math.radians(angle_degrees)

    # Calculate the x and y components
    dx = math.cos(angle_radians)
    dy = -math.sin(
        angle_radians
    )  # Negative because Pygame's y-axis is positive downward

    # Normalize the direction vector
    length = math.sqrt(dx**2 + dy**2)
    if length == 0:
        return (0, 0)  # To avoid division by zero
    normalized_dx = dx / length
    normalized_dy = dy / length

    return pygame.Vector2(normalized_dy, normalized_dx * -1)


# Get mouse position
# mouse_x, mouse_y = pygame.mouse.get_pos()

# angle = get_angle_to_mouse(self.rect, (mouse_x, mouse_y))
# self.image = pygame.transform.rotate(self.original_image, angle)
# self.rect = self.image.get_rect(center=self.rect.center)
# direction = angle_to_direction_vector(angle)
