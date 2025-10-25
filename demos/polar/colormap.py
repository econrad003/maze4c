"""
demos.polar.maze1 - create a theta maze
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demo creates a theta (or polar or circular) maze using a choice of
    parameters and algorithms.

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
from matplotlib.colors import to_rgb

import mazes
from mazes import rng
from mazes.Grids.polar import ThetaGrid
from mazes.maze import Maze

    # algorithms
from mazes.VGT.dfs import dfs
from mazes.VGT.bfs import bfs
from mazes.VGT.sprim import sprim
from mazes.VGT.vprim import vprim
from mazes.AGT.primic import primic
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.houston import Houston
from mazes.Algorithms.kruskal import Kruskal
from mazes.Algorithms.hunt_kill import HuntKill

from mazes.tools.distance_map import DistanceColoring

    # graphics
from mazes.Graphics.polar1 import Pholcidae

def init_maze(rings:int, pole:int=6, split:int=1) -> Maze:
    """create an empty theta maze"""
    return Maze(ThetaGrid(rings, pole=pole, split=split))

def prim(maze, start_cell=None):
    """Prim's algorithm with random edge weights"""
    pr = {}
    for cell in maze.grid:
        for nbr in cell.neighbors:
            cost = rng.random()
            arc = (cell, nbr)
            pr[arc] = cost
            arc = (nbr, cell)
            pr[arc] = cost
    if start_cell:
        return primic(maze, start_cell, pr_map=pr)
    return primic(maze, pr_map=pr)

def main(grid_args:tuple, graphics_args:tuple, alg_args,
         output_pathname:str=None):
    """the main entry point"""

            # create the empty maze
    rings, pole, split = grid_args
    print(f"Theta maze: {rings=}, {pole=}, {split=}")
    maze = init_maze(rings, pole, split)
    grid = maze.grid
    print(f"      grid: {len(grid)} cells")

            # carve the maze
    alg, start_cell, kwargs = alg_args
    if start_cell:
        start_cell = tuple(start_cell)
        start_cell = grid[start_cell]

    if alg == None:
        print("Skipping maze carver...")
    else:
        if start_cell:
            print(alg(maze, start_cell, **kwargs))
        else:
            print(alg(maze, **kwargs))

            # display the result
    hot, cold, zero, title = graphics_args
    if not start_cell:
        start_cell = grid[0, 0]
    distances = DistanceColoring(maze,
                                 to_rgb(hot), to_rgb(cold), to_rgb(zero),
                                 source=start_cell)
    spider = Pholcidae(maze)
    spider.setup(fillcolors=distances.gradients)
    spider.title(title)
    spider.draw_maze()
    if output_pathname:
        spider.save_image(output_pathname)
    spider.show()

