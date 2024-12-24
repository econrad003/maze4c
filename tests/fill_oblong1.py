"""
tests.fill_oblong1 - test the fill method in graphics.oblong1
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This silly test colors four cells in a maze.

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
from mazes.Algorithms.simple_binary_tree import BinaryTree

    # the new improved daddy long legs (23 Dec 2024)
from mazes.Graphics.oblong1 import Phocidae

    # create a maze
maze = Maze(OblongGrid(5, 8))
BinaryTree.on(maze)

	# create the fill array
cell1 = maze.grid[0,0]
cell2 = maze.grid[4,7]
cell3 = maze.grid[2,3]
cell4 = maze.grid[3,2]
fills = {cell1:"red", cell2:"green", cell3:"blue", cell4:"goldenrod"}

	# plot the maze
spider = Phocidae(maze)
spider.setup(fillcolors=fills)
spider.draw_maze()
spider.show()

# end module tests.fill_oblong1