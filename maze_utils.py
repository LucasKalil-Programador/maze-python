import cv2
import numpy as np

from MazeNode import MazeNode
from MazeSolver import MazeSolver


def maze_foreach(maze: MazeNode) -> tuple[tuple[int, int], MazeNode]:
    """
    Iterates over a maze and yields the position and node at each intersection.

    Args:
        maze (MazeNode): The maze to iterate over.

    Yields:
        tuple[tuple[int, int], MazeNode]: A tuple containing the position (x, y) and node.
    """
    for x, line in enumerate(maze):
        for y, node in enumerate(line):
            yield (x, y), node


def new_maze(maze_height, maze_width):
    """
    Creates a new maze with the specified height and width.

    Args:
        maze_height (int): The height of the maze.
        maze_width (int): The width of the maze.

    Returns:
        list[list[MazeNode]]: A 2D list representing the maze, where each element is a MazeNode object.
    """
    n_maze = [[MazeNode(pos=(x, y)) for y in range(maze_height)] for x in range(maze_width)]
    for x, line in enumerate(n_maze):
        for y, node in enumerate(line):
            if y > 0:
                n_maze[x][y].top = (n_maze[x][y - 1], True)
            if y + 1 < maze_height:
                n_maze[x][y].bottom = (n_maze[x][y + 1], True)
            if x > 0:
                n_maze[x][y].left = (n_maze[x - 1][y], True)
            if x + 1 < maze_width:
                n_maze[x][y].right = (n_maze[x + 1][y], True)
    return n_maze


def draw_maze(maze_input: list[list[MazeNode]], last_frame=None, redraw_list=None, width=50, height=50, border_thickness=5, cursor_pos=None,
              cursor_color=(255, 255, 255), border_color=(0, 0, 0), bg_color=(50, 50, 50), node_color=(50, 50, 50)):
    """
    Draws the maze on a frame using OpenCV.

    Args:
        maze_input (list[list[MazeNode]]): The maze to draw.
        last_frame (numpy.ndarray, optional): The previous frame. Defaults to None.
        redraw_list (list[tuple[int, int]], optional): A list of positions to redraw in the current frame. Defaults to None.
        width (int, optional): The width of each node in the grid. Defaults to 50.
        height (int, optional): The height of each node in the grid. Defaults to 50.
        border_thickness (int, optional): The thickness of the border between nodes. Defaults to 5.
        cursor_pos (tuple[int, int], optional): The position of the cursor. Defaults to None.
        cursor_color (tuple[int, int, int], optional): The color of the cursor. Defaults to white.
        border_color (tuple[int, int, int], optional): The color of the borders. Defaults to black.
        bg_color (tuple[int, int, int], optional): The background color of the frame. Defaults to dark gray.
        node_color (tuple[int, int, int], optional): The color of the nodes. Defaults to dark gray.

    Returns:
        numpy.ndarray: The drawn maze on a frame.
    """
    if last_frame is None:
        maze_img = np.full((height * len(maze_input[0]), width * len(maze_input), 3), bg_color, dtype=np.uint8)
    else:
        maze_img = last_frame

    if redraw_list is None:
        for x, line in enumerate(maze_input):
            for y, node in enumerate(line):
                render_node(border_color, border_thickness, cursor_color, node_color, cursor_pos, height, maze_img, node, width, x, y)
    else:
        for node_pos in redraw_list:
            node = maze_input[node_pos[0]][node_pos[1]]
            render_node(border_color, border_thickness, cursor_color, node_color, cursor_pos, height, maze_img, node, width, node_pos[0], node_pos[1])
    return maze_img


def render_node(border_color, border_thickness, cursor_color, node_color, cursor_pos, height, maze_img, node, width, x, y):
    """
    Renders a single node in the maze on the given image.

    Args:
        border_color (tuple[int, int, int]): The color of the borders.
        border_thickness (int): The thickness of the borders.
        cursor_color (tuple[int, int, int]): The color of the cursor.
        node_color (tuple[int, int, int]): The color of the node.
        cursor_pos (tuple[int, int], optional): The position of the cursor. Defaults to None.
        height (int): The height of each node in the grid.
        maze_img (numpy.ndarray): The image to render on.
        node (MazeNode): The node to render.
        width (int): The width of each node in the grid.
        x (int): The x-coordinate of the node.
        y (int): The y-coordinate of the node.
    """
    pos_x, pos_y = x * width, y * height
    top_left = (pos_x, pos_y)
    top_right = (pos_x + width, pos_y)
    bottom_left = (pos_x, pos_y + height)
    bottom_right = (pos_x + width, pos_y + height)

    color = cursor_color if (x, y) == cursor_pos else node_color
    cv2.rectangle(maze_img, top_left, bottom_right, color=color, thickness=-1)

    if node.left[1]:
        cv2.line(maze_img, top_left, bottom_left, color=border_color, thickness=border_thickness)
    if node.top[1]:
        cv2.line(maze_img, top_left, top_right, color=border_color, thickness=border_thickness)
    if node.right[1]:
        cv2.line(maze_img, top_right, bottom_right, color=border_color, thickness=border_thickness)
    if node.bottom[1]:
        cv2.line(maze_img, bottom_left, bottom_right, color=border_color, thickness=border_thickness)


def draw_path(frame, color, maze_solver: MazeSolver):
    """
    Draws the paths of multiple maze solvers on the given frame.

    Args:
        frame (numpy.ndarray): The image to draw on.
        color (tuple(int,int,int)) a color of path
        maze_solver (list[MazeSolver]): A maze solver to draw paths for.
    """
    solve_points = maze_solver.path
    cv2.circle(frame, (9, 9), 5, (255, 255, 255), lineType=cv2.LINE_AA, thickness=-1)
    cv2.circle(frame, (9 + 18 * 49, 9 + 18 * 49), 5, (255, 255, 255), lineType=cv2.LINE_AA, thickness=-1)
    for i in range(len(solve_points)):
        if i < len(solve_points) - 1:
            pt1 = (9 + 18 * solve_points[i][0], 9 + 18 * solve_points[i][1])
            pt2 = (9 + 18 * solve_points[i + 1][0], 9 + 18 * solve_points[i + 1][1])
            cv2.line(frame, pt1, pt2, color, lineType=cv2.LINE_AA, thickness=2)
