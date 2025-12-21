"""
demos.Konigsberg_bridges - create a maze from a grid based on the
    Königsberg bridges problem layout.
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    We create a maze based on a masked grid which approximates the layout
    of the seven bridges of Königsberg.  Apart from the superficial
    resemblance of the grid to the layout of the town in Euler's day, there
    is no connection to the actual problem.

USAGE

    Just run it as a module:
        python -m demos.Konigsberg_bridges

    Note that the module name uses a capital K, so you will need to use
    the shift key.

    If you save the file, use SVG (scalable vector graphics).  You can add
    a title with a vector graphics editor (e.g. Inkscape).

NOTE

    The seven bridges of Königsberg is a foundational problem in graph
    theory and in topology -- what Leonhard Euler called geometria
    situs (geometry of location) to distinguish it from geometry of
    distances (or metric geometry).  The town of Königsberg had seven
    bridges and the problem was to find a path through the town which
    crossed each bridge exactly once.  Euler was able to show that there
    was no such path.  He was also able to state, but not prove, general
    conditions for the existance of such a path.

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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Graphics.oblong1 import Pholcidae

def getchar(n:int, line:str):
    """get the nth character"""
    return 'X' if n >= len(line) else line[n]

print("Dedicated to Leonhard Euler (1707-1783)")
print("\tfounder of 'geometria situs'")
print("\ta forerunner of both graph theory and topology...")
print("Königsberg: preparing the grid")
maze = Maze(OblongGrid(25, 80))
filename = "demos/Konigsberg_bridges.txt"
row = 25
hidden = 0
with open(filename, "r") as fp:
    for line in fp:
        row -= 1
        if row < 0:
            break
        for col in range(80):
            if getchar(col, line) != 'X':
                maze.grid[row, col].hide()
                hidden += 1
print(f"Königsberg: {hidden=}")

print(Wilson.on(maze))

spider = Pholcidae(maze)
spider.setup()
spider.draw_maze()
spider.fig.tight_layout()
spider.show()

# END demos.Konigsberg_bridges
