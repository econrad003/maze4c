# Experimenting with vertex-Prim

Vertex-Prim is a modification of Prim's algorithm which assigns priorities to cells (vertices) instead of edges (internal grid walls).

The inspiration for the following experiments with the vertex-Prim algorithm was the following article in the Game Developer Blog:

*  Herman Tulleken.  Algorithms for making more interesting mazes.

The URL is `https://www.gamedeveloper.com/programming/algorithms-for-making-more-interesting-mazes`.  (Access date: 23 December 2025.)

## Section 1.  The Knight's move metric.

Simply described, the knight's move metric on a chessboard is the minimum number of moves it takes a knight to travel from one square on a chessboard to another square.  For example, if the knight starts in the lower left corner, it takes two moves to go two squares to the right:
```
    +---+---+---+
    |   | 1 |   |
    +---+---+---+
    |   |   |   |
    +---+---+---+
    | 0 |   | 2 |
    +---+---+---+
```
This is certainly the best we can do since we cannot get to the square in one move.  The actual number of knight moves can be calculated using a formula on a square-by-square basis without moving any knights and without ant program loops.  Here are the results for the number of knight moves required to take a knight positioned on the center square of a 9 by 13 (fairy) chessboard to move to any given square:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 3 | 4 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 4 | 3 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 4 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 4 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 3 | 2 | 3 | 4 | 1 | 2 | 1 | 4 | 3 | 2 | 3 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 4 | 3 | 2 | 1 | 2 | 3 | 2 | 1 | 2 | 3 | 4 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 3 | 2 | 3 | 2 | 3 | 0 | 3 | 2 | 3 | 2 | 3 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 4 | 3 | 2 | 1 | 2 | 3 | 2 | 1 | 2 | 3 | 4 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 3 | 2 | 3 | 4 | 1 | 2 | 1 | 4 | 3 | 2 | 3 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 4 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 4 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 3 | 4 | 3 | 2 | 3 | 2 | 3 | 2 | 3 | 4 | 3 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 1.  The knight move metric starting at (4,6)
```
*Note:* "Fairy chess" is just chess played on a nonstandard chessboard or with nonstandard pieces.  We used a standard piece (the knight) on a nonstandard chessboard.

Note that every cell is at most four knight's moves from the center cell.

Here is the code used to prepare the display Figure 1:
```python
    from mazes.Grids.oblong import OblongGrid
    from mazes.maze import Maze
    from mazes.Metrics.oblong import KnightMetric
    maze = Maze(OblongGrid(9,13))
    s = maze.grid[4,6]
    metric = KnightMetric(maze)    # set up the metric
    d = metric.distances(s)        # get distances from the center
    for cell in maze.grid:
       cell.label = str(d[cell])
    print(maze)
```

## Section 2.  Metric spaces

A *metric* on a set X is function *d* which maps pairs of points in X to real number that satisfies several constraints:

1.  For each *x* and *y* in X, *d(x,y)* is nonnegative; it is zero if and only if *x=y*.
2.  For each *x* and *y* in X, *d(x,y)=d(y,x)*.
3.  For each *x*, *y* and *z* in X, *d(x,y)+d(y,z)* is never less than *d(x,z)*.

The first constraint is what is meant when we say that *d* is *positive definite*.  The second constraint tells us that *d* is *symmetric*.  The third constraint is a version of the *triangle inequality* -- some would say that *d* is *subadditive*.  If set X has a metric *d*, then the ordered pair (X,*d*) is a *metric space*.

Metric spaces generalize the notion of distance on a surface or in space.

## Section 3.  Vertex-Prim and the knight's metric.

We will use the knight's move metric as our way of measuring the time it takes to go from one cell to another.  We will weight our cells based on starting in the cell in row 4 column 6.

Using the grid above, we start by erasing the labels:
```python
    for cell in maze.grid:
        cell.label = ' '
```

Next we run vertex-Prim:
```python
    from mazes.VGT.vprim import vprim
    print(vprim(maze, start_cell=s, shuffle=False, cell_map=d,
          action="stable"))
    print(maze)
