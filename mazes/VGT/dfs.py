"""
mazes.VGT.dfs - depth first search using the vertex growing tree module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines a method "dfs" which uses the vertex-growing tree
    module and a stack to carve a maze.  The result is equivalent to
    depth-first search as implemented in mazes.Algorithms.dfs_better.
    The algorithm is implemented as a passage carver.

    In [1], depth-first search (or DFS) is called 'recursive backtracker'.

    In addition to method "dfs", the method "init_maze" is included to create
    an oblong grid set up for passage carving.  (The growing tree algorithm
    works on arbitrary grids.)

SUMMARY

    defined here:
        method dfs - carve a maze using depth-first search
        method init_grid - create an oblong grid and set it up for carving

    Method dfs will work on any connected grid.

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
from mazes.Algorithms.growing_tree1 import VertexGrowingTree as VGT
from mazes.Queues.stack import Stack

def dfs(maze:Maze, start_cell:Cell=None, shuffle=True) -> VGT.Status:
    """depth-first search using the vertex-growing tree module"""
    return VGT.on(maze, start_cell=start_cell, QueueClass=Stack)

def init_maze(rows:int, columns:int) -> Maze:
    """create an oblong grid set up for passage carving"""
    from mazes.Grids.oblong import OblongGrid
    return Maze(OblongGrid(rows, columns))

# end module mazes.VGT.dfs