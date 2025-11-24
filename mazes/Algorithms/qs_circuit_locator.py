"""
mazes.Algorithms.qs_circuit_locator - a queue-based search maze circuit locator
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module uses of a queue-based search to locate a circuit in an
    undirected maze.

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
from mazes.gqueue import GeneralizedQueue
from mazes.Queues.stack import Stack

class _QueueEntry(object):
    """contains the cell, the active join, and all unprocessed joins.

    The active join was used to reach the cell from its predecessor.  It is
    thus treated as an arc.
    """

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
    """a queue-based search circuit-locator algorithm

    USAGE

        The status must be queried to determine the result:

            status = CircuitFinder,on(maze)
            print(status)
            if status.result:
                cell, join, nbr = status.result
                print("cell in circuit:", cell)
                print("the edge or arc in the circuit", join)
                print("the other endpoint:", nbr)
            else:
                print("No circuits")

        If you want to break the circuit:
            maze.unlink(join)

        There is not generally enough information in the queue to reconstruct
        the circuit.  One exception: the circuit can always be reproduced if
        the queue is last-in first-out (i.e. if the queue is a stack).
    """
    class Status(Algorithm.Status):
        """this is where the bulk of the work is done"""

        NAME = "Circuit Locator"

        __slots__ = ("__queue", "__priority",
                     "__unvisited_cells", "__visited_joins",
                     "__randomize", "__result", "__maxlen",
                     "__more", "__dump", "__name")

                # QUEUE OPERATIONS

        def enter(self, packet:_QueueEntry):
            """enter the data into the queue

            Also marks the cell and the join as visited.  The join is
            the edge or arc that was used to reach the cell.
            """
            self.__queue.enter(packet)
            if len(self.__queue) > self.__maxlen:
                self.__maxlen = len(self.__queue)
                self.store_item("maximum queue length", self.__maxlen)

            cell = packet.cell
            self.__unvisited_cells.remove(cell)
            self["cells visited"] += 1

            join = packet.arc
            if join:
                self.__visited_joins.add(join)

        def leave(self) -> _QueueEntry:
            """pop and return the top of the stack"""
            return self.__queue.jettison()

        @property
        def front(self) -> _QueueEntry:
            """return the top of the stack"""
            return self.__queue.top()

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__queue) == 0

                # POST MORTEM QUEUE ANALYSIS

        @property
        def post_mortem_dump(self) -> tuple:
            """dump the queue"""
            if self.__dump != None:
                return self.__dump
            dump = list()
            while not self.is_empty:
                packet = self.__queue.leave()
                cell = packet.cell
                arc = packet.arc
                item = (arc, cell)
                dump.append(item)
            self.__dump = tuple(dump)
            return self.__dump

        def label_pmqueue(self, label="Q"):
            """label cells in the post mortem queue"""
            dump = self.post_mortem_dump
            for item in dump:
                item[1].label = label

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True,
                       QueueType:callable=Stack, qargs:tuple=tuple(),
                       qkwargs:dict=dict()):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)  The default is True.

                QueueType - (default:Stack) the queuing class.  It must
                    be derived from class GeneralizedQueue.

                qargs - queuing class constructor arguments.  If supplied,
                    this is a tuple.  (default: an empty tuple)
                qkwargs - queuing class constructor arguments.  If supplied,
                    this is a dictionary whose keys are strings.  (default:
                    an empty dictionary)
            """
            super().parse_args()                # chain to parent
            if not issubclass(QueueType, GeneralizedQueue):
                raise TypeError("QueueType must be derived from GeneralizedQueue")
            self.__queue = QueueType(*qargs, **qkwargs)
            self["queuing class"] = QueueType.__name__
            self.__unvisited_cells = set(list(self.maze.grid))
            self.__visited_joins = set()
            self.__randomize = shuffle
            self["shuffle"] = shuffle
            self.__result = None                # nothing found (yet)
            self.__maxlen = 0
            self.__more = True
            self.__dump = None                  # see property post_mortem_dump()
            self["components found"] = 0
            self["components finished"] = 0
            self["cells visited"] = 0
            if start_cell == None:
                start_cell = rng.choice(list(self.maze.grid))
            self["start cell"] = start_cell.index
            self.start(start_cell)

        def start(self, cell:"Cell"):
            """seed the empty queue"""
            assert self.is_empty
            packet = _QueueEntry(cell, None, randomize=self.__randomize)
            self.enter(packet)
            self["components found"] += 1

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
            if self.is_empty:                   # queue is empty
                self["components finished"] += 1
                if len(self.__unvisited_cells) == 0:
                    self.__more = False             # done
                    self.store_item("circuit", "None")
                    return                      # all cells visited
                        # there is another component
                self["components found"] += 1
                start_cell = rng.choice(list(self.__unvisited_cells))   # 2025-11-23
                self.store_item(f"component start cell", start_cell.index)
                self.start(start_cell)

            cell = self.front.cell
            join = self.front.join
            if join == None:            # all joins processed
                self.leave()
                return
            nbr = cell.cell_for(join)
            if join in self.__visited_joins:
                    # this edge was already processed
                return
            if nbr in self.__unvisited_cells:
                    # one step further from start
                packet = _QueueEntry(nbr, join, randomize=self.__randomize)
                self.enter(packet)
                return
            self.__result = (cell, join, nbr)
            self.store_item("circuit", (cell.index, nbr.index))
            self.__more = False         # circuit located

# end module mazes.Algorithms.qs_circuit_locator