```

### Example 3.1

Here is the output:
```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (4, 6)
                             cells      117
                          passages      116
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       |   |   |                   |
+---+---+---+---+---+   +   +   +   +---+---+---+---+
|                       |   |                       |
+---+---+---+---+---+   +   +   +---+---+---+---+---+
|               |                   |               |
+---+---+---+   +---+   +---+   +---+   +---+---+---+
|                           |                       |
+---+---+---+---+   +---+   +---+   +   +   +---+---+
|                   |           |   |   |           |
+---+---+---+---+   +---+   +---+   +---+---+---+---+
|                       |   |                       |
+---+---+   +   +   +   +---+---+   +   +---+---+---+
|           |   |   |           |   |               |
+---+---+   +   +---+   +---+   +---+   +---+---+---+
|           |   |           |       |               |
+---+   +   +   +   +   +   +   +   +   +---+---+---+
|       |   |   |   |   |   |   |   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.1 - Knight's move maze (deterministic)
```
Note that the starting cell had weight 0 was degree 4.  Things get a bit more complicated from there on out, but, with one exception, the cells that are a knights move away are all degree 3 or degree 4.  As we move further away, the maze becomes more like a breadth-first search maze.  The algorithm does not create circuits... close to the center, the vertex weights control the allocation of cells; away from the center, the circuit crushing dominates the algorithm.

Now let's make the behavior more random.  First, erase the work:
```python
    maze.unlink_all()
```

Now recreate the maze without the determinism:
```python
    print(vprim(maze, start_cell=s, cell_map=d))
    print(maze)
```

### Example 3.2

The output:
```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (4, 6)
                             cells      117
                          passages      116
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |   |   |   |   |   |   |   |       |
+   +---+   +   +   +   +   +   +   +   +   +---+   +
|   |   |       |       |   |       |           |   |
+---+   +---+   +---+   +   +   +---+---+   +---+   +
|               |               |   |   |           |
+---+   +---+   +---+   +---+   +   +   +   +---+   +
|   |   |           |   |   |                   |   |
+   +---+---+---+   +---+   +---+   +---+   +---+---+
|                   |           |       |           |
+---+---+---+---+   +---+   +   +   +---+---+---+---+
|       |               |   |               |   |   |
+---+   +---+   +---+   +---+   +---+   +---+   +   +
|           |   |                   |   |           |
+---+   +   +---+---+   +   +   +---+   +   +---+   +
|       |               |   |       |           |   |
+   +   +   +---+   +   +---+   +   +   +   +---+   +
|   |   |   |       |   |       |   |   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.2 - Knight's move maze (stochastic, starting from center)
```
We still have the central feature, the maze doesn't have the BFS-like outer region.

We don't need to start the algorithm in the center cell:
```python
    maze.unlink_all()
    start = maze.grid[0,2]
    print(vprim(maze, start_cell=start, cell_map=d))
    print(maze)
```
## Example 3.3

```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (0, 2)
                             cells      117
                          passages      116
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |               |   |                       |
+   +---+---+   +---+   +   +   +---+   +---+---+---+
|   |       |   |       |   |       |   |   |       |
+   +---+   +---+---+   +   +   +---+---+   +   +---+
|           |   |   |               |   |           |
+   +---+   +   +   +   +   +   +---+   +   +---+---+
|   |                   |   |                   |   |
+---+---+   +---+   +---+---+   +   +   +   +---+   +
|               |       |   |   |   |   |           |
+---+---+   +---+   +---+   +---+   +---+---+   +---+
|   |       |               |   |           |   |   |
+   +---+   +---+   +   +---+   +---+   +---+---+   +
|           |   |   |               |               |
+---+---+   +   +---+   +   +   +---+---+   +---+---+
|   |               |   |   |       |           |   |
+   +---+---+   +---+   +---+   +---+---+   +---+   +
|         S     |       |               |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.3 - Knight's move maze (stochastic, off-center start)
         Legend:  S=start cell
```
That seems to break up some of the symmetry.

We can let the algorithm decide where to start:
```python
    maze.unlink_all()
    print(vprim(maze, cell_map=d))
    print(maze)
