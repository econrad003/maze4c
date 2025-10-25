"""
demos.agt_sprim - create a "Simplified Prim" maze using the arc growing tree
    module (mazes.Algorithms.growing_tree2 via mazes.AGT.sprim)
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is "Simplified Prim".  It is implemented using a random-in,
    first out (RIFO?) queue or "random queue" using the arc-based growing
    tree architecture.

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
"""
import mazes
from mazes.AGT.sprim import sprim, init_maze
from mazes.Graphics.oblong1 import Pholcidae

def make_maze(maze:"Maze", start_cell:"Cell", shuffle:bool=True) -> "Status":
    """carve the maze"""
    return sprim(maze, start_cell=start_cell, shuffle=shuffle)

def main(dim, start, shuffle, color, output, console, gui):
    """the main entry point"""
    maze = init_maze(*dim)
    if start:
        start_cell = maze.grid[start]
        start_cell.label = 'S'
    else:
        start_cell = None
    print(make_maze(maze, start_cell, shuffle))
    if console or (dim[0] <= 10 and dim[1] <= 15):
        print(maze)

    spider = Pholcidae(maze)
    spider.setup(color=color)
    title = 'Simplified "Prim"'
    if shuffle:
        title += "(AGT)"
    else:
        title += "(AGT/no shuffle)"
    spider.title(title)
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

    DESC = 'Simplified "Prim" growing tree demonstration (arc-based)'
    EPI = 'The similarities between simplified "Prim" and Prim\'s algorithm' \
    	+ ' are at best superficial.'
    default_dim = (8, 13)
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    parser.add_argument('-d', '--dim', type=int, nargs=2, \
        default=default_dim, metavar=('ROWS', 'COLS'), \
        help='the numbers of rows and columns in the maze.' \
        + f'  (Default: {default_dim}.)')
    parser.add_argument('--start', type=int, nargs=2, \
        default=None, metavar=('ROW', 'COL'), \
        help='the starting cell.' \
        + f'  (Default: None.)')
    parser.add_argument('--middle', action="store_true", \
        help='this places the starting cell in or near the center of the' \
        + ' grid.  If this option is specified, the --start option is' \
        + ' ignored.  If neither option is specified, the start location is' \
        + ' random.')

    maze = parser.add_argument_group('maze options')
    maze.add_argument('-X', '--no-shuffle', action='store_true', \
        help='set this option to suppress shuffling when accessing' \
        + ' the neighborhoods.  This will typically result in a simpler' \
        + ' maze, but the actual effect will depend on how dictionaries' \
        + ' are implemented in your Python distribution.')

    graphics = parser.add_argument_group('graphics options')
    maze.add_argument('-p', '--pen', type=str, default='black', \
        help='The pen color.  (Default: black.)')
    maze.add_argument('-o', '--output', type=str, default=None, \
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
    if args.middle:
        rows, cols = args.dim
        args.start = (rows//2, cols//2)
    elif args.start:
        args.start = tuple(args.start)
    shuffle = not args.no_shuffle
    main(args.dim, args.start, shuffle, args.pen, args.output,
         args.console, not args.no_gui)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.agt_sprim
