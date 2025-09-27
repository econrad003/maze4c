# The fractal tessellation algorithm

This maze creation algorithm is, in a proper sense, neither a passage carver nor a wall builder.  It is really a copier which does a small amount of carving.  If we start with a 1×1 single-cell maze as the initial unit, then it becomes a passage carver in the strict sense.

The algorithm starts with a maze.  That maze is copied and arranged to form a larger maze.  The pieces are then connected by a network of passages.  We can repeat the process using the result to create an even larger maze.  And that is the algorithm in its entirety.

## Example 1 - the tessellation algorithm

We start with some imports:

```
eric@purple-cow:~/repositories/maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.fractal_tess \
...     import FractalTessellation as Tessellation
```

Tessellation is, in essence, taking some scraps of paper and piecing them together without overlapping them to form a given shape.  For example, we might take 8 congruent square pieces of paper and arrange them to form a rectangle.  If the side of each paper square is 1 cm, then there are, up to congruence, exactly 2 rectangles that can be formed using all eight squares:

+ 1 cm × 8 cm
+ 2 cm × 4 cm

The scraps are called *tiles*, and, in our basic implementation, the tiles must be squares or rectangle of identical dimensions.  For example, if one of our tiles is a 3×3 square maze, all our tiles must be likewise.  Likewise, if one of our tiles is a 4×7 rectangular maze, then so also must be the other tiles.

So now we need some tiles of the same shape and dimensions.  First let's import some carving algorithms:
```
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree
>>> from mazes.Algorithms.sidewinder import Sidewinder
>>> from mazes.Algorithms.recursive_division import RecursiveDivision
>>> from mazes.Algorithms.wilson import Wilson
>>> from mazes.Algorithms.dfs_better import DFS
>>> from mazes.Algorithms.bfs import BFS
```

Now we need a supply of identical grids:
```
>>> mazes = list()
>>> for i in range(6):
...     mazes.append(Maze(OblongGrid(6, 5)))
...
```

And we need to turn these grids into (perfect) mazes.  The first line creates a little function which always returns None -- this allows us to ignore the status returned from the *on* methods.  The remaining lines carve the 6×5 rectangular mazes which we will use as our tiles:
```
>>> zap = lambda x: None
>>> zap(BinaryTree.on(mazes[0]))
>>> zap(Sidewinder.on(mazes[1]))
>>> zap(RecursiveDivision.on(mazes[2]))
>>> zap(Wilson.on(mazes[3]))
>>> zap(DFS.on(mazes[4]))
>>> zap(BFS.on(mazes[5]))
```

Now we program our tesellatrix and get some information about the expected result:
```
>>> rules = [[0, 1, 2], [5, 4, 3]]
>>> tessellation = Tessellation(rows=2, cols=3, symmetries=rules)
>>> tessellation.single_pass(*mazes, test=True)
(<class 'mazes.Grids.oblong.OblongGrid'>, 12, 15)
```
The rules tell us where each tile will be placed.  Our tessellatrix will use the rules to arrange the tiles to form a 2 row, 3 column array of tiles.  The result will be a 12 row, 15 column rectangular maze with Von Neumann (*i.e.* N/S/E/W) neighborhoods.  We now create the maze:
```
>>> maze = tessellation.single_pass(*mazes)
>>> print(tessellation)
                        passes 1
                         cells 180
                      passages 179
                        carver Kruskal
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   | M   k     |         K |       |         H |
+   +   +   +   +   +   +---+   +   +---+   +   +   +---+---+
|                   |           |   |   |   |               |
+---+---+---+---+   +   +---+---+   +   +   +---+---+   +---+
|                   |   |       |   |   |   |   |           |
+---+---+---+---+   +   +---+   +   +   +---+   +---+---+   +
|                   |   |       |       |   |           |   |
+---+---+---+---+   +   +   +   +---+---+   +   +   +---+   +
|                   |   |   |       | j   h     |           |
+---+---+---+---+   +   +   +---+   +   +   +   +   +---+---+
| L                 | J   e |           | G | g |           |
+---+---+---+---+---+---+   +---+---+---+---+   +---+---+---+
|                 B |     d           D |     f |   |     F |
+---+   +---+   +   +   +   +   +   +---+   +   +   +---+   +
|       |       | b   c |   |   |       |   |       |       |
+   +---+   +   +   +   +   +---+   +---+   +---+   +   +---+
|   |       |   |   |   |   |     a     |       |   |       |
+---+---+   +   +   +   +   +---+   +   +   +---+---+   +   +
|           |   |   |   |       |   |   |       |       |   |
+---+---+---+   +   +   +---+---+   +   +   +   +   +---+   +
|               |   |   |           |   |   |       |       |
+   +   +   +---+   +   +---+   +   +   +   +---+---+---+---+
| A |   |   |       | C |       |   |   | E                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The status tells us that the maze consists of 180 cells (12×15=180) and 179 passages (the right number for a perfect maze).  The tiles were themselves perfect mazes with 30 cells and 29 passages.  Of the 179 passages, 174 passages (29×6=174) were copies of the passages in the tiles, and just 5 were carved by Kruskal's algorithm to complete the perfect maze.

The cell labels were added manually to assist in the discussion that follows.

* Tile AB in the lower left is a simple binary tree maze.  The rule `rules[0][0]` was set to 0 and the maze `mazes[0]` is the binary tree maze tile.
* Tile CD (lower center) is a sidewinder maze.  (Cell a has degree 4, so it is not a binary tree.)  The rules dictated placement of this tile.
* Tile EF (lower right) is the recursive division maze.
* Tile GH (upper right) is the Wilson maze.
* Tile JK (upper center) is the DFS maze.
* Tile LM (upper left) is the BFS maze.

The passages added using Kruskal's algorithm are:

* Passage bc connecting Tiles AB and CD
* Passage de connecting Tiles CD and JK
* Passage fg connecting Tiles EF and GH
* Passage hj connecting Tiles GH and JK
* Passage kM connecting Tiles JK and LM

If we consider these five passages and the tiles they serve, we have the following 2 row, 3 column *subdivision*:

```
             LM -- JK -- GH
              |     |     |
             AB    CD    EF
