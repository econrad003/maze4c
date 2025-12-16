"""
mazes.Algorithms.boruvka - Borůvka's minimum weight spanning tree algorithm
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An underlying assumption is that each edge has a unique weight and the
    weights are linearly ordered.  If a weight is duplicated, then the
    resulting maze (or graph) might contain circuits.

    As with Kruskal's algorithm, Borůvka's algorithm works by joining
    forests.  Kruskal's algorithm is serial -- just one pair of components
    is joined in each step.  Borůvka's algorithm is parallel, at least in
    principle -- all components are processed in each step.  (The
    implementation here is serial.)

    The algorithm was first published in 1926 by Otakar Borůvka for
    Moravia's electrical network.  It was rediscovered several by a number
    of people (including Gustave Choquet in 1938, both Jan Łukasiewicz and
    Hugo Steinhaus, among others, in 1951, and Georges Sollin in 1965.)
    It is also known as Sollin's algorithm. [1]

ALGORITHM (PARALLEL)

    while there are grid edges to process:
        let S = {cheapest edge from each component to any other component}
        for each edge in S:
            carve a passage on the edge
        (discard all edges that are internal to a component)

REFERENCES

[1] "Borůvka's algorithm" in Wikipedia, 27 Mar. 2025. Web. Accessed 9 Dec. 2025.
        https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm

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
from mazes import rng, Algorithm
from mazes.maze import Maze
from mazes.components import ComponentRegistry, MazeComponents

def generate_weights(maze:Maze) -> dict:
    """create a set of unique linearly ordered weights

    The weights are ordered pairs (c, n) where:
        *   c is a randomly generated cost in the interval [0,1]; and
        *   n is a unique randomly assigned integer.

    The dictionary maps the grid edges to the weights.
    """
    joins = list(maze)
    rng.shuffle(joins)
    weights = dict()
    n = 0
    for cell in maze.grid:
        for nbr in cell.neighbors:
            edge = frozenset([cell, nbr])
            weight = rng.random(), n        # generate the ordered pair
            n += 1
            weights[edge] = weight
    return weights

class Boruvka(Algorithm):
    """Borůvka's minimum weight spanning tree algorithm"""

    class Status(Algorithm.Status):
        """workhorse for Borůvka's algorithm"""

        __slots__ = ("__registry", "__weights", "__edges", "__verify",
                     "cheapest")

        NAME = "Borůvka's minimum weight spanning tree algorithm"

        def discard_unwanted_edges(self):
            """discard edges in the same component"""
            wanted = set()
            for edge in self.__edges:
                cell1, cell2 = edge
                if self.__registry.are_connected(cell1, cell2):
                    continue
                self["discards"] += 1
                wanted.add(edge)
            self.__edges = wanted

        def skip_verify(self):
            """don't raise a warning"""
            self["circuit detected"] = True

        def verify(self):
            """don't raise a warning"""
            raise Warning("circuit detected")

        def link(self, edge:frozenset):
            """carve a passage"""
            cell1, cell2 = edge
            self.maze.link(cell1, cell2)
            self["passages"] += 1
            self["links"] += 1
            component1 = self.__registry.component_for(cell1)
            component2 = self.__registry.component_for(cell2)
            if component1 == component2:
                self.__verify()
            else:
                self.__registry.merge(component1, component2)
                self["merges"] += 1

        def update(self, edge, component) -> bool:
            """is the edge preferred for the component?"""
            w = self.cheapest.get(component)
            if w == None or self.__weights[edge] > self.__weights[w]:
                self.cheapest[component] = edge

        def visit(self):
            """visit (simulated parallel)

            A lot of this could happen in parallel, but this is a serial
            implementation.

            For each pair of components, determine the cheapest edge.
            Carve passages from all such edges.  Then remove all
            redundant edges.
            """
                    # find the set of cheapest edges
            self.cheapest = dict()
            for edge in self.__edges:
                self["visits (serial)"] += 1
                cell1, cell2 = edge
                component1 = self.__registry.component_for(cell1)
                component2 = self.__registry.component_for(cell2)
                self.update(edge, component1)
                self.update(edge, component2)
            cheapest = set(self.cheapest.values())
                    # carve passages from these edges
            for edge in cheapest:
                self.link(edge)
                self.__edges.remove(edge)
                    # discard redundant edges
            self.discard_unwanted_edges()

        @property
        def more(self):
            """are there some edges to process?"""
            self["components (out)"] = len(self.__registry)
            return len(self.__edges) > 0

        def parse_args(self, edge_weights:dict=None, verify:bool=False):
            """argument parser

            POSITIONAL ARGUMENTS

                maze - a maze object.  If there are passages, then a preliminary
                    component analysis is done using depth-first search.

            KEYWORD ARGUMENTS

                edge_weights - a dictionary mapping grid edges to weights.  The
                    weights should be linearly ordered and unique.  (Non-unique
                    weight may lead to circuits.)  The edges are frozenset objects
                    that contain pairs of cells.

                    If no weights are provided (default), a weight dictionary is
                    automatically generated.

                verify - if True, a Warning exception is raised if an added passage
                    creates a circuit.  This can only happen if the weight map
                    is not one-to-one.
            """
            if bool(edge_weights):
                if isinstance(edge_weights, dict):
                    self.__weights = edge_weights
                else:
                    raise TypeError("passage weights should be in a dictionary")
            else:
                self.__weights = generate_weights(self.maze)
            self.__verify = self.verify if verify else self.skip_verify

        def initialize(self):
            """initialize the components registry"""
            self["cells"] = len(self.maze.grid)
            if len(self.maze) > 0:
                self["passages (in)"] = len(self.maze)
            self["passages"] = len(self.maze)
            self["visits (serial)"] = 0
            self["discards"] = 0
            self["links"] = 0
            self["merges"] = 0
            components = MazeComponents(self.maze)
            self.__registry = components.registry
            self["components (in)"] = len(self.__registry)
            self.__edges = set()
            for edge in list(self.__weights.keys()):
                if len(edge) == 1:          # loop
                    continue
                cell1, cell2 = edge
                if self.__registry.are_connected(cell1, cell2):
                    continue
                self.__edges.add(edge)

# END mazes.Algorithms.boruvka
