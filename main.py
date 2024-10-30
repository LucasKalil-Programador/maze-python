import time

import cv2

from MazeGenerator import MazeGenerator
from MazeSolver import MazeSolver
from maze_utils import new_maze, draw_maze, draw_path


def render_loop(maze, maze_gen: MazeGenerator, maze_solver: MazeSolver, maze_height, maze_width, window_name="Maze"):
    """
    Main rendering loop for the maze generation and solving process.

    Args:
        maze (list): The generated maze.
        maze_gen (MazeGenerator): The current state of the maze generation process.
        maze_solver (MazeSolver): A active maze solvers.
        maze_height (int): The height of the maze.
        maze_width (int): The width of the maze.
        window_name (str, optional): The name of the window to display the maze. Defaults to "Maze".
    """
    continue_loop = True
    target_frame_time = 1
    maze_img = None

    while continue_loop:
        redraw_list = [(0, 0)]
        cursor_pos = None
        start_time = time.time() * 1000

        if maze_gen.has_next:
            redraw_list.append(maze_gen.cursor_pos)
            maze_gen.next_step()
            redraw_list.append(maze_gen.cursor_pos)
            cursor_pos = maze_gen.cursor_pos
        elif maze_solver.has_next:
            maze_solver.next_step()
        else:
            continue_loop = False

        # draw maze
        maze_img = draw_maze(
            maze, last_frame=maze_img,
            redraw_list=redraw_list,
            width=18, height=18, border_thickness=1, cursor_pos=cursor_pos,
            bg_color=(0, 0, 0), node_color=(50, 50, 50))

        frame = maze_img.copy()

        # draw maze solve
        if not maze_gen.has_next:
            draw_path(frame, (0, 0, 255), maze_solver)

        end_time = time.time() * 1000
        status1 = f"solve path length: {len(maze_solver.path)}"
        status2 = f"remain: {maze_gen.remain_count} progress: {(maze_gen.visited_count / (maze_height * maze_width)) * 100:0.2f}% draw time: {end_time - start_time:0.2f} ms"

        cv2.putText(frame, status1, (10, 870), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, status2, (10, 890), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, lineType=cv2.LINE_AA)
        cv2.imshow(window_name, frame)

        end_time = time.time() * 1000
        delay = int(max(target_frame_time - (end_time - start_time), 1))
        cv2.waitKey(delay)

    cv2.waitKey(1000)
    cv2.destroyAllWindows()


def main(run_count):
    """
    Main entry point for the program.

    Args:
        run_count (int): The number of runs to perform.
    """
    maze_height, maze_width = 50, 50
    maze = new_maze(maze_height, maze_width)
    maze_gen = MazeGenerator(maze, step_to_next_random=run_count)
    maze_solver = MazeSolver(maze, end_pos=(49, 49))

    render_loop(maze, maze_gen, maze_solver, maze_height, maze_width, window_name=f"Maze-{run_count}")


if __name__ == '__main__':
    main(2)
