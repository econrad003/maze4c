# The toroidal grid

A torus is a surface that can be realized in three dimensions.  For example, the surface of a donut is essentially a torus.  Topologically speaking, the surface of a coffee cup with one loop for a finger is another.  A torus can be constructed from a rectangle by identifying both pairs of opposite sides individually in the same sense (as in constructing a cylinder.  We can do the same thing starting with a rectangular grid...

We offer a single example with little comment.  (You might want to look over the documentation for cylindrical, Möbius strip, and Klein bottle grids to get some insight.)

```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.torus import TorusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> from mazes.console_tools import unicode_str
>>> maze = Maze(TorusGrid(10, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       65
                             cells      150
                          passages      149
                 paths constructed       65
                     cells visited      312
                          circuits       37
                    markers placed      210
                   markers removed       61
                     starting cell  (6, 8)
>>> print(unicode_str(maze, h="N", v="A"))
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏   ┳   ┳   ┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳   ┳   ┳   ┳   ┳━━━┓
  9 ┃   ┃   ┃   ┃   ┃   ┃           ┃       ┃       ┃           ┃ 9
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ┫
  8             ┃   ┃   ┃       ┃   ┃       ┃               ┃     8
    ┣━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  7     ┃   ┃       ┃       ┃       ┃   ┃   ┃   ┃   ┃             7
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  6         ┃           ┃   ┃   ┃           ┃           ┃   ┃     6
    ┣   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
  5 ┃   ┃           ┃   ┃       ┃       ┃   ┃           ┃       ┃ 5
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━┫
  4 ┃       ┃       ┃       ┃               ┃   ┃   ┃       ┃   ┃ 4
    ┣━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  3         ┃               ┃   ┃       ┃   ┃           ┃   ┃     3
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ┫
  2 ┃       ┃           ┃       ┃               ┃   ┃   ┃       ┃ 2
    ┣━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━┫
  1         ┃   ┃                   ┃       ┃       ┃       ┃     1
    ┣   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  0 ┃   ┃   ┃   ┃           ┃           ┃   ┃   ┃       ┃       ┃ 0
    ┗   ┻   ┻   ┻━━━┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻   ┻   ┻   ┻   ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

The four corners are actually quite near each other -- one or two steps away on the grid -- as a result of the identifications.  Although it won't always happen, we can get some idea if we notice a short path in the maze which visits all four.  This maze has one:

```
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏ ^ ┳ v ┳   ┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳   ┳   ┳   ┳ ^ ┳━━━┓
  9 ┃ 1 ┃ * ┃   ┃   ┃   ┃           ┃       ┃       ┃     3   * ┃ 9
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ┫
  8 < *   *     ┃   ┃   ┃       ┃   ┃       ┃               ┃ * < 8
    ┣━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  7     ┃   ┃       ┃       ┃       ┃   ┃   ┃   ┃   ┃             7
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  6         ┃           ┃   ┃   ┃           ┃           ┃   ┃     6
    ┣   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
  5 ┃   ┃           ┃   ┃       ┃       ┃   ┃           ┃       ┃ 5
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━┫
  4 ┃       ┃       ┃       ┃               ┃   ┃   ┃       ┃   ┃ 4
    ┣━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  3         ┃               ┃   ┃       ┃   ┃           ┃   ┃     3
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ┫
  2 ┃       ┃           ┃       ┃               ┃   ┃   ┃       ┃ 2
    ┣━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━┫
  1   *   * ┃   ┃                   ┃       ┃       ┃       ┃     1
    ┣   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  0 ┃ 2 ┃ * ┃   ┃           ┃           ┃   ┃   ┃       ┃ *   4 ┃ 0
    ┗ ^ ┻ v ┻   ┻━━━┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻   ┻   ┻   ┻ ^ ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

Twelve steps!  Notice that the path was never more than two steps away from a corner.

## ANALYSIS

Suppose our rectangle is the unit square in the *(x,y)* Cartesian plane.  The vertices are the origin *O=(0,0)*, the axial units *X=(1,0)* and *Y=(0,1)* and the intersection *I* of the lines *x=1* and *y=1*, namely *I=(1,1)*.  We identify opposite sides of the square in the same sense, so *OX=YI* and *OY=XI*.

Under the identification *OX=YI*, we obtain *O=Y* and *X=I*.  Points between are also identified, for example *(0,0.222)=(1,0.222)*

Under the identification *OY=XI*, we obtain *O=X* and *Y=I*.  Points between are also identified, for example *(0.222,0)=(0.222,1)*.

After making both identifications, we have the *quadruple* point *O=X=Y=I*, *i.e.*, all four vertices become the same point in the projective plane.  The remaining points on the sides are double points -- every such point is identified with exactly point on the opposite side.  Points in the interior of the rectangle are not identified with any partner.

If an ant move to the right at a fixed rate from some point it will eventually reach a side, and continue its trip from the left. For example, if it starts at *(0.8,0.2)* and moves at a rate of *0.1* per second, it will reach the right side at *(1,0.2)* in 2 seconds, and continuing right from *(0,0.2)*, it will reach the starting point in another 8 seconds, for a total of ten seconds for the round trip.  Note that unlike a round trip on a rectangle, the ant doesn't need to reverse the direction.

Moving to the left, upward, or downward works the same way.  If we divide the rectangle into cells to form a grid or lattice, we replace the ant with a grasshopper who hops from the center of one cell to the next (right, left, up or down) at a fixed rate (cells per second).