```
(This subdivision is a spanning tree of the tiles, or, equivalently, a perfect maze.)

## Example 2 - tessellation, again

The *rules* in Example 1 determined the placement of the tiles.  If we omit the rules, tiles are drawn randomly with replacement.  Using the tiles above:
```
>>> tessellation = Tessellation(rows=2, cols=3)
>>> maze = tessellation.single_pass(*mazes)
>>> print(tessellation)
                        passes 1
                         cells 180
                      passages 179
                        carver Kruskal
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                 D |       |         K |       |   |     F |
+   +   +   +   +---+   +---+   +   +---+   +   +   +---+   +
|   |   |   |                   |   |   |   |       |       |
+   +   +---+   +---+   +---+---+   +   +   +---+   +   +---+
|   |   |           |   |       |   |   |       |   |       |
+   +   +---+   +   +   +---+   +   +   +   +---+---+   +   +
|   |       |   |   |   |       |       |       |       |   |
+   +---+---+   +   +   +   +   +---+---+   +   +   +---+   +
|   |           |   |   |   |       |   |   |       |       |
+   +---+   +   +   +   +   +---+   +   +   +---+---+---+---+
| C |       |   |   | J     |           | E                 |
+---+---+---+---+---+   +---+---+---+---+---+---+---+---+   +
|       |         K |       |         K |                 B |
+   +---+   +   +---+   +---+   +   +---+---+   +---+   +   +
|           |   |   |           |   |   |       |       |   |
+   +---+---+   +   +   +---+---+   +   +   +---+   +   +   +
|   |       |   |   |   |       |   |   |   |       |   |   |
+   +---+   +   +   +   +---+   +   +   +---+---+   +   +   +
|   |       |           |       |       |           |   |   |
+   +   +   +---+---+   +   +   +---+---+---+---+---+   +   +
|   |   |       |   |   |   |       |                   |   |
+   +   +---+   +   +   +   +---+   +   +   +   +   +---+   +
| J     |           | J     |           | A |   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Here, the binary tree (Tile AB), the sidewinder tree (Tile CD) and the recursive division tree (Tile EF) were each used once.  The depth-first search tree (Tile JK) was used three times to fill the remaining entries.  The breadth-first search tree (Tile LM) and the uniform Wilson tree (Tile GH) weren't used at all.

Kruskal's algorithn was used to connect the tiles.  Here is the subdivision maze:
```
     CD  --  JK1     EF
              |       |
     JK2 --  JK3 --  AB
```

## Example 3 - fractal tessellation (at last!)

The term fractal implies a self-similarity at several levels.  So fractal tessallation implies that we use similar tiles at several levels.  In the simplest case, at each level, we use a single tile, and the results of lower levels are used to generate the next level.  Using the defaults, we start with a trivial 1×1 maze, tile it in two rows and 2 columns to create a 2×2 maze.  We then use the 2×2 maze as a tile to create a 4×4 maze.  Finally, in a third pass, we use the 4×4 maze as a tile to create an 8×8 maze.

We start from scratch with an import:
```
eric@purple-cow:~/repositories/maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.fractal_tess import FractalTessellation
```

We create the tesselatrix:
```
>>> tess = FractalTessellation()
```
(The default is 2 rows and 2 columns.)

