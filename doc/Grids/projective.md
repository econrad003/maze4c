# The real projective planar grid

A real projective plane is a another surface that can be realized in four dimensions but not in three.  It can be constructed from a rectangle by identifying both pairs of opposite sides individually in the opposite sense (as in constructing a Möbius strip).  We can do the same thing starting with a rectangular grid...

We offer a single example keeping comments to a minimum.  (You might want to look over the documentation for cylindrical, Möbius strip, and Klein bottle grids to get some insight.)  There is, however, one peculiarity of the projective grid that does require comment, and fortunately the situation arose in our example.  This is a very unusual grid!
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.projective import ProjectiveGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> from mazes.console_tools import unicode_str
>>> maze = Maze(ProjectiveGrid(10, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       63
                             cells      150
                          passages      149
                 paths constructed       63
                     cells visited      986
                          circuits      272
                    markers placed      651
                   markers removed      502
                     starting cell  (0, 10)
>>> print(unicode_str(maze, w="N", e="NR", s="A", n="R"))
      O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳   ┳━━━┳   ┳   ┳━━━┳   ┳━━━┳   ┳   ┳━━━┳   ┳━━━┳━━━┳   ┓
  9 ┃       ┃           ┃   ┃   ┃   ┃       ┃   ┃           ┃     0
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
  8 ┃           ┃           ┃       ┃   ┃       ┃   ┃   ┃   ┃     1
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  7     ┃       ┃                       ┃   ┃   ┃       ┃         2
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  6     ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃           ┃   ┃       ┃ 3
    ┣   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ┫
  5     ┃   ┃               ┃           ┃   ┃       ┃   ┃   ┃     4
    ┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
  4         ┃   ┃           ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃     5
    ┣━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  3 ┃           ┃   ┃           ┃   ┃           ┃       ┃   ┃     6
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  2                     ┃               ┃       ┃                 7
    ┣━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  1         ┃   ┃               ┃           ┃   ┃   ┃           ┃ 8
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
  0     ┃       ┃       ┃   ┃           ┃       ┃   ┃       ┃   ┃ 9
    ┗   ┻━━━┻━━━┻   ┻━━━┻   ┻   ┻━━━┻   ┻━━━┻   ┻   ┻━━━┻   ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

## COMMENT

One apparent problem does need comment.  How many ways are there to step from the cell in the lower left corner to its diagonal opposite?

There is only one passage between the cell in the lower left and the cell in the upper right even though there appear to be two.  There are two grid connections and one passage, but apart from the two cells that were joined, the grid connections and the passages are not actually associated with either grid connection.  And we really need do both connections.  This is a surprising feature of the projective grid, but not a bug.

Here we verify that the bottom left corner is both east of and north of the top right corner:
```
>>> cell = maze.grid[0, 0]
>>> cell.west.index
(9, 14)
>>> cell.south.index
(9, 14)
```

And here we verify that the top left corner is both east of and south of the bottom right corner:
```
>>> cell2 = maze.grid[9, 0]
>>> cell2.west.index
(0, 14)
>>> cell2.north.index
(0, 14)
```

The question:

+ How many ways are there to step from the cell in the lower left corner to its diagonal opposite?

The answer:

+ It depends.  If we are working with the *grid*, the answer is two.  We can go either west or south.  The projective grid joins a cell to its diagonal opposite with a pair of *parallel* (directed) arcs.  If we are working with the *maze*, there is just one passage -- we can follow a single (undirected) edge between the two cells.

## ANALYSIS

Consider what happens when we construct a projective plane from a rectangle without dividing it into cells,  For sake of simplicity, consider a unit square with *(x,y)* coordinates.  The vertices are the origin *O=(0,0)*. the axes units *X=(1,0)* and *Y=(0,1)*, and the intersection of the lines *y=1* and *x=1*, namely *I=(1,1)*.  Identifying the horizontal vectors $OX$ and *IY* identifies the diagonally opposite points so that *O=I* and *X=Y*.  If we consider an ant moving left (westward) on the $x$-axis, as it passes through the origin, it finds itself moving to the left (still westward) from point *I* on the the line $IY$.  Of course the two side have been identified, so let's track its movement on the x-axis.  Suppose it starts at *(0,0.2)* and travels west at a constant rate of *0.1* per second.

| time (s)   | 0        | 1        | 2        | 3        | 4        |
| -----------| -------- | -------- | -------- | -------- | -------- |
| rectangle  | (0.2, 0) | (0.1, 0) | *O = I*  | (0.9, 1) | (0.8, 1) |
| projective | (0.2, 0) | (0.1, 0) | (0, 0)   | (0.1, 0) | (0.2, 0) |

Moving to the left on the line *y=1$ is the same under the identification as moving to the right on the *line *x*-axis.  Conversely, moving to the left on the $x$-axis is the same under the identification as moving to the right on the line *y=1*.

Now what happens if the ant starts a bit above the $x$-axis.  We now need to remember that the left side *OY* (upward) is identified with the right side *IX* (downward).  But unlike the sides of the rectangle, points inside the rectangle are not identified.

| time (s)   | 0   | 1   | 2 = | = 2 | 3   | 4   |
| ---------- | --- | --- | --- | --- | --- | --- |
| rectangle  |
| *x*        | 0.2 | 0.1 | O   | 1   | 0.9 | 0.8 |
| *y*        | 0.1 | 0.1 | O.1 | 0.9 | 0.9 | 0.9 |
| projective |
| *x*        | 0.2 | 0.1 | 0   | 1   | 0.9 | 0.8 |
| *y*        | 0.1 | 0.1 | 0.1 | 0.9 | 0.9 | 0.9 |

The only time on this trip where the ant is on a side is (exactly) at the 2 second mark.  Before the 2 second mark, it is on the line *y=0.1$ moving to the left, and afterward, it is on the line *y=0.9*, also moving to the left.  Eventually it will pass through the side *OY* and continue moving to the left on the line *y=0.1*.  From the ant's viewpoint, the line segment *y=0.9* in the interval \[0,1\] is an extension of line segment *y=0.1* in the interval \[0,1\] -- the ant simply sees them as parts of the same line.

If we divide the square into cells, we can think of a grasshopper hopping west from the center of one cell to its neighbor to the west.

Moving to the right, or downward, or upward works the same way.  Details are left to the reader.
