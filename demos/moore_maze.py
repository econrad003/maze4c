"""
demos.moore_maze - create a maze on a Moore grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we create a weave maze on an 8-connected (Moore neighborhood)
    grid.  The result is displayed using the matplotlib spider graphics
    module.

    Option support is limited.

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

USAGE

    moore_maze.py [-h] [-d ROWS COLS] [-a ALGORITHM] [-c] [--coff] [-p PEN]
                     [-o OUTPUT] [-t TITLE] [-v]

    Moore grid maze demonstration

    OPTIONS
        -h, --help      show this help message and exit
        -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

                            maze options:
        -a ALGORITHM, --algorithm ALGORITHM
                        The algorithm used to carve the maze. The choices are
                        w-Wilson (default), k-kruskal, d-dfs, b-bfs.

                            display options:
        -c, --console   display to console even if the maze is larger than
                        10x19.
        --coff          omit display to console for mazes no larger than
                        10x19.

                            graphics options:
        -p PEN, --pen PEN     The pen color. (Default: black.)
        -o OUTPUT, --output OUTPUT
                        An image file for the output, e.g. foo.png. (Default:
                        None.)
        -t TITLE, --title TITLE
                        A title for the maze.

control options:
  -v, --verbose         display the arguments and the output from argparse.
"""
import mazes
from mazes.Grids.oblong8 import MooreGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.kruskal import Kruskal
from mazes.Algorithms.dfs_better import DFS
from mazes.Algorithms.bfs import BFS

from mazes.Graphics.moore import Huntsman

def make_grid(rows, columns) -> Maze:
    """returns a maze object that is ready for passage carving"""
    return Maze(MooreGrid(rows, columns))

def make_maze(maze, AlgorithmClass:object=Wilson):
    """carve the maze

    returns a Status object.
    """
    return AlgorithmClass.on(maze)

def main(rows, cols, console:bool=True, AlgorithmClass:object=Wilson,
         pen:'color'='black', output:str=None,
         title:str='Moore neighborhood maze', gui:bool=True) -> Maze:
    """the main entry point"""
    maze = make_grid(rows, cols)
    print(make_maze(maze, AlgorithmClass))
    if console:
        print(maze)

    spider = Huntsman(maze)
    spider.setup(color=pen)
    if title:
        spider.title(title)
    spider.draw_maze()
    spider.fig.tight_layout()
    if output:
        print(f"Saving to {output}")
        spider.save_image(output)
    if gui:
        spider.show()
    return maze

def parse_args(argv):
    """parse the command line arguments"""
    import argparse

    DESC = "Moore grid maze demonstration"
    EPI = ""
    default_dim = (8, 13)
    console_max = (10, 19)
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    parser.add_argument('-d', '--dim', type=int, nargs=2, \
        default=default_dim, metavar=('ROWS', 'COLS'), \
        help='the numbers of rows and columns in the maze.' \
        + f'  (Default: {default_dim}.)')

    maze = parser.add_argument_group('maze options')
    maze.add_argument('-a', '--algorithm', type=str, default='w', \
        help='The algorithm used to carve the maze.  The choices are' \
        + ' w-Wilson (default), k-kruskal, d-dfs, b-bfs.')

    display = parser.add_argument_group('display options')
    display.add_argument('-c', '--console', action='store_true', \
        help='display to console even if the maze is larger than 10x19.')
    display.add_argument('--coff', action='store_true', \
        help='omit display to console for mazes no larger than 10x19.')

    graphics = parser.add_argument_group('graphics options')
    graphics.add_argument('-p', '--pen', type=str, default='black', \
        help='The pen color.  (Default: black.)')
    graphics.add_argument('-o', '--output', type=str, default=None, \
        help='An image file for the output, e.g. foo.png.' \
        + '  (Default: None.)')
    graphics.add_argument('-t', '--title', type=str,
        default='Moore neighborhood maze', \
        help='A title for the maze.')
    graphics.add_argument('--goff', action='store_true', \
        help="Don't display the graphics.  The graphics are drawn " \
        + "regardless.  A warning will be displayed if this option" \
        + "is set and not output is requested.")

    control= parser.add_argument_group('control options')
    control.add_argument('-v', '--verbose', action='store_true', \
        help='display the arguments and the output from argparse.')

    args = parser.parse_args(argv)
    if args.verbose:
        print("command line input:")
        print(f"    {argv=}")
        print("argparse output:")
        print(f"    {args=}")
    rows, cols = args.dim
    max_rows, max_cols = console_max
    console = True
    if args.coff or rows > max_rows or cols > max_cols:
        console = False
    if args.console:
        console = True
    algorithm = args.algorithm[:1].lower()
    algorithms = {'w':Wilson, 'k':Kruskal, 'd':DFS, 'b':BFS}
    if algorithm in algorithms:
        AlgorithmClass = algorithms[algorithm]
    else:
        AlgorithmClass = Wilson
        print("WARNING: Algorithm class set to default (Wilson's algorithm).")
    if args.goff and not args.output:
        print("WARNING: No gui and no output!")
    return main(rows, cols, console, AlgorithmClass, args.pen, args.output,
        args.title, not args.goff)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.sidewinder
