from typing import Any


class MazeNode:

    """
    Represents a node in a maze, with properties for its position, neighbors, and walls.
    """

    def __init__(self, neighbors=None, walls=None, pos=(0, 0)):
        """
        Initializes a new MazeNode with the given position and optional neighbors/walls.

        Args:
            neighbors (list): A list of boolean values indicating whether each neighbor is present.
            walls (list): A list of boolean values indicating whether each wall is present.
            pos (tuple): The node's position in the maze, defaulting to (0, 0).

        Note:
            If no neighbors or walls are provided, they will be initialized with default values.
        """
        if walls is None:
            walls = [True, True, True, True]

        if neighbors is None:
            neighbors = [None, None, None, None]

        self.pos = pos
        self.neighbors = neighbors
        self.walls = walls

    def __iter__(self):
        """
        Returns an iterator over the node's neighbors and corresponding wall status.

        Yields:
            tuple: A pair containing a neighbor and its wall status.
        """
        return iter(zip(self.neighbors, self.walls))

    def __str__(self):
        """
        Returns a string representation of the node, including its position and neighbor/wall information.

        Returns:
            str: A formatted string describing the node's properties.
        """
        directions = ["Left", "Top", "Right", "bottom"]
        output = [f"Pos={self.pos}"]
        for i, (neighbor, wall) in enumerate(zip(self.neighbors, self.walls)):
            output.append(
                f"{directions[i]}: Neighbor={neighbor.pos if neighbor else 'None'}, Wall={'Yes' if wall else 'No'}")
        return "\n".join(output)

    @property
    def left(self):
        """
        Gets the node's left neighbor and its corresponding wall status.

        Returns:
            tuple: A pair containing a neighbor and its wall status.
        """
        return self.neighbors[0], self.walls[0]

    @left.setter
    def left(self, new_neighbor: tuple[Any, bool]):
        """
        Sets the node's left neighbor and its corresponding wall status to the provided values.

        Args:
            new_neighbor (tuple): A pair containing a new neighbor and its wall status.
        """
        new_neighbor[0].neighbors[2], new_neighbor[0].walls[2] = self, new_neighbor[1]
        self.neighbors[0], self.walls[0] = new_neighbor[0], new_neighbor[1]

    @property
    def top(self):
        """
        Gets the node's top neighbor and its corresponding wall status.

        Returns:
            tuple: A pair containing a neighbor and its wall status.
        """
        return self.neighbors[1], self.walls[1]

    @top.setter
    def top(self, new_neighbor: tuple[Any, bool]):
        """
        Sets the node's top neighbor and its corresponding wall status to the provided values.

        Args:
            new_neighbor (tuple): A pair containing a new neighbor and its wall status.
        """
        new_neighbor[0].neighbors[3], new_neighbor[0].walls[3] = self, new_neighbor[1]
        self.neighbors[1], self.walls[1] = new_neighbor[0], new_neighbor[1]

    @property
    def right(self):
        """
        Gets the node's right neighbor and its corresponding wall status.

        Returns:
            tuple: A pair containing a neighbor and its wall status.
        """
        return self.neighbors[2], self.walls[2]

    @right.setter
    def right(self, new_neighbor: tuple[Any, bool]):
        """
        Sets the node's right neighbor and its corresponding wall status to the provided values.

        Args:
            new_neighbor (tuple): A pair containing a new neighbor and its wall status.
        """
        new_neighbor[0].neighbors[0], new_neighbor[0].walls[0] = self, new_neighbor[1]
        self.neighbors[2], self.walls[2] = new_neighbor[0], new_neighbor[1]

    @property
    def bottom(self):
        """
        Gets the node's bottom neighbor and its corresponding wall status.

        Returns:
            tuple: A pair containing a neighbor and its wall status.
        """
        return self.neighbors[3], self.walls[3]

    @bottom.setter
    def bottom(self, new_neighbor: tuple[Any, bool]):
        """
        Sets the node's bottom neighbor and its corresponding wall status to the provided values.

        Args:
            new_neighbor (tuple): A pair containing a new neighbor and its wall status.
        """
        new_neighbor[0].neighbors[1], new_neighbor[0].walls[1] = self, new_neighbor[1]
        self.neighbors[3], self.walls[3] = new_neighbor[0], new_neighbor[1]
