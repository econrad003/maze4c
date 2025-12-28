"""
mazes.Metrics.hops - the hop distance metric for a growing tree
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DEFINITIONS

    A metric on a set X is a real-valued function d:X²→R which
    satisfies the following constraints:
        a) d is positive definite, i.e., for each x and y in X,
             1) d(x, y) ≥ 0; and
             2) d(x, y) = 0 if and only if x = y;
        b) d is symmetric, i.e., for each x and y in X,
                d(x, y) = d(y, x); and
        c) d satisfies the triangle inequality, i.e., for each x, y, z
            in X,
                d(x, y) + d(y, z) ≥  d(x, z).

    A metric space is a pair (X, d) where X is a set and d is a metric
    on X.

PREPARATORY ANALYSIS

    Given a tree that is growing one cell at a time, let T be the cells
    in the tree and let F be the cells in the frontier.  Consider a cell
    c1 in F.  Suppose c2 is a neighbor in T of c1.  Let c3 be an arbitrary
    cell in T.  The claim is that if we add the edge {c1, c2} to the tree
    then d(c3, c1) = d(c3, c2) + 1 and for every cell c4 in T, d(c3, c4)
    remains unchanged.

    The proof is straightforward.  First, suppose the addition of the
    edge {c1, c2} changes the value of d(c3, c4)  That would imply that
    there are two paths from c3 to c4, one via c1 and another wholly
    in T.  Then adding the edge creates a circuit.  (That gives rise
    to a contradiction.  We started with tree T with |T|-1 edges.  We
    added one frontier edge and one frontier cell to obtain a tree with
    |T|+1 cells and |T| edges, so T+{c1,c2} cannot have a circuit.)

    Now clearly there is a path with length d(c3, c2)+1 edges from c3
    to the new cell c1.  But after adding {c1,c2}, if the distance is
    not d(c3, c2)+1, then there must be a second path.  The two paths
    give rise to a circuit.  (Contradiction!)

DESCRIPTION

    From the preparatory analysis, adding an edge "only" requires updating
    distances to and from the new node.  But the updating process is apt
    to create a bottleneck.

    This module contains the a class which handles the updates.  For the
    algorithm, see module mazes.Algorithms.hoptree.

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
from collections import defaultdict

from mazes import Cell, Grid, Edge, rng
from mazes.maze import Maze
from mazes.Algorithms.floyd import Floyd, TransitiveClosure

def _shuffle(cell):
    """reorder the neighborhood"""
    nbrs = list(cell.neighbors)
    rng.shuffle(nbrs)
    return nbrs

def _no_shuffle(cell):
    """don't reorder"""
    return list(cell.neighbors)

class Metric(object):
    """the growing tree hop metric"""

    __slots__ = ("__maze", "__distances", "__visited", "__frontier",
                 "__shuffle")

    def __init__(self, maze:Maze, *args, Closure:callable=Floyd,
                 shuffle:bool=True, **kwargs):
        """contructor

        REQUIRED ARGUMENTS

            maze - a maze object; it may be empty or it may contain some joins.

        OPTIONAL ARGUMENTS

            args - positional arguments to pass to the closure class, other
                than maze.

        KEYWORD ARGUMENTS

            Closure - the transitive closure operation to use (default: Floyd).
                Floyd's algorithm uses hops while Warshall's algorithm uses
                edge weights.  If the maze is empty, just use the default.

            shuffle - randomize the order that neighborhoods are traversed

            kwargs - keyword arguments to pass to the closure class.

        A transitive closure object is used to create the initial distances
        map.
        """
        if not isinstance(maze, Maze):
            raise TypeError("the maze must be a member of class Maze")
        if not issubclass(Closure, TransitiveClosure):
            raise TypeError("The closure class must be a subclass of" \
                + " TransitiveClosure")
        closure = Closure(maze, *args, **kwargs)
        self.__distances = closure.D
        self.__visited = set()
        self.__maze = maze
        self.__shuffle = _shuffle if shuffle else _no_shuffle
        self.initialize()
        self.configure()

    def initialize(self):
        """initialization

        All cells that are contained in arcs and edges are added to
        the visited set.  Unvisited neighbors of visited cells form a
        new frontier.
        """
        for join in self.__maze:
            self.__visited.update(set(join))
        self.__frontier = set()
        for cell in self.__visited:
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.__frontier.add(nbr)

    def configure(self):
        """configuration"""
        pass

    @property
    def grid(self) -> Grid:
        """return the grid"""
        return self.__maze.grid

    @property
    def maze(self) -> Maze:
        """return the maze"""
        return self.__maze

    def is_visited(self, cell:Cell) -> bool:
        """returns true if a cell has been visited"""
        return cell in self.__visited

    @property
    def number_visited(self):
        """length of the visited set"""
        return len(self.__visited)

    @property
    def empty_frontier(self) -> bool:
        """returns True if the frontier is empty"""
        return len(self.__frontier) == 0

    @property
    def frontier(self) -> list:
        """returns the frontier as a list"""
        return list(self.__frontier)

    def in_frontier(self, cell:Cell) -> bool:
        """returns True if the cell is in the frontier"""
        return cell in self.__frontier

    def __iter__(self):
        """returns an iterator for the frontier"""
        return iter(self.__frontier)

    def start_cell(self, cell:Cell):
        """add a starting cell

        If the maze is not empty, a ValueError exception is raised.
        """
        if len(self.__maze) > 0:
            raise ValueError("The maze is not empty")
        if cell not in self.grid:
            raise ValueError("The start cell must be in the maze")
        self.__visited.add(cell)
        for nbr in cell.neighbors:
            if nbr not in self.__visited:
                self.__frontier.add(nbr)

    def trial_d(self, p:Cell, q:Cell):
        """compute the metric from a visited cell to a frontier cell"""
        if p not in self.__visited:
            raise ValueError("the source cell has not been visited")
        if q not in self.__frontier:
            raise ValueError("the target cell is not in the frontier")
        dist = float('inf')
        via = None
        for nbr in self.__shuffle(q):
            if nbr not in self.__visited:
                continue
            d = self.d(p,nbr) + 1
            if d < dist:
                dist = d
                via = nbr
        return dist, via

    def d(self, p:Cell, q:Cell) -> 'Real':
        """compute the metric between two visited cells"""
        if p == q:
            return 0
        return self.__distances[p][q]

    @property
    def distances(self) -> dict:
        """return the current distances map"""
        return self.__distances

    def _update_distances(self, fcell, via, cell, hop):
        """update the distances"""
                # add a hop to each current distance
        self.__distances[fcell][cell] = self.d(via, cell) + hop
        self.__distances[cell][fcell] = self.d(cell, via) + hop

    def _update_sets(self, fcell, cell):
        self.__frontier.remove(fcell)
        self.__visited.add(fcell)
        for nbr in fcell.neighbors:
            if nbr not in self.__visited:
                self.__frontier.add(nbr)

    def link(self, visited_cell:Cell, frontier_cell:Cell, hop=1) -> int:
        """link a cell"""
        if not self.is_visited(visited_cell):
            raise ValueError("The source is not a visited cell")
        if not self.in_frontier(frontier_cell):
            raise ValueError("The target is not a frontier cell")
        self.maze.link(visited_cell, frontier_cell, weight=hop)
                    # Update the distances -- this is a bottleneck!
                    #   worst case O(|V| log(|V|))
        for cell in self.__visited:
            self._update_distances(frontier_cell, visited_cell, cell, hop)
                    # Update the sets
        self._update_sets(frontier_cell, cell)

# END mazes.Metrics.hops
