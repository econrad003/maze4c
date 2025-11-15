"""
mazes.tests.animation - test the basic Python turtle animation driver
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a quick and dirty test module.  At some point, it should be
    expanded into a more useful demo.

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
from time import sleep

from mazes.maze import Maze
from mazes.Grids.oblong import OblongGrid
from mazes.Algorithms.dfs_better import DFS
from mazes.Graphics.animation import Animation

    # create the grid
grid = OblongGrid(6, 9)
maze = Maze(grid)

    # set up a few preparatory links
cell0 = grid[0,0]
cell1 = cell0.east
cell2 = cell1.north
maze.link(cell0, cell1)
maze.link(cell1, cell2)

    # prepare the animation
spider = Animation(maze, speed=3)
spider.title("DFS animation")
print("Three second timeout:")
for t in range(3, 0, -1):
    print(f"{t=}...")
    sleep(1)

    # carve the maze
cell0.hide()
cell1.hide()
DFS.on(spider.maze)
cell1.reveal()
cell0.reveal()

    # animation
print("When maze is complete, click on the screen to exit...")
spider.animate()
print("Bye-bye!")
