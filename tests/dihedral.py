"""
tests.dihedral - test the dihedral module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

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

    # the class to test
from mazes.Algorithms.dihedral import DihedralGroup

    # the required classes
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.kruskal import Kruskal

def main(rows:int, cols:int):
    """the test"""
    print(f"Carving the maze... {rows=}, {cols=}")
    maze = Maze(OblongGrid(rows, cols))
    Kruskal.on(maze)

    if rows == cols:
        print("The symmetry group is D(8)...")
        print("   4 rotations and 4 reflections...")
    else:
        print("The symmetry group is D(4)...")
        print("   2 rotations and 2 reflections...")
    print(f"Symmetry group orbit:")
    group = DihedralGroup(maze, debug=True)
    group.build_table()

    if rows == cols:
        assert len(group.symmetries) == 8
    else:
        assert len(group.symmetries) == 4
    for i in range(len(group.symmetries)):
        item = group.symmetries[i]
        assert type(item) == Maze
        if i == 0:
            assert item == maze
        else:
            assert item != maze
    
def parse_args(argv:list):
    """parse the command line arguments"""
    import argparse

    parser = argparse.ArgumentParser("test the dihedral module")
    parser.add_argument("-d", "--dim", nargs=2, type=int, \
        metavar=('ROWS', "COLS"), default=(5,5), \
        help="the number of rows and columns")
    args = parser.parse_args(argv)
    rows, cols = args.dim
    main(rows, cols)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])
