"""
demos.hierholzer - demonstration of Hierholzer's algorithm for Eulerian tours
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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
from mazes import rng
from mazes.Grids.eulerian_oblong import maximally_Eulerian
from mazes.Algorithms.hierholzer import Hierholzer

DESC = "Hierholzer's algorithm demonstration"
BREAK_AFTER = 60

def make_maze(rows, cols, debug=True):
    """create a maximally Eulerian maze"""
    if debug:
        msg = f"Creating a maximally Eulerian {rows}×{cols} oblong maze."
        print(msg)
    maze = maximally_Eulerian(rows, cols)
    return maze

def delete_one_passage(maze, debug=True):
    """delete a random passage"""
    join = rng.choice(list(maze))
    cell1, cell2 = join
    if debug:
        msg = f"Deleting the passage between {cell1.index} and {cell2.index}"
        print(msg)
    maze.unlink(join)
    return cell1, cell2

def make_trail(maze, start, debug=True):
    """find an Eulerian trail"""
    status = Hierholzer.on(maze, start)
    if debug:
        print(status)
    trail = status.trail
    return trail

def make_tour(maze, debug=True):
    """find an Eulerian tour"""
    status = Hierholzer.on(maze)
    if debug:
        print(status)
    trail = status.trail
    return trail

def positive_int(n:str):
    """positive integer check"""
    n = int(n)
    if n <= 0:
        raise ValueError(f"{n} is not a positive integer")
    return n

def display_results(maze, trail, cell1, cell2):
    """report the results of the experiment"""
    def break_trail(n, prev, curr, msg):
        """dead end?"""
        if n > 0:
            if prev == curr:
                print(msg)
                return "  "
            print(msg, "-- DEAD END")
        else:
            print(msg)
        i, j = curr.index
        return f"({i},{j})"

    if cell1:
        cell1.label = "X"
        cell2.label = "Y"
        msg = "Eulerian trail:"
    else:
        trail[0][0].label = "0"
        trail[0][2].label = "1"
        trail[-1][0].label = "n"
        msg = "Eulerian tour:"
    print(maze)
    prev = None
    n = 0
    for packet in trail:
        cell1, join, cell2 = packet
        if cell1 != prev or len(msg)>BREAK_AFTER:
            msg = break_trail(n, prev, cell1, msg)
            n = 1
        prev = cell2
        i, j = cell2.index
        msg += f" -- ({i},{j})"
    print(msg)
    print(f"Passages in maze: {len(maze)}")
    print(f"  Steps in trail: {len(trail)}")
    cells = set()
    joins = set()
    for packet in trail:
        cells.add(packet[0])
        joins.add(packet[1])
        cells.add(packet[2])
    print(f"   Cells spanned: {len(cells)}")
    print(f"Passages spanned: {len(joins)}")

def main(argv):
    """parse arguments"""
    import argparse
    EPI = "Some dimension won't work."
    parser = argparse.ArgumentParser(description = DESC, epilog=EPI)
    parser.add_argument("-d", "--dim", type=positive_int, nargs=2, \
        metavar=("ROWS", "COLS"), default=(8, 13), \
        help="dimensions of the maze.")
    parser.add_argument("--trail", action="store_true", \
        help="set this flag to create an Eulerian trail.")
    args = parser.parse_args(argv)
    print(args)
    rows, cols = args.dim
    maze = make_maze(rows, cols)
    if args.trail:
        cell1, cell2 = delete_one_passage(maze)
        trail = make_trail(maze, cell1)
    else:
        cell1, cell2 = None, None
        trail = make_tour(maze)
    display_results(maze, trail, cell1, cell2)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
