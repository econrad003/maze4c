"""
mazes.Algorithms.floyd - the Floyd/Warshall transitive closure algorithm
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

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

from mazes.maze import Maze

class TransitiveClosure(object):
    """find the transitive closure for a matrix"""

    __slots__ = ("__distances", "__matrix")

    def __init__(self, matrix:dict=dict()):
        """constructor"""
        self.matrix = matrix

    @property
    def D(self):
        """returns the distance matrix"""
        return self.__distances

    @D.setter
    def D(self, other):
        """returns the distance matrix"""
        self.__distances = other

    def d(self, cell1, cell2):
        """returns the directed distance between two cells"""
        return 0 if cell1 == cell2 else self.D[cell1][cell2]

    @property
    def matrix(self):
        """matrix getter"""
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix:dict):
        """matrix setter -- finds the closure"""
        self.__matrix = matrix
        self.initialize()
        self.configure()
        self.find_closure()

    def initialize(self):
        """initialization"""
        inf = lambda: float("inf")
        d = lambda: defaultdict(inf)            # cell : infinity
        self.D = defaultdict(d)                 # cell : (cell : infinity)

    def configure(self):
        """configuration"""
        for i in self.__matrix:
            for j in self.__matrix[i]:
                if i != j:                      # no loops!
                    self.D[i][j] = self.__matrix[i][j]

    def find_closure(self):
        """find the transitive closure

        THIS IS THE HEART OF THE ALGORITHM!

        Note that this is cubic in complexity.
        """
        for via in self.D:
            for src in self.D:
                if self.D[src][via] == float('inf'):
                    continue
                for sink in self.D:
                    if self.D[via][sink] == float('inf'):
                        continue
                    self.D[src][sink] = min(self.D[src][sink], \
                        self.D[src][via] + self.D[via][sink])

class Floyd(TransitiveClosure):
    """finds the hop distance between cells in a maze"""

    __slots__ = ("__maze", )

    def __init__(self, maze:Maze):
        """constructor"""
        self.maze = maze

    @property
    def maze(self):
        """get the maze"""
        return self.__maze

    @maze.setter
    def maze(self, maze:Maze):
        """set the maze and recalculate the hop distances"""
        self.__maze = maze
        M = defaultdict(dict)
        for join in maze:
            cells = join.cells
            if len(cells) == 1:
                continue
            i, j = cells
            M[i][j] = 1
            if isinstance(cells, (frozenset, set)):
                M[j][i] = 1
        self.matrix = M         # this will perform needed initialization

class Warshall(TransitiveClosure):
    """finds the edge-weight distance between cells in a maze"""

    __slots__ = ("__maze", "__allow_negative_weights", "__negative_weights")

    def __init__(self, maze:Maze, allow_negative_weights:bool=False):
        """constructor

        If negative weights are encountered and 'allow_negative_weights'
        is False, a ValueError exception is raised after configuration
        is complete.
        """
        self.__allow_negative_weights = bool(allow_negative_weights)
        self.maze = maze

    @property
    def maze(self):
        """get the maze"""
        return self.__maze

    @property
    def allow_negative_weights(self):
        """are negative weights allowed?"""
        return self.__allow_negative_weights

    @maze.setter
    def maze(self, maze:Maze):
        """set the maze and recalculate the hop distances"""
        negative_weights = 0
        self.__maze = maze
        M = defaultdict(dict)
        for join in maze:
            cells = join.cells
            weight = join.weight
            if weight < 0:
                negative_weights += 1
                weight = 0
            if len(cells) == 1:
                continue
            i, j = cells
            M[i][j] = min(weight, M[i][j])
            if isinstance(cells, (frozenset, set)):
                M[j][i] = min(weight, M[j][i])
        self.matrix = M         # this will perform needed initialization
        if negative_weights > 0:
            print(f"{negative_weights} edges or arcs with negative weights")
            if not self.allow_negative_weights:
                raise ValueError("negative weights were encountered")

# END mazes.Algorithms.floyd
