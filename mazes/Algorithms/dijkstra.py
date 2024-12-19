"""
mazes.Algorithms.dijkstra - Dijkstra's distance and shortest path algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of Dijkstra's algorithm for finding the distance
    and a shortest path between two points in a maze.  The distance algorithm
    proceeds as follows:

        Given:
            a maze, a source cell and an optional target cell;
            a function:
                weight(passage)
                    returns a non-negative value for each passage in the maze;
            a priority queue using the current distance from source.

        Result:
            Two functions:
                distance(sink)
                    returns the distance from the given source;
                via(sink)
                    returns the last step in a path from source to sink.

            If a target cell is given, these functions will not be completely
            resolved.

            If weight(passage)=1 for each passage in the maze, the distance
            function will measure the number of passages in a path from source
            to sink.

        Initialization:
            for every sink:
                distance(source, sink) = 0 if sink==source else infinity;
                via(source, sink) = None;
            place the source in the priority queue.

        Loop until the queue is empty or the target has been visited:
            remove the first cell in the priority queue;
            if it has not been visited:
                mark it as visited;
                for each passage leading to a neighbor:
                    if distance(neighbor) > distance(cell) + weight(passage):
                            # update the distance and via functions
                        distance(neighbor) = distance(cell) + weight(passage)
                        via(neighbor) = passage
                        place the neighbor in the queue

IMPLEMENTATION

    This is an instantiated class Dijkstra.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 35-44.

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
from numbers import Real
from mazes import rng
from mazes.Queues.priority_queue import PriorityQueue

class Dijkstra(object):
    """Dijkstra's algorithm for finding distances and shortest paths"""

    NAME = "Dijkstra's distance algorithm"

    __slots__ = ("__maze", "__source", "__target", "__weight",
                 "__distance", "__via", "__queue", "__visited",
                 "__random_weights")

    def __init__(self, maze:'Maze', source:'Cell', target:'Cell'=None,
                 weight:callable=None):
        """constructor

        REQUIRED ARGUMENTS

            maze - the maze to process

            source - the source cell

        OPTIONAL ARGUMENTS

            target (default: None) - an optional target cell.  The algorithm
                finished when either:
                    (i) all reachable cells have been visited; or
                    (ii) the target cell, if any has been visited.

            weight (default: unit_weight) - a function mapping each passage to
                a non-negative value.  If the value is infinite, the passage
                will be ignored.  If the value is negative, a ValueError
                exception will be raised.  The default is a function which
                sets the weight of every passage to 1.

                If the option "weight" is assigned the string value "random",
                weights will be assigned randomly. This option is intended
                primarily for use in testing.
        """
        self.__maze = maze
        self.__weight = weight if weight else lambda passage: 1
        if weight == "random":
            self.__random_weights = {}
            self.__weight = self.random_weight
        self.calculate(source, target)

    @property
    def maze(self):
        """returns the maze object"""
        return self.__maze

    @property
    def source(self):
        """returns the source cell"""
        return self.__source

    @property
    def target(self):
        """returns the target cell"""
        return self.__target

    def weight(self, passage) -> Real:
        """returns the weight of a passage"""
        wgt = self.__weight(passage)
        if not isinstance(wgt, Real): raise TypeError
        if wgt < 0: raise ValueError
        return wgt

    def distance(self, sink:'Cell') -> Real:
        """distance from source to sink

        A value of infinity means:
            (i) the sink is unreachable, if the target was not reached; or
            (ii) the sink wasn't visited when the target was reached.
        """
        return self.__distance.get(sink, float('inf'))

    def __len__(self):
        """the number of reachable cells"""
        return len(self.__distance)

    @property
    def farthest(self) -> 'Cell':
        """find the farthest reachable (and catalogued) cell"""
        cell = self.source
        for contender in self.__distance:
            if self.distance(contender) > self.distance(cell):
                cell = contender
        return contender

    def via(self, sink:'Cell') -> 'Cell':
        """return the cell before the sink in the path from source to sink

        A value of None means:
            (i) The sink is the source cell;
            (ii) the sink is unreachable, if the target was not reached; or
            (iii) the sink wasn't visited when the target was reached.
        """
        return self.__via.get(sink, None)

    def path_to(self, sink:'Cell') -> list:
        """returns the requested path as a list of cells"""
        rpath = [sink]
        while via := self.via(rpath[-1]):
            rpath.append(via)
        if rpath[-1] != self.source:
            return []               # no path found
        return list(reversed(rpath))

    def label_path(self, sink:'Cell', source_label:str='S', dest_label:str='T',
                   path_label = '*'):
        """mark the requested path"""
        for cell in self.path_to(sink):
            cell.label = path_label
            sink.label = dest_label
            self.source.label = source_label

    def calculate(self, source:'Cell', target:'Cell'=None):
        """sets the source and target and calculates the distances"""

            # INITIALIZE
        if source not in self.maze.grid:
            raise ValueError("the source cell was not found")
        self.__source = source
        self.__target = target
        self.__distance = {source:0}
        self.__via = {}
        self.__visited = set()
        self.__queue = PriorityQueue()
        self.enter(source, 0)

            # LOOP
        while target not in self.__visited and not self.is_empty:
            cell = self.leave()
            if cell in self.__visited:
                continue
            self.__visited.add(cell)
            for nbr in cell.passages:
                passage = cell.join_for(nbr)
                wgt = self.weight(passage)
                if wgt == float('inf'):
                    continue        # this passage is not available
                dist1 = self.distance(nbr)
                dist2 = self.distance(cell) + wgt
                if not (dist2 < dist1):
                    continue        # no improvement
                            # UPDATE
                self.__distance[nbr] = dist2
                self.__via[nbr] = cell
                self.enter(nbr, dist2)

    def enter(self, cell:'Cell', distance:'Number'):
        """place a cell in the queue"""
        self.__queue.enter(cell, priority=distance)

    def leave(self):
        """remove and return a cell from the queue"""
        return self.__queue.leave()

    @property
    def is_empty(self):
        """return True if the queue is empty"""
        return len(self.__queue) == 0

    def random_weight(self, passage):
        """primarily for testing

        This methods creates passage weights in conjunction with the
        constructor option "weight='random'".  An exception is raised if
        this method is called when that option was not set.

        The weights are uniformly random in [0,1).
        """
        if passage not in self.__random_weights:
            self.__random_weights[passage] = rng.random()
        return self.__random_weights[passage]

    @property
    def diameter(self):
        """if the maze is a tree, this give the length of a longest path"""
        if self.distance(self.target) != float("inf"):
                    # rerun with an empty target
            print("diameter: pass 1")
            self.calculate(self.source)
        else:
            print("diameter: pass 1 skipped")
        if len(self) < len(self.maze.grid):
            print("diameter: (warning) the maze is not connected")
            if len(self.maze) >= len(self.maze.grid):
                print("diameter: (warning) the maze is not a tree")
        print("diameter: pass 2")
        self.calculate(self.farthest)
        farthest = self.farthest
        print(f"diameter: start at {self.source.index},",
              f"farthest at {farthest.index}")
        print("The results may mislead if the maze is not a tree.")
        return self.distance(farthest)

def test(maze:'Maze') -> Dijkstra:
    """just run it"""
    cell = rng.choice(list(maze.grid))
    print(f"Dijkstra: starting at {cell.index}")
    dijkstra = Dijkstra(maze, cell)
    diameter = dijkstra.diameter
    print(f"{diameter=}")
    dijkstra.label_path(dijkstra.farthest)
    return dijkstra

# end module mazes.Algorithms.dijkstra