Now we run three passes of the algorithm:
```
>>> maze = tess.on()
Expected result: 8 rows, 8 columns
Actual result: 8 rows, 8 columns
>>> print(tess)
                        passes 3
                         cells 64
                      passages 63
                        carver Kruskal
>>> print(maze)
+---+---+---+---+---+---+---+---+
|                               |
+---+   +---+   +---+   +---+   +
|       |       |       |       |
+---+   +---+   +---+   +---+   +
|       |       |       |       |
+---+   +---+   +---+   +---+   +
|       |       |       |       |
+---+---+---+---+---+---+   +---+
|             C |               |
+---+   +---+   +---+   +---+   +
|       |               |       |
+---+   +---+   +---+   +---+   +
|     B |       |       |       |
+---+   +---+   +---+   +---+   +
| A     |       |       |       |
+---+---+---+---+---+---+-.--+---+
```

If we consider the 2×2 tile AB or the 4×4 tile AC, the self-similarity is obvious at two of the three levels.  The resulting maze does however have a somewhat dull texture.  But we can make the texture more interesting by rotating or even reflecting the tiles.

## Example 4 - fractal tesselation with dihedral symmetries

The dihedral group on a rectangle (or square) consists of the rotations and reflections of the rectangle onto itself.  If the rectangle is a square, there are four such rotations and four such reflection.  In this case, the dihedral group is known as *D₄* (the number of congruent sides) or *D₈* (the number of distinct symmetries).  If the rectangle is not square, there are just two rotations and two reflections.  Depending on author, the group is either *D₂* (the number of sides in each congruence class) or *D₄* (the number of symmetries) or *ℤ₂×ℤ₂* (for technical reasons).  Here we call the rectangular group *D₂* and the square group *D₄* and leave it to serious authors to argue about the merits of a given naming system.

Using the import from the previous example, we create a tessellatrix:
```
>>> tess = FractalTessellation(symmetries=True)
```

At each step, our tiles may be rotated or reflected:
```
>>> maze = tess.on()
Expected result: 8 rows, 8 columns
Actual result: 8 rows, 8 columns
>>> print(tess)
                        passes 3
                         cells 64
                      passages 63
                        carver Kruskal
>>> print(maze)
+---+---+---+---+---+---+---+---+
|       |     H |   |   |     F |
+   +   +   +---+   +   +---+   +
|   |           |               |
+---+   +   +---+---+---+   +---+
|       |       |               |
+---+   +   +---+   +   +   +   +
| G     |         E |   |   |   |
+---+---+---+   +---+---+---+---+
|       |     B |   |   |   | D |
+---+   +   +---+   +   +   +   +
|       |       |               |
+---+   +   +---+---+   +---+---+
|   |           |               |
+   +   +   +---+   +---+   +   +
| A     |         C     |   |   |
+---+---+---+---+---+---+---+---+
```

In the final pass, four of the eight symmetries were used in the arrangement of the 4×4 basic tile.

## Example 5 - Moore grid fractal tesselation

We can use Moore neighborhood with a simple cheat.  (Upsilon and hexagonal grids are more complicated and require additional tweaking.)  We need two imports:
```
>>> from mazes.Grids.oblong8 import MooreGrid
>>> from mazes.maze import Maze
```

After creating the tessellatrix, we apply the tweak:
```
>>> tess = FractalTessellation(symmetries=True)
>>> tess.maze = Maze(MooreGrid(1, 1))    # simple cheat
```

Now we can run our three passes, but we do get a warning.  (We could alternately create a derived class which modifies the *configure* and *test\_warning* methods.)  Note that our final result for this run does contain some diagonal passages:
```
>>> maze = tess.on()
WARNING: types other than OblongGrid are not supported.
Expected result: 8 rows, 8 columns
Actual result: 8 rows, 8 columns
>>> print(tess)
                        passes 3
                         cells 64
                      passages 63
                        carver Kruskal
>>> print(maze)
+---+---+---+---+---+---+---+---+
|       |       |       |       |
+   \---\   \---+---/   /---/   +
|   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+   +
|   |   |   |   |   |   |   |   |
+---\   \   /---/---\   /   /---+
|       |       |       |       |
+---+---+---+---+---+   +---+---+
|       |       |       |       |
+---/   \   \---+---/   /   \---+
|   |   |   |   |   |   |   |   |
+---+---+---+   \   +---+---+---+
|   |   |   |   |   |   |   |   |
+---\   \---\   +   /---/   /---+
|       |       |       |       |
+---+---+---+---+---+---+---+---+
```

## Additional examples

For a few more examples, look at the test module *tests.fractal\_tess*.  It can be run using the following command line:
```
    $ python -m tests.fractal_tess
```