from pygame import Vector2 as vector
from collections import deque


def find_path(grid, start, goal):
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


def dfs(maze, start, goal) -> list | None:
    rows, cols = len(maze), len(maze[0])
    stack = [start]  # Use a list as a stack
    visited = set([start])  # Track visited nodes
    parent = {start: None}  # Track path

    while stack:
        current = stack.pop()  # Get the last inserted node (LIFO)

        # Check if we reached the goal
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return the path from start to goal

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            # Check if the neighbor is within bounds and open (0)
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 0
                and neighbor not in visited
            ):
                stack.append(neighbor)  # Add to stack
                visited.add(neighbor)  # Mark as visited
                parent[neighbor] = current  # Track the path

    return None  # Re


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
