import random
import time


class MazeGenerator:
    def __init__(self, i_maze, cursor_pos=(0, 0), step_to_next_random=1):
        """
        Initializes the maze generator with a maze layout and starting position.

        Args:
            i_maze (list): The maze represented as a grid of nodes.
            cursor_pos (tuple): Starting position in the maze (default (0, 0)).
            step_to_next_random (int): Time step to increment for randomization (default 1).
        """
        self.__visited = [cursor_pos]
        self.cursor_pos = cursor_pos
        self.__remain_pos = []
        self.maze = i_maze
        self.__first = True

        self.__step_counter = 0
        self.__random = time.time_ns()
        self.step_to_next_random = step_to_next_random

    def get_possible_moves(self, root_node):
        """
        Returns all unvisited nodes that can be moved from the given node.

        Args:
            root_node: Node in the maze that is being evaluated.

        Returns:
            list: List of possible moves.
        """
        possible_moves = []
        for node, wall in root_node:
            if node and node.pos not in self.__visited:
                possible_moves.append(node)
        return possible_moves

    def __random_control(self):
        """
            Increments the random seed and resets the step counter if necessary.
        """
        if self.__step_counter >= self.step_to_next_random:
            self.__random = self.__random + 1
            self.__step_counter = 0
        random.seed(self.__random)
        self.__step_counter += 1

    def next_step(self, pop_first=False):
        """
        Takes a step in the maze by randomly choosing an unvisited neighbor.

        Args:
            pop_first (bool): Whether to remove the current position from the remain positions list if it's empty. Default False.
        """
        x, y = self.cursor_pos
        root_node = self.maze[x][y]
        possible_moves = self.get_possible_moves(root_node)
        self.__random_control()

        if len(possible_moves) > 0:
            next_node = random.choice(possible_moves)
            self.__visited.append(next_node.pos)

            if len(possible_moves) > 1:
                self.__remain_pos.append(self.cursor_pos)

            self.cursor_pos = next_node.pos
            if root_node.top[0] == next_node:
                root_node.top = (root_node.top[0], False)
            elif root_node.bottom[0] == next_node:
                root_node.bottom = (root_node.bottom[0], False)
            elif root_node.right[0] == next_node:
                root_node.right = (root_node.right[0], False)
            elif root_node.left[0] == next_node:
                root_node.left = (root_node.left[0], False)
        else:
            while len(self.__remain_pos) > 0:
                x, y = self.cursor_pos = self.__remain_pos.pop(0 if pop_first else -1)
                if len(self.get_possible_moves(self.maze[x][y])) > 0:
                    break

        self.__first = False

    def run(self):
        """
            Runs the maze generator algorithm until all reachable nodes have been visited.
        """
        while self.has_next:
            self.next_step()

    @property
    def remain_count(self):
        """
        Returns the number of remaining unvisited nodes in the maze.

        Returns:
            int: Number of remaining nodes.
        """
        return len(self.__remain_pos)

    @property
    def visited_count(self):
        """
        Returns the number of visited nodes in the maze.

        Returns:
            int: Number of visited nodes.
        """
        return len(self.__visited)

    @property
    def visited(self):
        """
        Returns a list of all visited node positions in the maze.

        Returns:
            list: List of visited positions.
        """
        return self.__visited

    @property
    def has_next(self):
        """
        Indicates whether there are remaining nodes to be visited in the maze.

        Returns:
            bool: True if there are remaining nodes, False otherwise.
        """
        return len(self.__remain_pos) > 0 or self.__first
