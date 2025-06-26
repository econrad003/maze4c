"""
mazes.tools.distance_map - color gradient for distances
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This test uses a discrete distance-based color gradiant to color a maze.

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
from math import isnan

from mazes.Algorithms.dijkstra import Dijkstra, test

    # the new improved daddy long legs (23 Dec 2024)
from mazes.Graphics.oblong1 import Phocidae

class DistanceColoring(object):
    """for building colormaps of mazes

    The base class uses Dijkstra's algorithm to obtain path lengths. Build a
    subclass or a duck-class to do something different.
    """

    def __init__(self, maze, hot, cold, zero, source:'Cell'=None, **kwargs):
        """constructor"""
        self.maze = maze
        self.grid = maze.grid
        self.hot = hot              # close color (%red, %green, %blue)
        self.cold = cold            # far away color
        self.zero = zero            # source color
        self.source = source
        self.kwargs = kwargs
        self.initialize()
        self.configure()

    def initialize(self):
        """get the distances and the source"""
        self.get_distances(self.source)

    def get_distances(self, source:'Cell'):
        """get the distances vector"""
        if source:
            dijkstra = Dijkstra(self.maze, source)
        else:
            dijkstra = test(self.maze)
            self.source = dijkstra.source
        self.distances = {}
        self.max_distance = 0
        for cell in self.grid:
            distance = dijkstra.distance(cell)
            if isnan(distance):
                continue
            if distance == float('inf'):            # 21 June 2025
                continue
            self.distances[cell] = distance
            self.max_distance = max(distance, self.max_distance)
        if self.max_distance == 0:
            self.max_distance = 0.5         # avoid divide by zero

    def configure(self):
        """configuration"""
        hot, cold, dmax = self.hot, self.cold, self.max_distance
        gradients = {}
        for cell in self.distances:
            d = self.distances[cell]
            gradients[cell] = self.gradient(hot, cold, d, dmax) \
                if d>=0 else "red"
        if self.source:
            gradients[self.source] = self.zero
        self.gradients = gradients

    def gradient(self, hot:'rgb', cold:'rgb', d:int, dmax:int) -> 'rgb':
        """compute the interpolated color"""
        rgb = []
        for i in range(3):
            t0, t1 = hot[i], cold[i]
            t = t0 + (t1-t0) * d / dmax
            rgb.append(t)
        return tuple(rgb)

    def color(self, cell) -> 'rgb':
        """return the color information, if any"""
        return self.gradients.get(cell)

# end module tests.distance_map
