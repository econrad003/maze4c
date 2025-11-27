"""
mazes.Wallbuilders.pruning_tree - finding a spanning tree by pruning edges
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The pruning_tree algorithm is a sort of growing tree in reverse.  With
    the growing tree algorithms, we begin with an empty maze, and starting
    with a single cell, we add edges, one at a time, to connect cells in the
    growing tree to cells in the frontier.  If the grid is connected, the
    end result is a spanning tree on the grid.

    With the pruning tree, we reverse the process. We begin with a connected
    maze which may contain circuits, Using just one search task, we start with
    a cell an traverse all the edges,  If we arrive at an edge which brings us
    to an already visited cell, we delete the edge.

    This differs from the naïve approach in "basic wallbuilder" and its
    derivatives in two important respects:

        (i)  in basic wallbuilder, each time we found an edge, we deleted it
             and started a completely new search; and

        (ii) our circuit locators used their queues a bit differently; here
             when we visit a cell or passage in the front of the queue, we will
             place its entire frontier in the queue.

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
from mazes import rng, Algorithm, Cell

from mazes.gqueue import GeneralizedQueue
from mazes.Queues.stack import Stack

class _CellData(object):
    """cell-based auxiliary data"""

    slots = {"__joins"}

    def __init__(self, cell:'Cell', shuffle:bool=True):
        """constructor"""
        joins = list(cell.joins)
        if shuffle and len(joins) > 0:
            rng.shuffle(joins)
        self.__joins = iter(joins)

    @property
    def next_join(self) -> "Passage":
        """return the next join in the iteration (destructive)"""
        try:
            return next(self.__joins)
        except StopIteration:
            return None

class PruningTree(Algorithm):
    """a wallbuilding algorithm that uses a search tree to prune passages"""

    class Status(Algorithm.Status):
        """where all the work is done"""

        __slots__ = ("__queue", "__more", "__shuffle", "__start",
                     "__unvisited", "__reached", "__visited",
                     "__visit")

        def enter(self, packet):
            """place a packet into the queue"""
            self["arrivals"] += 1
            self.__queue.enter(packet)

        def leave(self) -> tuple:
            """pop and return the entry at the top or front of the queue"""
            self["departures"] += 1
            packet = self.__queue.leave()
            return packet

        @property
        def top(self) -> tuple:
            """return the entry at the top or front of the queue"""
            return self.__queue.top()

        def jettison(self):
            """pop entry at the top or front of the queue"""
            self["departures"] += 1
            self.__queue.jettison()

        @property
        def is_empty(self):
            """determines whether the queue is empty"""
            return len(self.__queue) <= 0

        def unlink(self, passage:'Join'):
            """remove a passage (erect a wall)"""
            self.maze.unlink(passage)
            self["unlinks"] += 1

        @property
        def unprocessed(self) -> set:
            """returns the set of cells or passages that haven't been visited

            If this set is not empty, then the maze is disconnected.
            """
            return set(self.__unvisited)

        @property
        def start(self) -> tuple:
            """returns the starting cell and the visit type

            This is for derived classes that use a queue protocol that doesn't
            involve just cells or passages.

            Note that derived classes that use a protocol other than cell only
            or passage only must handle two NotImplementedError exceptions in,
            class PruningTree.Status, namely one in method initialize() and the
            other in method configure().
            """
            return self.__start, self.__visit_type

        def visit_cell(self):
            """visit method when cells are queued"""
            cell = self.top                 # top entry
            if cell in self.__unvisited:    # the active cell not been reached
                self.__unvisited.remove(cell)
                self.__reached[cell] = _CellData(cell, self.__shuffle)
            join = self.__reached[cell].next_join
            if join == None:
                self.jettison()                 # work complete for cell
            elif join in self.__visited:
                pass                            # this edge has been processed
            else:
                self.__visited.add(join)
                nbr = cell.cell_for(join)
                if nbr in self.__reached:       # a circuit has been completed
                    self.unlink(join)
                    # print(cell.index, "==", nbr.index, "Unlink")
                else:
                    self.__reached[nbr] = True
                    self.enter(nbr)
                    # print(cell.index, "==", nbr.index, "Enqueue")

        def visit_passage(self):
            """visit method when joins are queued"""
            join = self.leave()         # pop the top entry
            if join in self.__visited:
                return                          # already visited
            self.__visited.add(join)

            cells = join.cells
            if len(cells) == 1:
                    # it's a loop (trivial circuit)
                self.unlink(join)
                self["loops removed"] += 1
                return
            cell1, cell2 = cells
            joins = list()
            if cell1 in self.__unvisited:
                joins += list(cell1.joins)
                self.__unvisited.remove(cell1)
                if cell2 in self.__unvisited:
                        # neither cell visited
                    joins += list(cell2.joins)
                    self.__unvisited.remove(cell2)
            elif cell2 in self.__unvisited:
                    # neither cell visited
                joins += list(cell2.joins)
                self.__unvisited.remove(cell2)
            else:
                    # both cells already visited: circuit detected
                self.unlink(join)
                return
            if self.__shuffle:
                rng.shuffle(joins)
            for join in joins:
                if join not in self.__visited:
                    self.enter(join)
 
        def visit(self):
            """wrapper for visit"""
            self.__visit()

        @property
        def more(self):
            """wrapper for more"""
            if self.is_empty:
                self["unprocessed"] = len(self.__unvisited)
                self["passages"] = len(self.maze)
                self["maximum queue length"] = self.__queue.maxlen
                self["average queue length"] = self.__queue.mean
                return False
            return True

        def parse_args(self, shuffle:bool=True, start_cell:Cell=None,
                       QueueType:"class"=Stack, qargs=tuple(), qkwargs=dict(),
                       visit_type="cell"):
            """parse the setup arguments

            REQUIRED ARGUMENTS

                maze - a maze object in which walls need to be erected

            KEYWORD ARGUMENTS

                shuffle (default: True) - if False, a cell's neighbors will
                    be traversed in dictionary order.  If true, the neighborhood
                    will be shuffled.

                start_cell (default: None) - if a starting cell is supplied,
                    all circuit location passes will start there.

                    If the maze is disconnected, the search will always start
                    in the component containing the start cell.  For the
                    remaining components, the search will start in a random cell.

                QueueType (default: None) - if None, then the queuing class will
                    be the default, if any, for the CircuitFinder class.  (This
                    will normally be a stack.)  If a class is specified, then the
                    queue will be set up as:
                        q = QueueType(*qargs, **qkwargs)

                    The default for qargs, an empty tuple, results in queue setup
                    as:
                        q =QueueType(**qkwargs)

                    The default for qkwargs, an empty dictionary, results in queue
                    setup as:
                        q =QueueType(*qargs)

                    If the default is taken for both qargs and qkwargs, then
                    the setup is:
                        q =QueueType()

                qargs - see QueueType

                qkwargs - see QueueType

                visit_type - either "cell" or "passage"
            """
            super().parse_args()

            if not issubclass(QueueType, GeneralizedQueue):
                raise TypeError("QueueType must be derived from GeneralizedQueue")
            self.__queue = QueueType(*qargs, **qkwargs)
            self["queuing structure"] = QueueType.__name__

            self.__shuffle = bool(shuffle)
            self.__unvisited = set(self.maze.grid)
            if start_cell == None:
                start_cell = rng.choice(list(self.maze.grid))

                    # check the starting cell
            if not isinstance(start_cell, Cell):
                raise TypeError("start cell type is a sunclass of Cell")
            if start_cell not in self.__unvisited:
                raise ValueError("start cell not in grid")
            self.__start = start_cell
            self.__visit = visit_type

        def initialize(self):
            """initialization"""
            super().initialize()
            self["unlinks"] = 0
            self["arrivals"] = 0
            self["departures"] = 0
            self.__visited = set()          # passages that have been reached
            self.__reached = dict()         # cell -> iter(passages)
            self["visit type"] = self.__visit
            if self.__visit in {"cell", "vertex", "node"}:
                        # visit cells
                self.__visit = self.visit_cell
            elif self.__visit in {"passage", "join", "edge", "arc"}:
                        # visit passages
                self.__visit = self.visit_passage
            else:
                        # trap this in derived classes
                raise NotImplementedError("unknown visit type")

        def configure(self):
            """initialization"""
            super().configure()
            self["start cell"] = self.__start.index

                    # seed the queue
            if self.__visit == self.visit_cell:
                self.enter(self.__start)
                return

                    # requires special handling for seeding the queue
            if self.__visit != self.visit_passage:
                raise NotImplementedError()

                    # seeds queue for passage visits
            self["loops removed"] = 0
            joins = list(self.__start.joins)
            if len(joins) == 0:
                return                                  # isolated start cell
            if self.__shuffle:
                rng.shuffle(joins)
            for join in joins:
                self.enter(join)                        # enter the join

        def resume(self, start_cell:Cell=None):
            """resume in another component"""
            if len(self.__unvisited) == 0:
                raise ValueError("all components have been processed")
            if start_cell == None:
                unvisited = list(self.__unvisited)
                start_cell = rng.choice(unvisited) if self.__shuffle \
                    else unvisited[0]
            if start_cell not in self.__unvisited:
                raise ValueError("start cell not in unvisited region")
            self.__start = start_cell
            self.configure()

            while self.more:
                self.increment_item("visits")
                self.visit()

# END mazes.Wallbuilders.pruning_tree
