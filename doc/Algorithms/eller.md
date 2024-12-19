# Eller's Algorithm

Eller's algorithm is a true generalization of the sidewinder algorithm in the sense that any maze that can be produced by sidewinder can be produced by Eller's algorithm by restricting choices made during processing.  Eller's algorithms also adapts some component merging techniques from Kruskal's algorithm.

## The algorithm

We will just give a brief overview here.

1. In the first row, as in sidewinder, we divide the first row into a number of runs.  We then carve a path upward from each run.  But unlike sidewinder, we also *optionally* carve additional passages upward.

2. In subsequent rows, we must be careful not to create circuits.  We according modify the sidewinder procedure.  Given two adjacent cells in a row, we may optionally carve a passage between the provided that they are not in the same component.  Then, from each component in the current row, we carve *at least one* passage upward.  (If we never carve more than one passage upward, then the components in each row are just runs -- as in sidewinder.  If we carve more than one passage up from a component, then components in the subsequent rows can be broken runs.)

3. In the last row, we again modify the rule from sidewinder.  If two adjacent cells are in different components, we carve a passage between then so that they are now in the same component.

## Example 1

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Algorithms.eller import Eller
    2> from mazes.Grids.oblong import OblongGrid
    3> from mazes.maze import Maze
    4> maze = Maze(OblongGrid(8,13))
    5> print(Eller.on(maze))
          Martin Eller's Spanning Tree (statistics)
                            visits        8
                             cells      104
                          passages      103
               optional merge left       33
               required merge left        3
             required carve upward       58
             optional carve upward        9
                            onward  east
                            upward  north
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |                                   |
    +   +   +   +   +   +---+---+   +   +---+---+   +   +
    |   |   |   |           |   |   |       |       |   |
    +   +   +---+   +---+   +   +   +   +   +---+   +   +
    |   |   |       |   |   |       |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +---+   +
    |   |   |   |   |   |   |   |   |   |       |   |   |
    +---+---+   +   +   +   +   +   +   +---+   +   +   +
    |           |       |   |   |   |       |       |   |
    +   +   +   +   +---+---+---+   +---+   +   +   +   +
    |   |   |   |       |               |   |   |   |   |
    +---+   +---+---+   +   +   +---+---+   +   +   +   +
    |       |   |   |   |   |   |   |       |   |   |   |
    +   +   +   +   +---+---+---+   +   +   +   +   +---+
    |   |       |                       |   |   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 2 - Outward Eller

Eller's algorithm works with rows and columns.  But it can be adapted to other grid organizations.  Here we have adapted Eller's algorithm to work in rings radiating outward from the center.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.maze import Maze
    2> from mazes.Grids.oblong import OblongGrid
    3> from mazes.Algorithms.outward_eller import OutwardEller
    4> maze = Maze(OblongGrid(8,13))
    5> print(OutwardEller.on(maze))
          Outward Eller (statistics)
                            visits        4
                             cells      104
                          passages      103
               optional merge left       45
               required merge left       13
             required carve upward       24
             optional carve upward       21
                            onward  clockwise
                            upward  outward
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |               |                   |       |
    +   +   +   +---+---+---+   +   +   +   +   +   +   +
    |   |   |           |   |   |   |   |   |   |   |   |
    +   +   +---+   +   +   +   +---+---+   +---+   +   +
    |               |       |       |   |           |   |
    +---+---+---+   +   +   +   +   +   +---+---+   +   +
    |       |   |   |   |       |               |   |   |
    +---+   +   +---+---+---+---+---+---+   +---+   +   +
    |           |           |   |       |       |   |   |
    +   +---+---+   +   +   +   +   +---+---+   +   +   +
    |       |       |   |   |       |           |   |   |
    +---+   +---+---+---+   +   +---+   +   +   +   +   +
    |       |   |   |   |       |       |   |   |   |   |
    +---+   +   +   +   +---+   +---+   +---+---+---+   +
    |                                           |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```