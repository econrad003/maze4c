"""
mazes.Algorithms.dfs_circuit_locator - the depth-first search maze circuit locator
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a variation of the DFS algorithm which is used to locate
    a circuit in an undirected maze.

REFERENCES

    [1] "Cycle (graph theory)" in Wikipedia. 13 Nov 2025. Web
        Accessed: 17 Nov 2025.
            URL: https://en.wikipedia.org/wiki/Cycle_(graph_theory) 

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

class _StackEntry(object):
    """contains the cell and all unprocessed joins"""

    __slots__ = ("__cell", "__joins", "__arc")

    @staticmethod
    def shuffle(unshuffled) -> list:
        """shuffles and returns"""
        result = list(unshuffled)
        rng.shuffle(result)
        return result

    def __init__(self, cell:"Cell", arc:"Join", randomize:bool=True):
        """constructor"""
        self.__cell = cell
        self.__arc = arc
        self.__joins = iter(self.shuffle(cell.joins) \
            if randomize else cell.joins)

    @property
    def cell(self):
        """return the cell"""
        return self.__cell

    @property
    def join(self):
        """return the next join

        The value None is return if there are no more joins.
        """
        try:
            return next(self.__joins)
        except StopIteration:
            return None

    @property
    def arc(self):
        """the arc which delivered the cell"""
        return self.__arc

class CircuitFinder(Algorithm):
    """a depth-first search circuit-locator algorithm

    USAGE

        The status must be queried to determine the result:

            status = CircuitFinder,on(maze)
            print(status)
            if status.result:
                cell, join, nbr = status.result
                print("top cell in stack:", cell)
                print("earlier in stack:", nbr)
                print("the edge or arc in the circuit", join)
            else:
                print("No circuits")

        If you just want to remove the circuit:
            maze.unlink(join)

        If you want to find the cells that form the circuit, you
        need pop stack entries to find "nbr" in the stack.            
    """

    class Status(Algorithm.Status):
        """this is where the bulk of the work is done"""

        NAME = "DFS Circuit Locator"

        __slots__ = ("__stack", "__unvisited", "__finished",
                     "__randomize", "__result", "__maxlen",
                     "__more")

                # STACK OPERATIONS

        def push(self, cell, arc):
            """push the data onto the stack and mark cell as visited"""
            item = _StackEntry(cell, arc, randomize=self.__randomize)
            self.__stack.append(item)
            self.__unvisited.remove(cell)
            self.increment_item("cells visited")
            if len(self.__stack) > self.__maxlen:
                self.__maxlen = len(self.__stack)
                self.store_item("maximum stack depth", self.__maxlen)

        def pop(self) -> _StackEntry:
            """pop and return the top of the stack"""
            return self.__stack.pop()

        @property
        def top(self) -> _StackEntry:
            """return the top of the stack"""
            return self.__stack[-1]

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__stack) == 0

        def label_circuit(self, label="*"):
            """label the circuit, if any"""
            cells = self.circuit
            for cell in cells:
                cell.label = label

        @property
        def circuit(self) -> list:
            """label the circuit that was found

            The empty list is returned if there is no circuit
            """
            result = list()
            if self.result:
                cell1, edge, cell2 = self.result
                n = -1
                item = self.__stack[n]
                while item.cell != cell2:
                    result.append(item.cell)
                    n -= 1
                    item = self.__stack[n]
                result.append(cell2)
            return result

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)
            """
            super().parse_args()                # chain to parent

                # initialize the unvisited set and the stack
            unvisited = list(self.maze.grid)
            if start_cell == None:
                start_cell = rng.choice(unvisited)
            self.__randomize = shuffle
            self.store_item("start cell", start_cell.index)
            self.store_item("components found", 1)
            self.store_item("components finished", 0)
            self.store_item("cells visited", 0)         # the start cell
            self.store_item("shuffle", shuffle)
                # we keep track of unvisited cells in the
                # event that the maze is disconnected
            self.__unvisited = set(unvisited)   # hash
            self.__finished = set()
            self.__stack = list()
            self.__maxlen = 0
            self.__more = True
            self.push(start_cell, None)             # one cell, no arc

        @property
        def more(self):
            """returns True if the stack is empty

            Overrides Algorithm.more.
            """
            return self.__more

        @property
        def result(self):
            """returns the an item in the circuit or None"""
            return self.__result

        def visit(self):
            """wrapper for __visit"""
            if self.is_empty:                   # stack is empty
                self.increment_item("components finished")
                if len(self.__unvisited) == 0:
                    self.__more = False
                    self.store_item("circuit", "None")
                    self.__result = None
                    return                      # all cells visited
                        # there is another component
                self.increment_item("components found")
                component = self["components found"]
                start_cell = rng.choice(list(self.__unvisited))
                self.store_item(f"start cell {component}", start_cell.index)
                self.push(start_cell, None)

            cell = self.top.cell
            join = self.top.join
            if join == None:            # all joins processed
                self.pop()
                self.__finished.add(cell)
                return
            nbr = cell.cell_for(join)
            if cell == nbr:             # this might be a loop
                self.__more = False
                self.__result = (cell, join, nbr)
                self.store_item("circuit", (cell.index, cell.index))
                self.store_item("loop", True)
                return
            if join == self.top.arc:
                return                  # arrived by this edge
            if nbr in self.__finished:
                return                  # not in a circuit
            if nbr in self.__unvisited:
                self.push(nbr, join)        # recurse
            else:
                self.__result = (cell, join, nbr)
                self.store_item("circuit", (cell.index, nbr.index))
                self.__more = False     # circuit located

# end module mazes.Algorithms.dfs_circuit_locator
