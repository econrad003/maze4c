"""
mazes.Algorithms.hierholzer - Hierholzer's algorithm for Eulerian tours
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Hierholzer's algorithm is named after Carl Hierholzer who, in 1871,
    proved Leohard Euler's conjecture [2] from 1735 that, if each of the
    vertices of a connected graph have even degree, then the graph will
    be connected.  The result was published posthumously in [3].

ALGORITHM

    Assuming the maze is Eulerian, choose an arbitrary starting edge.
    Find a closed walk in which an edge may appear at most once..  Mark
    the edges in walk as visited.

    While there are vertices in the walk which have unvisited edges:
        Choose one of these vertices:
            Find a closed walk from that vertex along unvisited edges,
            each edge used at most once; insert the walk into the tour
            and mark its edges as visited.

    The algorithm has O(|E|) time complexity (i.e. roughly linear in the
    number of edges).

REFERENCES

    [1] "Eulerian path" in Wikipedia.  8 Dec 2025. Web. Accessed
        3 Apr 2026.

    [2] Leonhard Euler (1707-1783). "Solutio problematis ad geometriam
        situs pertinentis" in Commentarii Academiae Scientiarum Imperialis
        Petropolitanae I, v 8 (1736), pp 128–140.

    [3] Carl Hierholzer (1840-1871), "Ueber die Möglichkeit, einen
        Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren" in
        Mathematische Annalen, v 6 (1), pp 30–32.

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
from collections import deque

from mazes import rng, Cell, Algorithm
from mazes.maze import Maze

NoneType = type(None)
DEBUG = False

class triple(tuple):
    """a wrapper for tuple

    It's an ordered triple (a, b, c) with an identifier attribute ('name').
    """

    def __new__(cls, a, b, c, NAME):
        """constructor"""
        return super(triple, cls).__new__(cls, tuple([a,b,c]))

    def __init__(self, a, b, c, NAME):
        """constructor"""
        self.name = NAME

    @property
    def name(self):
        """name getter"""
        return self.__name

    @name.setter
    def name(self, NAME):
        """name setter"""
        self.__name = NAME

class Hierholzer(Algorithm):
    """Hierholzer's algorithm for finding Eulerian tours"""

    class Status(Algorithm.Status):
        """the work happens here"""

        NAME = "Hierholzer's Algorithm"


        __slots__ = ("__odd", "__start", "__curr", "__trail",
                     "__unvisited", "__graph", "__first",
                     "nextID")

        def parse_args(self, start_cell:(Cell, NoneType)=None):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class

            KEYWORD ARGUMENTS

                start_cell - starting cell for the tour.  If there is a
                    cell with odd degree, one such cell must be specified
                    as the starting cell, otherwise the algorithm will fail.
                    If the starting cell is odd, the walk will end in another
                    cell of odd degree.  If all cells have even degree, the
                    starting cell is optional.

                    If there are more than two odd cells, the walk will not
                    encompass all of the edges.
            """
            self.__start = start_cell

        def initialize(self):
            """initialization"""
            self.__graph = dict()
            self["isolated cells"] = 0
            self.__odd = set()
            self.__unvisited = set(self.maze)
            for cell in self.maze.grid:
                passages = list(cell.joins)
                if passages:
                    rng.shuffle(passages)
                    self.__graph[cell] = passages
                    if len(passages) % 2 == 1:
                        self.__odd.add(cell)
                else:
                    self["isolated cells"] += 1
            if len(self.__odd) > 0 and self.__start not in self.__odd:
                msg = "There are cells of odd degree.  You must start in one."
                raise ValueError(msg)
            self.__trail = deque()
            self["packets"] = 0
            self["rejects"] = 0
            self["rotates"] = 0
            self.nextID = 0
                            
        def configure(self):
            """set up the first visit"""
            if isinstance(self.__start, Cell):
                self.__curr = self.__start
                self["start cell"] = self.__curr.index
            else:
                self.__curr = rng.choice(list(self.__graph.keys()))
                self["start cell"] = "any"
            self["first cell"]  = self.__curr.index
            if self.__curr in self.__graph:
                self.more = True
            else:
                self.more = False
                self["warning"] = "The first cell is isolated."

        @property
        def trail(self):
            """return the trail"""
            return list(self.__trail)

        def add_to_trail(self):
            """proceed from the current node"""
            join = self.__graph[self.__curr].pop()
            if len(self.__graph[self.__curr]) == 0:
                del self.__graph[self.__curr]       # done with the cell
            if join not in self.__unvisited:
                self["rejects"] += 1
                return                              # passage already used
            self.__unvisited.remove(join)
            next_cell = self.__curr.cell_for(join)
            packet = triple(self.__curr, join, next_cell, self.nextID)
            if DEBUG:
                print(f"ADD PACKET {self.nextID}:", self.__curr.index,
                      "--", next_cell.index)
            if len(self.__trail) == 0:
                self.__first = self.nextID
            self.nextID += 1
            self.__trail.append(packet)
            self.__curr = next_cell
            self["packets"] += 1

        def rotate(self):
            packet = self.__trail.pop()
            if DEBUG:
                print("ROTATE", f"{packet.name}:", packet[0].index,
                      "--", packet[2].index)
            self.__trail.appendleft(packet)
            self.__curr = packet[0]
            if packet.name == self.__first:            # full rotation
                self.more = False
            self["rotates"] += 1

        def visit(self):
            """visit"""
            if DEBUG:
                print("VISIT", self.__curr.index)
            if self.__curr in self.__graph:
                self.add_to_trail()
            else:
                self.rotate()
            
