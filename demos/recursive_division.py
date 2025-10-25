"""
demos.recursive_division - create a maze using recursive division
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we use the recursive division algorithm to create a rectangular
    maze.  The result is displayed using the matplotlib spider graphics
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

    recursive_division.py [-h] [-d ROWS COLS] [-m MINR MINC] [-r] [-p PEN]
                             [-o OUTPUT] [-c] [-v] [-N]
    Recursive division demonstration

    options:
      -h, --help            show this help message and exit
      -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

    maze options:
      -m MINR MINC, --minimums MINR MINC
                        The minimum numbers of rows and columns for dividing.
                        Both values must be at least 2. (Default: (2, 2).)
      -r, --rooms           if set, rooms will be carved. This makes a difference
                        only if either the row or the column minimum is
                        greater than 2.
      -L, --labels          if set, rooms will be labelled in the console display.


    graphics options:
      -p PEN, --pen PEN     The pen color. (Default: black.)
      -o OUTPUT, --output OUTPUT
                        An image file for the output, e.g. foo.png. (Default:
                        None.)

    control options:
      -c, --console         if the maze is larger than 10 rows or 15 columns,
                        console output is normally suppressed. Set this option
                        to display larger mazes to the console.
      -v, --verbose         display the arguments and the output from argparse.
      -N, --no-gui          if this is set, the graphics display is suppressed.
"""
import mazes
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.recursive_division import RecursiveDivision
from mazes.Graphics.oblong1 import Pholcidae

def make_grid(rows, columns) -> Maze:
    """returns a maze object that is ready for passage carving"""
    return Maze(OblongGrid(rows, columns))

def make_maze(maze, min_rows:int=2, min_cols:int=2,
              carve_rooms:bool=False, label_rooms:bool=False):
    """run recursive division

    returns the RecursiveDivision.Status object.
    """
    return RecursiveDivision.on(maze, min_rows=min_rows, \
        min_cols=min_cols, carve_rooms=carve_rooms, \
        label_rooms=label_rooms)

def main(rows:int, cols:int, min_rows:int=2, min_cols:int=2,
         carve_rooms:bool=False, label_rooms:bool=False,
         color:str="black", output:str=None,
         console:bool=False, gui:bool=True):
    """the main entry point"""
    maze = make_grid(rows, cols)
    print(make_maze(maze, min_rows, min_cols, carve_rooms, label_rooms))
    if (rows <= 10 and cols <= 15) or console:
        print(maze)

    spider = Pholcidae(maze)
    spider.setup(color=color)
    spider.title("Recursive Division Maze")
    spider.draw_maze()
    spider.fig.tight_layout()
    if output:
        print(f"Saving to {output}")
        spider.save_image(output)
    if gui:
        spider.show()

def parse_args(argv):
    """parse the command line arguments"""
    import argparse

    DESC = "Recursive division demonstration"
    EPI = ""
    default_dim = (8, 13)
    default_mins = (2, 2)
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    parser.add_argument('-d', '--dim', type=int, nargs=2, \
        default=default_dim, metavar=('ROWS', 'COLS'), \
        help='the numbers of rows and columns in the maze.' \
        + f'  (Default: {default_dim}.)')

    maze = parser.add_argument_group('maze options')
    maze.add_argument('-m', '--minimums', type=int, nargs=2, \
        default=default_mins, metavar=('MINR', 'MINC'), \
        help='The minimum numbers of rows and columns for dividing.' \
        + '  Both values must be at least 2.' \
        + f'  (Default: {default_mins}.)')
    maze.add_argument('-r', '--rooms', action='store_true', \
        help='if set, rooms will be carved.' \
        + '  This makes a difference only if either the row or the' \
        +' column minimum is greater than 2.')
    maze.add_argument('-L', '--labels', action='store_true', \
        help='if set, rooms will be labelled in the console display.')

    graphics = parser.add_argument_group('graphics options')
    graphics.add_argument('-p', '--pen', type=str, default='black', \
        help='The pen color.  (Default: black.)')
    graphics.add_argument('-o', '--output', type=str, default=None, \
        help='An image file for the output, e.g. foo.png.' \
        + '  (Default: None.)')

    control= parser.add_argument_group('control options')
    control.add_argument('-c', '--console', action='store_true', \
        help='if the maze is larger than 10 rows or 15 columns,' \
        + ' console output is normally suppressed.  Set this' \
        + ' option to display larger mazes to the console.')
    control.add_argument('-v', '--verbose', action='store_true', \
        help='display the arguments and the output from argparse.')
    control.add_argument('-N', '--no-gui', action='store_true', \
        help='if this is set, the graphics display is suppressed.')
    args = parser.parse_args(argv)
    if args.verbose:
        print("command line input:")
        print(f"    {argv=}")
        print("argparse output:")
        print(f"    {args=}")
    rows, cols = args.dim
    min_rows, min_cols = args.minimums
    min_rows = max(2, min_rows)
    min_cols = max(2, min_cols)
    args.minimums = (min_rows, min_cols)
    print(args)
    main(rows, cols, min_rows, min_cols, args.rooms, args.labels,
         args.pen, args.output,
         args.console, not args.no_gui)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.sidewinder
