"""
mazes.Algorithms.fractal_tess - fractal tessellation maze carver
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    As described in [1], we start with a small rectangular maze,
    for example, a 2x2 maze.  We make four copies of the maze and
    place them to the east, south, and southeast of the original
    maze, and then carve three passages to connect the four small
    mazes.  The result is a maze with dimensions doubled.  If the
    original maze is perfect (i.e. a spanning tree maze), then the
    resulting maze is also perfect.  The process can be repeated
    several times to form a maze several times the size.

    If we start with an m×n perfect maze and run the algorithm k times,
    the result is a perfect maze with dimensions:
        2^k m × 2^k n.
    For example, if the original maze is 2x2, then, since 2^4=16,
    running the algorithm 5 times yields a 32x32 maze.

VARIATIONS INCLUDED

    1.  We can rotate and or reflect the copy before placing it.  If
        the maze is square, there are four possible rotations and four
        possible reflections.  For a general rectangle (not square),
        there are just two rotations and two reflections.  (One of the
        rotations is the 0-degree rotation or identity.)

    2.  Instead of placing three copies, we might place copies in m rows
        of n columns each (m>1, n>1).

    Both variations have been implemented herein.

OTHER VARIATIONS

    1.  The algorithm can be adapted to some non-rectangular mazes, for
        example triangular mazes.  The main requirement is that there
        must be a way of producing larger tessellating shapes from
        smaller tessellating shapes.

    Variations mentioned in this section can be treated as homework.

REFERENCES

    [1] "Maze generation algorithm" in Wikipedia. 6 Sep. 2025. Web. 
        Accessed 24 Sep. 2025.
            https://en.wikipedia.org/wiki/Maze_generation_algorithm
        The basic algorithm is described in a section entitled
            "Fractal Tessellation algorithm".

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
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.dihedral import DihedralGroup
from mazes.Algorithms.kruskal import Kruskal

class FractalTessellation(object):
    """This is an implementation of the fractal tessellation algorithm

    Since the algorithm is run a specific number of times, it is not
    built upon class algorithm.  It is technically neither a wall
    builder nor a passage carver as the grid is not passed as
    an argument to the algorithm.  Instead, it is constructed in the
    final step and returned to the caller.

    In other respects, the algorithm does behave like a typical
    carving algorithm.  Note that the "on" method is implemented
    as a regular instance method.

    The object is instantiated.  A seed maze is fed to the on method.
    """

    def __init__(self, rows:int=2, cols:int=2, symmetries=None,
                 Carver=Kruskal):
        """constructor

        This describes how the maze will be built from the seed.

        ARGUMENTS

            rows, cols - in a given iteration, copies of the seed maze
                (or symmetries) will be arranged into a fixed number
                of rows and columns.  (Default: 2, 2)  Afterward assembly,
                the entries will be connected by a minimal system of
                passages.  (The number of passages is one less than the
                number of entries.)

            symmetries - (default: None)
                If the value is None, False, or 0, then only the seed
                maze will be used to carve the entries (or blocks) in the
                next maze.  If the value is True or 1, the each entry will
                be constructed from a randomly chosen symmetry.  If the
                value is an m×n list of integers, where m is the number of
                rows and n is the number of columns, the entry will use the
                indicated symmetry.  (The symmetries are arranged in a list.
                If the number exceeds the length of the list or is negative,
                it will be reduced modulo the length.)

            Carver - (default: mazes.Algorithms.kruskal.Kruskal)
                The carving algorithm for connecting the entries in each
                pass.  The default is Kruskal's algorithm with no weights.
        """
        self.rows = rows
        self.cols = cols
        self.symmetries = symmetries
        self.maze = Maze(OblongGrid(1, 1))
        self.status = {}
        self.Carver = Carver
        assert callable(Carver)
        self.status["passes"] = 0
        self.initialize()
        self.configure()

    def initialize(self):
        """stub"""
        pass

    def configure(self):
        """stub"""
        pass

    def verify_seeds(self, *seeds):
        """check the seed mazes"""
        grid1 = seeds[0].grid
        for i in range(len(seeds)):
            maze = seeds[i]
            grid = maze.grid
            if type(grid) != type(self.maze.grid):
                typename = type(grid).__name__
                raise TypeError(f"Grid {i} {typename} not supported")
            if grid.m != grid1.m or grid.n != grid1.n:
                raise ValueError(f"Grid {i} dimension error")

    def test_pass(self, maze):
        """a test pass"""
        grid = maze.grid
        cls = type(grid)
        m = grid.m * self.rows
        n = grid.n * self.cols
        return cls, m, n

    def create_maze_object(self, GridType, m, n, *args, **kwargs):
        """create a new maze object

        The optional parameters (args and kwargs) are intended for
        use by derived classes.
        """
        return Maze(GridType(m, n, *args, **kwargs))

    def carve_entry(self, maze, i, j, seeds):
        """carve the passages in a single entry"""
            # DETERMINE THE SEED
        z = None
        if isinstance(self.symmetries, dict):
            z = self.symmetries.get((i,j))
        elif isinstance(self.symmetries, (list, tuple)):
            try:
                z = self.symmetries[i][j]
            except:
                z = None
        if isinstance(z, int):
            z = z % len(seeds)
            seed = seeds[z]
        else:
            seed = rng.choice(seeds)

            # CARVE THE ENTRY BY COPYING THE SEED
        m, n = seed.grid.m, seed.grid.n
        p0, q0 = i*m, j*n       # lower left of entry
        for edge in seed:
            cell1, cell2 = edge
            p1, q1 = cell1.index
            p2, q2 = cell2.index
            cell3 = maze.grid[p0+p1, q0+q1]
            cell4 = maze.grid[p0+p2, q0+q2]
            maze.link(cell3, cell4)

    def single_pass(self, *seeds, test=False, symmetry=True,
                    SymmetryGroup=DihedralGroup):
        """one pass

        OPTIONAL ARGUMENTS

            seeds - zero or more seed mazes
                If none are provided, then the current maze (initially
                a single cell with no passages) will be used.  The only
                requirements are that these mazes must be rectangular
                mazes of the same dimensions and of type OblongGrid.

                If more than one seed is provided, these will be used in
                place of the symmetries (provided the symmetries option
                is True or 1 or an m×n list of integers).

            test - if True, instead of running the pass, the grid type,
                the number of rows, and the number of columns of the
                output will be returned.

            symmetry - can be set to False to block using the
                symmetry group to create an orbit of a given maze

                Symmetries are blocked if self.symmetries is False, 0,
                or None.  (This is set in the constructor.)

                Symmetries are also blocked if there is more than one
                seed.

            SymmetryGroup - a class (duck-type compatible with class
                DihedralGroup in mazes.Algorithms.dihedral) which
                purports to generate the orbit of a group (of symmetries)
                on a maze.
        """
            # HOUSEKEEPING
        if len(seeds) == 0:
            seeds = (self.maze, )

        if len(seeds) > 1:
            symmetry = False
        elif len(seeds[0].grid) == 1:
            symmetry = False
        else:
            symmetry = bool(self.symmetries) and bool(symmetry)
        if symmetry:
            assert callable(SymmetryGroup)

        self.verify_seeds(*seeds)
        GridType, m, n = self.test_pass(seeds[0])
        if test:
            return GridType, m, n

            # PERFORM ONE PASS
        self.status["passes"] += 1
        maze = self.create_maze_object(GridType, m, n)
        if symmetry:
            group = DihedralGroup(seeds[0])
            group.build_table()
            seeds = group.symmetries
        for i in range(self.rows):
            for j in range(self.cols):
                self.carve_entry(maze, i, j, seeds)
        self.Carver.on(maze)
        self.status["cells"] = len(maze.grid)
        self.status["passages"] = len(maze)
        self.status["carver"] = self.Carver.__name__
        return maze

    def __str__(self):
        """format the status"""
        s = ""
        for key in self.status.keys():
            s += "%30s %s\n" % (key, self.status[key])
        return s[:-1]

    def test_warning(self, GridType):
        """display a warning if the GridType is not OblongGrid"""
        if GridType == OblongGrid:
            return
        print("WARNING: types other than OblongGrid are not supported.")

    def test(self, seed:Maze=None, passes:int=3) -> tuple:
        """returns the type and size of the result of the 'on' method"""
        assert type(passes) == int and passes >= 0
        if seed == None:
            GridType = type(self.maze.grid)
            m = self.maze.grid.m
            n = self.maze.grid.n
        else:
            GridType = type(seed.grid)
            m = seed.grid.m
            n = seed.grid.n
        self.test_warning(GridType)
        p = m * (self.rows ** passes)
        q = m * (self.cols ** passes)
        return GridType, p, q

    def on(self, seed:Maze=None, passes:int=3,
           SymmetryGroup:callable=DihedralGroup) -> Maze:
        """run the algorithm throug several passes

        If no seed is specified, the current value of self.maze
        is used as the seed.  (The base class default is a 1 by 1
        empty rectangular grid.)

        The default number of passes is 3.

        If symmetries are enabled in the constructor, the default
        is to use the dihedral group symmetries (D(2) or D(4).)

        The return value is the resulting maze.  Using the
        defaults here and for rows and columns in the constructor.
        """
        _, p, q = self.test(seed=seed, passes=passes)
        print(f"Expected result: {p} rows, {q} columns")
        if seed == None:
            seed = self.maze
        self.status["passes"] = 0
        for i in range(passes):
            seed = self.single_pass(seed, SymmetryGroup=SymmetryGroup)
        p, q = seed.grid.m, seed.grid.n
        print(f"Actual result: {p} rows, {q} columns")
        return seed

