"""
demos.inwinder - create an inwinder maze
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we use the inwinder algorithm (based on sidewinder, but using
    rings instead of rows and columns) to create a maze. The result is
    displayed using the matplotlib spider graphics module.

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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.inwinder import Inwinder
from mazes.Graphics.oblong1 import Phocidae

def make_grid(rows, columns) -> Maze:
    """returns a maze object that is ready for passage carving"""
    return Maze(OblongGrid(rows, columns))

def make_inwinder(maze, bias=0.5, which=any) -> Inwinder.Status:
    """run inwinder"""
    return Inwinder.on(maze, bias=bias, which=which)

def main(rows:int, cols:int, color, output=None,
         tree_args:dict={}, console:bool=False, gui:bool=True):
    """the main entry point"""
    maze = make_grid(rows, cols)
    print(make_inwinder(maze, **tree_args))
    if (rows <= 10 and cols <= 15) or console:
        print(maze)

    spider = Phocidae(maze)
    spider.setup(color=color)
        # The cocktail shaker algorithm guarantees a binary tree with
        # sidewinder, but not with inwinder.  If the first or last cell
        # in a run is a corner cell, then (respectively) the second or
        # penultimate cell might be the location of a degree 4
        # intersection.
    title = "Cocktail Shaker Inwinder Tree" \
        if tree_args.get("which") == (0, -1) else "Inwinder"
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

    DESC = "Inwinder demonstration"
    EPI = "Unlike Sidewinder, the cocktail shaker doesn't guarantee" \
        + " a binary tree."
    default_dim = (8, 13)
    default_ways = ('east', 'north')
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    parser.add_argument('-d', '--dim', type=int, nargs=2, \
        default=default_dim, metavar=('ROWS', 'COLS'), \
        help='the numbers of rows and columns in the maze.' \
        + f'  (Default: {default_dim}.)')

    maze = parser.add_argument_group('maze options')
    maze.add_argument('-b', '--bias', type=float, default=0.5, \
        help='the probability of the toss being a head.' \
        + '  (Default: 0.5)')
    maze.add_argument('-C', '--cocktail-shaker', action='store_true', \
        help='if set, the run choice will be either first or last.')

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
    rows, cols = args.dim
    tree_args ={}
    tree_args['bias'] = args.bias
    if args.cocktail_shaker:
        tree_args['which'] = (0, -1)
    main(rows, cols, args.pen, args.output,
         tree_args, args.console, not args.no_gui)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.inwinder