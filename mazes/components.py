"""
mazes.components - tools for managing components
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The following classes are defined:

        ComponentRegistry - used to identify components
        GridComponents - depth-first search to find the components in an
            undirected grid
        MazeComponents - depth-first search to find the components in an
            undirected maze

BACKGROUND

    A non-empty set of vertices and edges in a graph forms a connected set in
    the graph if and only if:
        (i) between any pair of vertices in the set, there is a path in the set
            that joins them; and
        (ii) the set contains each vertex that is incident to an edge in the
            set.
    The definition applies equally to cells and grid edges in an undirected
    grid, and to cells and passages in an undirected maze.  For networks
    containing arcs, there are some generalizations of this notion.

    We will use the following simple graph as an example:

        A -- B    E    F
           / |         |        Figure 1. A disconnected simple graph.
          /  |         |
        D -- C         G

    For the edges in the graph, we use a pair of lower case letters, in
    alphabetic order and corresponding to the capital letters used to label
    the vertices.  For example ab and cd are respectively the edge joining A
    B and the edge joining C and D.

    The sets {A}, {A, B, ab}, {A, B, C, D, ab, bc, bd}, and {A, B, C, D, ab,
    bc, bd, cd} all form connected sets, but the sets {A, B}, {A, B, C, ab},
    {A, ab}, and {A, E} do not.  Of the sets in the latter group, the first
    three can be extended to connected sets, but the last cannot:

        (i) adding edge ab to {A, B} connects the set;
        (ii) adding edge bc to {A, B, C, ab} connects the set;
        (iii) adding vertex B to {A, ab} connects the set;
        (iv) there is no path from A to E, so {A, E} is not a subset of any
            connected set.

    A maximally connected set of vertices and edges forms a component.  The
    graph above has three components:
        S1 := {A, B, C, D, ab, bc, bd, cd},
        S2 := {E}, and
        S3 := {F, G, fg}.

    A vertex which has no incident edges is an isolated vertex.  So vertex E
    in S2 is an isolated vertex.  There are no other isolated vertices in the
    graph of Figure 1.

    Note that, if vertex E were to have an incident loop (e.g. an edge ee),
    then it would no longer be isolated.  (Figure 1 would become a pseudograph
    with this change.  It would no longer be simple.)

    Let T := S1 \ {ab} = {A, B, C, D, bc, bd, cd}.  Then T is not a connected
    set.  An edge in a connected set which, when removed, disconnects the set
    is called a bridge in the set.  For a connected graph, a bridge is an edge
    whose removal disconnects the graph.

    A 2-connected set (graph) is a connected set (graph) which has no bridges.
    In Figure 1, components S1 and S3 have bridges, so neither component forms
    a 2 connected set.  But component S2 has no bridges, so it is a (trivially)
    2-connected set.

    More generally, an n-connected set (graph) is a connected set (graph) in
    which we can remove any set of at most (n-1) edges without disconnecting
    the set (graph).

    Note that a graph is 1-connected if and only if it is connected.  Also
    note that if a graph is (n+1)-connected, then it also n-connected.

    A connected set containing a single vertex (with 0 or more incident loops)
    is (by definition) ∞-connected.

    The empty set is (by definition) disconnected.  A connected set with n
    vertices must have at least n-1 edges.

    Now consider the following simple graph:

           B
          /|\             Figure 2. A 2-connected simple graph which is not
        A -+- C                3-connected
          \|/
           D

    Any of the six edges can be removed without disconnecting the graph of
    Figure 2.  So there are no bridges.  In fact, we can remove any pair of
    edges and the graph will still be connected.  But if we remove all three
    edges incident to one of the four vertices (for example: ab, ac and ad,
    all incident to A), then the graph is no longer connected.  So the graph
    of Figure 2 is 2-connected, but not 3-connected.

    (The graph of Figure 4 is known as K₄, the complete graph on four
    vertices.  The K stands for Kuratowski.  "Complete" refers to the fact
    that there is an edge between each pair of distinct vertices.  So K₄ is
    a minimally complete graph.  We could add loops or parallel edges to get
    larger complete graphs on the same set of vertices.  Technically it is an
    isomorphism class -- if we hide all the labels and consider only the
    structural relationships in the graph, we have an isomporhism class.)

    We can also consider removing vertices.  When we remove a vertex, we need
    remove all of its incident edges.  For example, consider the following
    graph:

        A : B : C         Figure 3.  A bipartite multigraph.

    The colons indicate the edges come in parallel pairs, so this graph has
    four edges.  Extending the edge-naming convention above, we'll call them
    ab1 and ab2 (between A and B) and bc1 and bc2 (between B and C).

    The graph is a multigraph since there are pairs of parallel edges.  The
    graph is bipartite since we can partition the vertices into two sets each
    of which contains no adjacent vertices.  For this graph, the partition is
    {{A, C}, {B}}.  There are no loops and there are no edges between A and C.
    Note that this graph is 2-connected -- there are no bridges.  But if I
    remove just one carefully chosen vertex (along with its incident edges),
    then I can disconnect the graph.  The carefully chosen vertex is B.
    Removing B coincidentally removes all four edges and leaves no path
    joining A and C.  The vertex B is a vertex cut of A and C since all paths
    between A and C pass through B.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] "Connectivity (graph theory)" in Wikipedia. 26 September 2024. Web.
        Accessed 10 December 2024.
            URL: https://en.wikipedia.org/wiki/Connectivity_(graph_theory)

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

class ComponentRegistry(object):
    """for managing components in a graph or maze or grid"""

    __slots__ = ("__components", "__component_for", "__next_component")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, next_component:int=0):
        """constructor"""
        self.__components = dict()          # int : set
        self.__component_for = dict()       # object : int
        if type(next_component) != int:
            raise TypeError("'next_component' must be an integer")
        self.__next_component = next_component

    def register(self, vertex_or_edge) -> int:
        """assign a vertex or an edge to a component

        DESCRIPTION

            If the object is not in a component, then a new component (which
            contains the object) will be created.  If the object is already
            registered, no new component is created.

        ARGUMENTS

            vertex_or_edge - the object being assigned, typically a vertex
                (cell) or an edge (grid edge or passage), but it can be any
                hashable object

        RETURNS

            the component number
        """
            # is the object already registered?
        if vertex_or_edge in self.__component_for:
            # print("register", vertex_or_edge.index,
            #       self.__component_for[vertex_or_edge])
            return self.__component_for[vertex_or_edge]

            # is the next component # valid?
        if self.__next_component in self.__components:
            raise RuntimeError(f"component {self.__component} already exists")

            # get a new component number
        component = self.__next_component;
        self.__next_component += 1

            # register the component
        self.__components[component] = {vertex_or_edge}
        # print("register", vertex_or_edge.index, component, "NEW")
        self.__component_for[vertex_or_edge] = component
        return component

    def component_for(self, vertex_or_edge):
        """return the component number of an object

        IndexError is raised if the object is not registered.  (Use 'register'
        to avoid this exception.  Use this method to avoid the small amount
        of overhead associated with registering an aleady registered object.)
        """
        return self.__component_for[vertex_or_edge]

    def merge(self, component1:int, component2:int):
        """merge two components

        returns the number of the merged component
        """
            # validate component 1
        if component1 not in self.__components:
            raise ValueError("'component1' is not a component")
        if component1 == component2:
            return component1               # nothing to do

            # validate component 2
        if component2 not in self.__components:
            raise ValueError("'component2' is not a component")

            # perform the merge
        if component1 < component2:
            return self.__merge(component1, component2)
        return self.__merge(component2, component1)

    def __merge(self, k1, k2):
        """the merger method (called by merge)"""
        # print("merge", k1, k2)
        for item in self.__components[k2]:
            self.__component_for[item] = k1
        # print(k1, self.__components[k1])
        # print(k2, self.__components[k2])
        self.__components[k1].update(self.__components[k2])
        del self.__components[k2]
        return k1

    def are_connected(self, obj1, obj2):
        """returns True if the objects are registered in the same component"""
        return self.register(obj1) == self.register(obj2)

    def __len__(self):
        """return the number of components in the registry"""
        return len(self.__components)

    @property
    def components(self) -> list:
        """return the registered components"""
        return list(self.__components.keys())

    def items_in(self, component) -> list:
        """return the registered items in the component"""
        return list(self.__components[component])

class GridComponents(object):
    """determine the components in an undirected grid

    The results are undefined for a directed grid.  No exception is raised.
    """

    __slots__ = ("__grid", "__registry")

    def __init__(self, grid:"Grid"):
        """constructor"""
        self.__grid = grid
        self.__registry = ComponentRegistry()
        self.__dfs()

    def __dfs(self):
        """depth-first search to find components"""
        unreached = list(self.__grid)
        unvisited = set(self.__grid)
                # outer loop
        while unvisited:
            start = unreached.pop()         # get a starting point
            stack = [start]                 # initialize the stack
            unvisited.remove(start)         # mark the start cell as visited
                    # middle loop
            while stack:
                cell = stack[-1]                # top
                k1 = self.__registry.register(cell)
                self.__dfs_inner(cell, k1, stack, unvisited)
                    # stack empty
            unreached = list(unvisited)

    def __dfs_inner(self, cell, k1, stack, unvisited):
        """the innermost loop in DFS"""
            #
            # list and set are mutable so we don't need to declare them
            # as globals
            #
        for nbr in cell.neighbors:
            if nbr in unvisited:
                unvisited.remove(nbr)   # mark it visited
                    # the neighbor is in the same component as the cell
                k2 = self.__registry.register(nbr)
                self.__registry.merge(k1, k2)
                stack.append(nbr)       # place it on the stack
                return                  # exit the inner loop early
        stack.pop()             # no unvisited neighbors

    @property
    def grid(self):
        """grid getter"""
        return self.__grid

    @property
    def registry(self):
        """registry getter"""
        return self.__registry

class MazeComponents(object):
    """determine the components in an undirected maze

    The results are undefined for a directed maze.  No exception is raised.
    """

    __slots__ = ("__maze", "__registry")

    def __init__(self, maze:"Maze"):
        """constructor"""
        self.__maze = maze
        self.__registry = ComponentRegistry()
        self.__dfs()

    def __dfs(self):
        """depth-first search to find components"""
        grid = self.__maze.grid
        unreached = list(grid)
        unvisited = set(grid)
                # outer loop
        while unvisited:
            start = unreached.pop()         # get a starting point
            stack = [start]                 # initialize the stack
            unvisited.remove(start)         # mark the start cell as visited
                    # middle loop
            while stack:
                cell = stack[-1]                # top
                k1 = self.__registry.register(cell)
                self.__dfs_inner(cell, k1, stack, unvisited)
                    # stack empty
            unreached = list(unvisited)

    def __dfs_inner(self, cell, k1, stack, unvisited):
        """the innermost loop in DFS"""
            #
            # list and set are mutable so we don't need to declare them
            # as globals
            #
        for nbr in cell.passages:
            if nbr in unvisited:
                unvisited.remove(nbr)   # mark it visited
                    # the neighbor is in the same component as the cell
                k2 = self.__registry.register(nbr)
                self.__registry.merge(k1, k2)
                stack.append(nbr)       # place it on the stack
                return                  # exit the inner loop early
        stack.pop()             # no unvisited neighbors

    @property
    def maze(self):
        """maze getter"""
        return self.__maze

    @property
    def registry(self):
        """registry getter"""
        return self.__registry

# end module mazes.components