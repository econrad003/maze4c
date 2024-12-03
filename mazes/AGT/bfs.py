"""
mazes.AGT.dfs - breadth first search using the arc growing tree module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines a method "bfs" which uses the arc-growing tree
    module and a queue to carve a maze.  The result is roughly equivalent to
    mazes.VGT.bfs.  The algorithm is implemented as a passage carver.

    In addition to method "bfs", the method "init_maze" is included to create
    an oblong grid set up for passage carving.  (The arc-growing tree algorithm
    works on arbitrary grids.)

    On an oblong grid, the resulting maze will probably be almost the same as
    a typical vertex-based breadth-first search.  There might be some very
    subtle differences in the biases.

SUMMARY

    defined here:
        method bfs - carve a maze using an arc-based breadth-first search
        method init_grid - create an oblong grid and set it up for carving

    Method bfs will work on any connected grid.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

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
from mazes import Cell
from mazes.maze import Maze
from mazes.Algorithms.growing_tree2 import ArcGrowingTree as AGT
from mazes.Queues.queue import Queue

def bfs(maze:Maze, start_cell:Cell=None, shuffle=True) -> AGT.Status:
    """depth-first search using the arc-growing tree module"""
    return AGT.on(maze, start_cell=start_cell, QueueClass=Queue)

def init_maze(rows:int, columns:int) -> Maze:
    """create an oblong grid set up for passage carving"""
    from mazes.Grids.oblong import OblongGrid
    return Maze(OblongGrid(rows, columns))

# end module mazes.AGT.bfs