import math
import random
from MazeNode import MazeNode


class MazeSolver:
    """
    Solves a maze by navigating from a starting position to an end position.
    """
    def __init__(self, i_maze: list[list[MazeNode]], start_pos=(0, 0), end_pos=(10, 10)):
        """
        Initializes the maze solver with a maze layout, start position, and end position.

        Args:
            i_maze (list[list[MazeNode]]): The maze represented as a grid of MazeNode objects.
            start_pos (tuple): Starting position in the maze (default (0, 0)).
            end_pos (tuple): Ending position in the maze (default (10, 10)).
        """
        self.maze = i_maze
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.__current_pos = start_pos
        self.__path = [start_pos]
        self.__blocked = []

    def next_step(self):
        """
        Advances to the next step in the maze by exploring adjacent nodes from the current position.

        This method uses a greedy approach, selecting the nearest from end unvisited node that does not lead back to the start position.

        If no such node is found, the solver will backtrack and try another path.
        """
        if self.has_next:
            x, y = self.__current_pos
            current_node = self.maze[x][y]
            nodes: list = [current_node.top, current_node.bottom, current_node.left, current_node.right]
            nodes = sorted([node for node in nodes if node[0] is not None], key=self.get_distance)

            for node in nodes:
                if self.check_node(node[0], node[1]):
                    self.__path.append(node[0].pos)
                    self.__current_pos = node[0].pos
                    return

            self.__blocked.append(self.__current_pos)
            self.__path.pop()
            self.__current_pos = self.__path[-1]

    def check_node(self, node: MazeNode, has_wall: bool):
        """
        Checks if a node is traversable and not yet visited.

        Args:
            node (MazeNode): The node to check.
            has_wall (bool): Indicates if the path to this node is blocked by a wall.

        Returns:
            bool: True if the node is open for traversal, False otherwise.
        """
        return node and not has_wall and node.pos not in self.__path and node.pos not in self.__blocked

    @property
    def path(self):
        """
        Returns the path taken through the maze.

        Returns:
            list: List of positions visited in the maze.
        """
        return self.__path

    @property
    def has_next(self):
        """
        Indicates if there are remaining steps to reach the end position.

        Returns:
            bool: True if the current position is not the end position, False otherwise.
        """
        return self.__current_pos != self.end_pos

    def get_distance(self, node: tuple[MazeNode, bool]):
        x1, y1 = self.end_pos
        x2, y2 = node[0].pos
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

