"""
mazes.watershed - divide a grid into several wetlands/swamps/bogs
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we take a connected grid and partition it into several connected
    subgrids which we can think of as a network of wetlands.  The ultimate
    intent, here, is to generalize the recursive division algorithm.
    This particular idea was inspired by the blog article [2].  (There
    are some differences, but I think they are "similar in spirit".)

    In essence, the idea is straighforward.  We start with two cells which
    we can think of as water sources.  Water flows from each into
    neighboring cells, to form watersheds.  The main rule is that the
    two watersheds are kept separate.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Jamis Buck.  "A better recursive division algorithm" in The
        Buckblog.  Web.  15 January 2015.  Accessed 12 August 2025.
            URL: https://weblog.jamisbuck.org/2015/1/15/ -
                        better-recursive-division-algorithm.html

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
from mazes.cell import Cell
from mazes.grid import Grid
from mazes.maze import Maze
from mazes.Queues.queue import Queue

class Watershed(object):
    """a network of connected subgrids"""

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, grid:(Grid, set), seeds:list, *args,  **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override parse_args,
            initialize, or configure.

        REQUIRED ARGUMENTS

            grid - a connected grid

            seeds - the water sources

            args - additional positional arguments (for subclasses)

        KEYWORD ARGUMENTS

            QueueType (default Queue) - the queuing structure
                This should be derived from GeneralizedQueue in module
                mazes.gqueue.

            qargs - additional queung arguments (dictionary)
                This should include the priority function if the queue is
                a priority queue.

            kwargs - additional keyword arguments (for subclasses)
        """
        self.parent = grid                  # the parent grid or subgrid
        self.seeds = list(set(seeds))       # the water sources
        if len(seeds) < 2:
            raise ValueError("Need at least two water sources")
        self.watersheds = dict()            # the watersheds
        self.sources = dict()               # maps cells to their source
        self.unvisited = set(grid)          # the unvisited cells
        self.q = dict()                     # the queues
        self.frontiers = dict()             # wetland borders
        self.new_random()                   # random number generator
        self.parse_args(*args, **kwargs)    # pass remaining arguments
        self.initialize()
        self.configure()

    def parse_args(self, QueueType:"Queue"=Queue, qargs:dict={}):
        """argument parser for Cell class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        self.QueueType = QueueType
        self.qargs = qargs

    def add(self, cell:Cell, watershed:int):
        """add a cell to a watershed"""
        if cell not in self.unvisited:
            raise RuntimeError("The cell must be unvisited when adding...")
        self.unvisited.remove(cell)
        self.watersheds[watershed].add(cell)
        self.sources[cell] = watershed
        neighbors = list(cell.neighbors)
        self.rng.shuffle(neighbors)
        for nbr in neighbors:
            j = self.sources.get(nbr)       # mapped?
            if j == None:                       # No!
                self.q[watershed].enter(cell, nbr)
            else:                               # Yes!
                if j != watershed:                  # frontier!
                    edge = (min(watershed, j), max(watershed, j))
                    door = frozenset([cell, nbr])
                    self.frontiers[edge].add(door)

    def new_random(self, prng:'Random'=rng):
        """set or reset the random number generator"""
        self.rng = prng

    def initialize(self):
        """default initialization"""
        Q = self.QueueType
        qargs = self.qargs
        for watershed in range(len(self.seeds)):
            seed = self.seeds[watershed]
            if watershed not in self.q:
                self.q[watershed] = Q(**qargs)          # default queue type
            self.watersheds[watershed] = set()          # the watersheds
            for j in range(watershed+1, len(self.seeds)):
                self.frontiers[(watershed, j)] = set()      # the borders

    def configure(self):
        """default configuration"""
        for i in range(len(self.seeds)):
            seed = self.seeds[i]
            self.add(seed, i)

    def round_robin(self) -> bool:
        """round robin once through the queues"""
        more = False                            # assume all queues are empty
        for watershed in range(len(self.seeds)):
            while not self.q[watershed].is_empty:
                _, cell = self.q[watershed].leave()
                if cell in self.unvisited:
                    self.add(cell, watershed)
                    more = True                         # we found a nonempty queue
                    break # while #
        return more

    def partition(self):
        """partition the grid or subgrid into watersheds"""
        while len(self.unvisited) > 0:
            more = self.round_robin()
            if len(self.unvisited) > 0 and not more:
                raise RuntimeError("The subgrid is not connected")

    def label(self):
        """label the cells by watershed"""
        for cell in self.sources:
            cell.label = str(self.sources[cell])

    def initialize_maze(self) -> Maze:
        """create a grid showing the component structure"""
            # create the grid
        grid = Grid()
        for watershed in range(len(self.seeds)):
            grid[watershed] = grid.newcell(watershed)
        for edge in self.frontiers:
            if len(self.frontiers[edge]) > 0:
                i, j = edge
                cell1 = grid[i]
                cell2 = grid[j]
                cell1[j] = cell2
                cell2[i] = cell1
        return Maze(grid)

    def doors(self, maze:Maze):
        """given a component maze, select one door per edge"""
        joins = list()
        for join in maze:
            items = join.cells
            item1, item2 = items
            i = min(item1.index, item2.index)
            j = max(item1.index, item2.index)
            frontier = list(self.frontiers[(i,j)])
            cell1, cell2 = self.rng.choice(frontier)
            if isinstance(items, frozenset):            # edge
                joins.append({cell1, cell2})
                continue
                    # directed arc
            if cell1 in self.watersheds[item1.index]:
                joins.append([cell1, cell2])
            else:
                joins.append([cell2, cell1])
        return joins

# end module mazes.watershed