```

## Example 3.4

```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (7, 9)
                             cells      117
                          passages      116
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |       |       |       |       |
+   +---+   +---+   +   +---+---+   +   +---+---+   +
|   |                   |             S     |       |
+---+---+   +---+---+   +---+   +   +   +---+   +---+
|           |   |               |   |   |           |
+---+---+---+   +---+   +---+   +---+---+   +   +---+
|       |               |                   |   |   |
+---+   +---+---+   +   +---+   +   +   +   +---+   +
|               |   |       |   |   |   |           |
+---+   +---+   +---+---+---+---+   +---+---+---+   +
|       |               |                   |   |   |
+---+---+---+   +---+   +---+   +   +   +---+   +---+
|           |   |               |   |   |           |
+---+---+   +---+---+   +   +   +---+---+   +   +---+
|                       |   |               |   |   |
+---+---+   +   +   +   +---+   +   +   +   +---+   +
|           |   |   |       |   |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.4 - Knight's move maze (stochastic, random start)
         Legend:  S=start cell
```

And we can re-introduce some of the determinism:
```python
    maze.unlink_all()
    start = maze.grid[7,9]
    print(vprim(maze, start_cell=start, shuffle=False, cell_map=d))
    print(maze)
```
Note that the priority queue is unstable, so we aren't fully deterministic.

## Example 3.5

```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (7, 9)
                             cells      117
                          passages      116
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |       |                   |       |
+   +   +   +   +---+   +---+   +---+   +---+---+   +
|   |   |   |   |       |   |   |     S     |       |
+   +   +   +   +---+   +   +   +---+   +---+   +---+
|               |                   |   |           |
+---+---+---+   +---+   +   +   +---+---+   +---+---+
|   |                   |   |                       |
+   +---+   +   +   +   +---+   +   +---+---+---+---+
|           |   |   |   |       |                   |
+   +   +---+---+   +---+---+---+   +---+---+---+---+
|   |   |               |                           |
+---+---+---+   +   +---+---+   +   +   +   +---+---+
|           |   |   |           |   |   |           |
+   +---+   +---+---+   +---+   +---+---+---+   +---+
|   |                   |           |       |       |
+   +---+   +---+---+   +---+   +---+   +---+   +---+
|   |       |           |                   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.5 - Knight's move maze (semi-deterministic, off-center start)
         Legend:  S=start cell
```
Note that the BFS-like behavior on the outskirts is starting to return, but the unstable priority queue offers some resistance.

Now let's stabilize the priority-queue to make things fully deterministic:
```python
    maze.unlink_all()
    print(vprim(maze, start_cell=start, shuffle=False, cell_map=d,
          action='stable'))
    print(maze)
```

## Example 3.6

```
          Vertex Growing Tree (statistics)
                            visits      233
                        start cell  (7, 9)
                             cells      117
                          passages      116
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |   |                           |
+---+---+---+---+   +   +---+---+---+   +---+---+---+
|                       |       |     S             |
+---+---+---+---+---+   +---+   +---+   +---+---+---+
|           |   |               |                   |
+---+---+   +   +---+   +---+   +---+   +---+---+---+
|                       |                           |
+---+---+---+---+   +   +---+   +   +   +---+---+---+
|                   |   |       |   |               |
+---+---+---+---+   +---+---+---+   +---+---+---+---+
|                   |   |                           |
+---+---+---+   +---+   +---+   +   +   +   +---+---+
|               |               |   |   |           |
+---+---+---+---+---+   +---+   +---+   +   +   +---+
|                       |           |   |   |       |
+---+---+---+   +   +   +---+   +---+   +   +   +   +
|               |   |   |           |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

    Figure 3.6 - Knight's move maze (deterministic, off-center start)
         Legend:  S=start cell
```
The off-center start breaks up some of the symmetry, but the fringe BFS-like behavior has reasserted itself.

## Section 4.  A larger example

A larger example has been saved in the gallery.  Here is the python run:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Metrics.oblong import KnightMetric
>>> from mazes.VGT.vprim import vprim
>>> maze = Maze(OblongGrid(34,55))
>>> metric = KnightMetric(maze)
>>> s = maze.grid[17,27]
>>> d = metric.distances(s)
>>> print(vprim(maze, start_cell=maze.grid[4,4], cell_map=d))
          Vertex Growing Tree (statistics)
                            visits     3739
                        start cell  (4, 4)
                             cells     1870
                          passages     1869
>>> from mazes.Graphics.dot.oblong2 import Plotter
>>> cells = {s:{"label":"C"}, maze.grid[4,4]:{"label":"S"}}
>>> dot = Plotter(maze, cell_attrs=cells)
>>> dot.render("vprim-knight")
Output: vprim-knight (svg)
```
The output is in file 'gallery/vprim-knight.svg'.