def parse_args(argv):
    """parse the command line arguments"""
    import argparse

    DESC = "create a distance-based color map for a theta maze"
    EPI = ""

            # defaults
    RINGS = 5
    POLE = 6
    SPLIT= 1
    TITLE = "Theta Maze"

            # create parser
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    grid = parser.add_argument_group('grid options', \
        'These options determine the arrangement of cells in the grid.')
    grid.add_argument('-r', '--rings', type=int, default=RINGS, \
        help=f'the numbers of rings in the maze.  (default: {RINGS}.)')
    grid.add_argument('-p', '--pole', type=int, default=POLE, \
        help='the number of cells at the pole.  (default: {POLE})')
    grid.add_argument('-s', '--split', type=int, default=SPLIT, \
        help='the splitting length.  (default: {SPLIT})')

    graphics = parser.add_argument_group('graphics options', \
        'These options control the graphics output.')
    graphics.add_argument('-H', '--hot', type=str, default="crimson", \
        help=f'the hot color for cells close to zero in distance.' \
        + '  (default: crimson')
    graphics.add_argument('-C', '--cold', type=str, default="skyblue", \
        help=f'the cold color for cells far away in distance.' \
        + '  (default: skyblue')
    graphics.add_argument('-Z', '--zero', type=str, default="goldenrod", \
        help=f'the zero distance color.' \
        + '  (default: goldenrod')
    graphics.add_argument('-T', '--title', type=str, nargs='*', default=[], \
        help=f'use this option to set a title.  If this option is not set,' \
        + 'a title will be automatically generated.')
    graphics.add_argument('-o', '--output', type=str, default='', \
        help="an optional image output file")

    ALGS = {}
    ALGS[1] = ['depth-first search (default)', '1', 'dfs']
    ALGS[2] = ['breadth-first search', '2', 'bfs']
    ALGS[3] = ['simplified "Prim"', '3', 'sp']
    ALGS[4] = ['vertex "Prim"', '4', 'vp']
    ALGS[5] = ['Prim\'s algorithm', '5', 'p', 'prim']
    ALGS[6] = ['Wilson\'s algorithm', '6', 'w', 'wilson']
    ALGS[7] = ['Houston\'s algorithm', '7', 'h', 'houston']
    ALGS[8] = ['Kruskal\'s algorithm', '8', 'k', 'kruskal']
    ALGS[9] = ['hunt and kill algorithm', '8', 'hk']

    ALGS['dfs'] = ALGS['1'] = (dfs, 'depth-first search')
    ALGS['bfs'] = ALGS['2'] = (bfs, ALGS[2][0])
    ALGS['sp'] = ALGS['3'] = (sprim, ALGS[3][0])
    ALGS['vp'] = ALGS['4'] = (vprim, ALGS[4][0])
    ALGS['prim'] = ALGS['p'] = ALGS['5'] = (prim, ALGS[5][0])
    ALGS['wilson'] = ALGS['w'] = ALGS['6'] = (Wilson.on, ALGS[6][0])
    ALGS['houston'] = ALGS['h'] = ALGS['7'] = (Houston.on, ALGS[7][0])
    ALGS['kruskal'] = ALGS['k'] = ALGS['8'] = (Kruskal.on, ALGS[8][0])
    ALGS['hk'] = ALGS['9'] = (HuntKill.on, ALGS[9][0])

    ALGHELP1 = 'these are the available algorithms: '
    ALGHELP2 = []
    n = 0
    while n in ALGS:
        x = list(ALGS[n])
        car = x[0]
        cdr = x[1:]
        ALGHELP2.append(' or '.join(cdr) + ' - ' + car)
        n += 1
    ALGHELP = ALGHELP1 + '; '.join(ALGHELP2) + '.'

    algorithms = parser.add_argument_group('algorithm options', \
        'These options control the maze carving.')
    algorithms.add_argument('-a', '--algorithm', type=str, default='dfs',
        help=ALGHELP)
    algorithms.add_argument('--start', type=int, nargs=2 , default=None, \
        metavar = ("R", "N"), \
        help = 'an (r, n) index for an optional starting cell.  Here, r is' \
        + ' the ring number and n is the ordinal number of the cell in the' \
        + ' ring.  The r-values are numbered starting with the polar ring as' \
        + ' 0.  The n-values are number counterclockwise starting at the' \
        + ' positive x-axis.')

    houston = parser.add_argument_group('Houston\'s algorithm options')
    houston.add_argument('--cutoff', type=float, default=1/3, \
        help = 'The cutoff rate for Houston\'s algorithm.' \
        + f'  (default {1/3}')
    houston.add_argument('--failures', type=float, default=0.9, \
        help = 'The failure rate for Houston\'s algorithm.' \
        + f'  (default {0.9}')

            # parse and pack the command line arguments
    args = parser.parse_args(argv)
    grid_args = (args.rings, args.pole, args.split)
    algstr = args.algorithm.lower()
    alg, algname = ALGS[algstr]
    if not args.title:
        args.title.append(TITLE)
        args.title.append("(" + algname + ")")
    title = ' '.join(args.title)
    graphics_args = (args.hot, args.cold, args.zero, title)

    kwargs = {}
    if alg == Houston.on:
        kwargs["cutoff_rate"] = args.cutoff
        kwargs["failure_rate"] = args.failures
    if (alg == Kruskal.on) and args.start:
        print("Starting cell is not used in Kruskal's algorithm...")
        args.start = None
    alg_args = (alg, args.start, kwargs)

            # run the demonstration
    main(grid_args, graphics_args, alg_args, args.output)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.polar.maze1
