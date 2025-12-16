"""
mazes.Grids.complete - complete grid on a given number of vertices
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A complete graph on a set of vertices is a (simple) graph in which
    every vertex is adjacent to every other vertex.  For a vertex set
    with n vertices, with n>0, the usual notation is K(n) -- the K stands
    variously for "komplett" (one way of saying "complete" in German) or
    "Kuratowski" (after Polish mathematician Kazimierz Kuratowski, who
    characterized planarity in term of the complete graph K(5) and the
    complete bipartite graph K(3,3)).

    Accordingly, a complete grid is a grid for which every cell is
    grid-adjacent to every other cell.  For any integer n, in our
    implementation the cells are indexed by range(n), i.e. the integers
    from 0 through n-1, inclusive.  Here is one planar embedding of this
    particular representation of K(4):

                                    1
                                   /|\
                                  / | \              Figure 1. K(4)
                                 /  |  \
                                /   |   \
                               2----0----3
                                \       /
                                 +-----+

    Let k be at least 2.  A complete k-partite graph on a set of vertices
    is a (simple) graph in which:
        1) the vertices are partitioned into k non-empty sets:
                V(0), V(1), ... V(k-1);
        2) for each i and j from 0 through k-1, if i≠j, then each vertex
           in V(i) is adjacent to every vertex in V(j); and
        3) for each i from 0 through k-1, there are no edges between
           vertices in V(i).
    For a vertex set partitioned into k sets with n1, n2, ..., nk elements,
    the usual notation is K(n1,n2,...,nk) with again standing variously
    for German "komplett" or "Kuratowski".

    In our implementation, the complete k-partite grids are indexed by
    ordered pairs (a,b) where a is a number in range(k) which indicates the
    the part and b is a number in range(na) which indicates the cell in the
    given part.  Here is one planar embedding of this
    particular representation of K(3,2):

                          (0,0)
                         /     \
                        /       \                     Figure 2.  K(3,2)
                       /         \
                  (1,0)---(0,1)---(1,1)
                       \         /
                        \       /
                         \     /
                          (0,2)

    Note that K(n) for n>1 is isomorphic to (i.e. structurally the same as)
    K(1,1,...,1) where there are n ones.  K(1) is just a graph (or grid) with
    a single vertex (cell) and no edges.

USAGE

    Two classes are defined here:

        CompleteGrid(n)

        PartiteGrid(a, b, ...)

    CompleteGrid requires one positive integer.  PartiteGrid takes two or
    more positive integers.

COMPLEXITY

    K(n) has n vertices and n(n-1)/2 edges.  For example:
        *  K(4) has 4x3/2=6 edges (see Figure 1)
        *  K(5) has 5x4/2=10 edges
    v=n, e = O(n²)

    K(a,b) has a+b vertices and ab edges.  For example:
        *  K(2,2) has 4 vertices and 4 edges
        *  K(3,3) has 6 vertices and 9 edges
        *  K(4,4) has 8 vertices and 16 edges
        *  K(5,5) has 10 vertices and 25 edges
    For K(n,n): v=2n, e=n²
        *  K(3,2) and K(2,3) both have 5 vertices and 6 edges
        *  K(4,3) and K(3,4) both have 7 vertices and 12 edges
    If the vertex parts are O(n), then v=O(n) and e=O(n²).

    K(a,b,c) has a+b+c vertices and (b+c)(a+c)(a+b) edges.
        *  (b+c)(a+c)(a+b)
                = baa + bab + bca + bcb + caa + cab + cca + ccb
                = a²b + ab² + 2abc + a²c + ac² + b²c + bc²
    K(n,n,n) has 3n vertices and (2n)(2n)(2n)=8n³ edges.

    For K(a,b,c), if the vertex parts are O(n), then v=O(n) and e=O(8n³).

    For a k-partite graph, e = O(2^k v^k) = O((2v)^k)
"""
import mazes
from mazes.cell import Cell
from mazes.grid import Grid

class CompleteGrid(Grid):
    """Kuratowski complete grids"""

    __slots__ = ("__n", )

    def _parse_args(self, n):
        """constructor"""
        super()._parse_args()
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 1:
            raise ValueError("n must be a positive integer")
        self.__n = n

    def _initialize(self):
        """create the cells"""
        super()._initialize()
        for k in range(self.__n):
            self[k] = self.newcell(k)

    def _configure(self):
        """connect the cells"""
        super()._configure()
        for i in range(self.__n):
            for j in range(self.__n):
                if i != j:
                    self[i][j] = self[j]

    def __str__(self):
        """string representation"""
        s = f"// Complete Grid K({self.__n})\n"
        s += "// (graphviz engine) circo\n"
        Kn = f"K{self.__n}"
        s += f"//    circo -Tpng -o {Kn}.png {Kn}.gv\n"
        s += self.graphviz_dot
        return s

class PartiteGrid(Grid):
    """Kuratowski k-partite grids"""

    __slots__ = ("__args", )

    def _parse_args(self, *args):
        """constructor"""
        super()._parse_args()
        k = len(args)
        if k < 2:
            raise ValueError("at least two arguments are required")
        for i in range(k):
            n = args[i]
            if not isinstance(n, int):
                raise TypeError(f"arg[{i}] must be an integer")
            if n < 1:
                raise ValueError("arg[{i}] must be a positive integer")
        self.__args = args

    def _initialize(self):
        """create the cells"""
        super()._initialize()
        k = len (self.__args)
        for i in range(k):
            n = self.__args[i]
            for j in range(n):
                index = (i,j)
                self[index] = self.newcell(index)

    def _configure(self):
        """connect the cells"""
        super()._configure()
        k = len (self.__args)
        for i in range(k):
            m = self.__args[i]
            for j in range(k):
                if i == j:
                    continue
                n = self.__args[j]
                for a in range(m):
                    for b in range(n):
                        self[i,a][j,b] = self[j,b]

    @property
    def parts(self) -> int:
        """the number of parts in the vertex partition

        This is the same as the number of arguments
        """
        return len(self.__args)


    def _get_parts(self) -> dict():
        """displays the parts that make this k-partite"""
        parts = dict()
        for cell in self.cells:
            i, j = cell.index
            if i not in parts:
                parts[i] = set()
            parts[i].add(cell)
        return parts

    def _display_parts(self, parts:dict) -> str:
        """display the partiotion"""
        s = str()
        k = len(self.__args)
        for i in range(k):
            if i in parts:
                s += f'  subgraph cluster_{i} '
                s += '{\n'
                s += f'    label = "{i}"\n'
                s += f'    pencolor = "red"\n'
                for cell in parts[i]:
                    i, j = cell.index
                    s += f'    "{cell.index}" [pos="{2*i},{j}!", shape="rectangle"]\n'
                s +="  }\n"
        return s

    @property
    def graphviz_dot(self) -> str:
        """return a simple graphviz representation"""
        s = 'digraph D {\n'
        s += '  splines=ortho\n'
        parts = self._get_parts()
        s += self._display_parts(parts)
        joins = self._get_joins()
        s += self._display_joins(joins)
        s += "}"
        return s

    def __str__(self):
        """string representation"""
        s = f"// {self.parts}-partite Grid K{self.__args}\n"
        s += "// (graphviz engine) fdp\n"
        s += f"//    fdp -Tpng -o maze.png maze.gv\n"
        s += f"// Partite graphs typically require some trial and error\n"
        s += self.graphviz_dot
        return s

# END mazes.Grids.complete
