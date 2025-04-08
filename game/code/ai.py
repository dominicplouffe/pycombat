from pygame import Vector2 as vector
from collections import deque
import random
import time


def find_path(grid, start, goal) -> list | None:
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        # Check if we've reached the goal
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            # Check bounds and if the cell is open (0)
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == 0
                and neighbor not in visited
            ):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return None  # No path found


def find_goal(intel_level, grid, correct_goal):
    random_goals = {
        1: 0.80,
        2: 0.70,
        3: 0.60,
        4: 0.50,
        5: 0.40,
        6: 0.30,
        7: 0.20,
        8: 0.10,
        9: 0.05,
    }

    random.seed(int(time.time()))
    if intel_level == 0:
        return correct_goal

    if intel_level in random_goals:
        r = random.random()
        if r < random_goals[intel_level]:
            return correct_goal

    random.seed(0)
    goal = random_goal(grid)

    return goal


def random_goal(grid) -> tuple:
    """Generate a random goal position on the grid."""
    rows, cols = len(grid), len(grid[0])

    new_goal = (0, 0)
    while True:
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        if grid[x][y] == 0:  # Check if the cell is open (0)
            new_goal = (x, y)
            break

    return new_goal


def find_direction(
    current_x: int,
    current_y: int,
    target_x: int,
    target_y: int,
) -> vector:
    """Find the direction to move towards the target coordinates."""
    if current_x < target_x:
        x_direction = 1
    elif current_x > target_x:
        x_direction = -1
    else:
        x_direction = 0

    if current_y < target_y:
        y_direction = 1
    elif current_y > target_y:
        y_direction = -1
    else:
        y_direction = 0

    return vector(x_direction, y_direction)
