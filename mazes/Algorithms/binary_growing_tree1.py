"""
mazes.Algorithms.binary_growing_tree1 - a growing tree algorithm for binary trees
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of a binary tree maze carver based on queue
    searches such as depth-first or breadth-first search.
    The basic algorithm as implemented here is cell-based roughly as follows:

        Place the start cell in the queue and mark it as visited
        Loop until the queue is empty:
            Pop a cell from the queue.
            if the cell has one or two unvisited neighbors:
                carve passages from the cell to the neighbors;
                mark the neighbors as visited
                place the neighbors in the queue.

    Note that the algorithm attempts to make the binary tree as full as
    possible when a cell is encountered.

ARITY

    The option "arity" can be use to create other types of (rooted) trees.
    The arity of a tree is the maximun number of children that any node
    can have.  The default, arity=2, yields binary trees.

    Setting arity=1 will yield a chain.  Arity=3 yields a ternary tree.
    Arity=infinity is a more general type of tree.  (Arity=0 yields
    a trivial tree consisting of a single cell.)

    Arity is not the same as degree.  If the starting cell has n neighbors,
    then under this algorithm, its degree will be the mininum of n and the
    arity.  (For the basic oblong grid, since every cell has 2, 3 or 4
    neighbors, with arity=2, the degree of the starting cell will be 2.)
    The starting cell may be viewed as the root of the tree.

    For the remaining visited cells, the degree of a cell will be the
    minimum of arity+1 and n+1 where n is the number of previously
    unvisited neighbors.  Except for the starting cell, each visited cell
    has a parent (previously visited) and, if there are previously
    unvisited neighbors.

REMARKS

    Some connected grid configurations do not admit binary spanning trees.  The
    simplest example is the following grid:

                    +---+
                    |   |           The unlabelled cells have cell X as their
                +---+---+---+       only neighbor, so any spanning tree (and)
                |   | X |   |       in fact the only spanning tree) has a
                +---+---+---+       passage from cell X to each of its neighbors.
                    |   |           Hence cell X is degree 4.
                    +---+

    In some cases, even when the grid is connected, the algorithm may fail to visit
    all cells.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Jamis Buck.  "Maze Algorithms".  Web.  Accessed 2 December 2025.
            https://www.jamisbuck.org/mazes/
        scroll down the page to "Growing Binary Tree Algorithm" for a
        demo.

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
from mazes import rng, Algorithm
from mazes.gqueue import GeneralizedQueue
from mazes.Queues.stack import Stack

class BinaryGrowingTree(Algorithm):
    """the growing tree binary maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Binary Growing Tree"

        __slots__ = ("__queue", "__visited", "__visit", "__arity")

                # QUEUE OPERATIONS

        def enter(self, cell):
            """place a cell in the queue"""
            self.__queue.enter(cell)

        def leave(self):
            """remove the cell in the front of the queue and return it"""
            return self.__queue.leave()

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__queue) == 0

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True,
                       arity:int=2, QueueType:callable=Stack,
                       qargs:tuple=tuple(), qkwargs:dict=dict()):

            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle (default: True) if False, neighbors are processed
                    first come, first served.

                arity (default: 2) the number of neighbors to enqueue. The
                    default guaranties that the resulting component is a
                    binary tree.  A value of 3 produces a ternary tree,
                    4 a 4-ary tree, etc.  (Note that some cells might end
                    up unvisited and thus isolated.)

                QueueType (default: Stack) - a queuing class

                qargs (default: ()) - constructor positional arguments for
                    the queuing class

                qkwargs (default: {}) - constructor keyword arguments for
                    the queuing class
            """
            if not issubclass(QueueType, GeneralizedQueue):
                raise TypeError("queuing type must derive from GeneralizedQueue")
            super().parse_args()                # chain to parent
            self.__visit = self.visit_shuffled if shuffle \
                else self.visit_in_order
            self.__queue = QueueType(*qargs, **qkwargs)
            self.__arity = arity

                # initialize the unvisited set and the queue
            if start_cell == None:
                unvisited = list(self.maze.grid)
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__visited = {start_cell}       # hash
            self.enter(start_cell)               # one cell

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 1)         # the start cell
            self.store_item("passages", 0)

        @property
        def more(self):
            """returns True if the queue is empty

            Overrides Algorithm.more.
            """
            return not self.is_empty

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit_in_order(self):
            """visit pass - unshuffled"""
            cell = self.leave()
            arity = self.__arity
            for nbr in cell.neighbors:
                if arity <= 0:
                    break                           # limit on children
                if nbr not in self.__visited:
                    self.link(cell, nbr)            # link to the first
                    self.__visited.add(nbr)
                    self.increment_item("cells")
                    self.enter(nbr)
                    arity -= 1

        def visit_shuffled(self):
            """visit pass - shuffled"""
            cell = self.leave()
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    nbrs.append(nbr)
            if not nbrs:
                return                              # nothing to do

            rng.shuffle(nbrs)
            arity = self.__arity
            for nbr in nbrs:
                if arity <= 0:
                    break                       # limit on children
                self.link(cell, nbr)                # link to it
                self.__visited.add(nbr)
                self.increment_item("cells")
                self.enter(nbr)
                arity -= 1

        def visit(self):
            """wrapper for __visit"""
            self.__visit()

# end module mazes.Algorithms.binary_growing_tree1
