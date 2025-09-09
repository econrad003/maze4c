# The Klein bottle grid

A Klein bottle is a surface that can be realized in four dimensions but not in three.  It can be constructed from a rectangle by identifying one pair of opposite sides in the same sense (as in constructing a cylinder), and the other pair in the opposite sense (as in constructing a Möbius strip).  We can do the same thing starting with a rectangular grid...

## Example 1 - a Klein bottle grid

We start with some imports.  We will want to label the rows and columns to show how sides are identified:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.klein import KleinGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> from mazes.console_tools import unicode_str
```

Next we create the maze using a suitable algorithm.  (We don't want to use an algorithm designed for the rectangular grid as it may give us a maze which is either disconnected or contains circuits.)  For this document, we chose Wilson's algorithm in hopes of producing a reasonably uniform maze:
```
>>> maze = Maze(KleinGrid(10, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       63
                             cells      150
                          passages      149
                 paths constructed       63
                     cells visited      416
                          circuits       75
                    markers placed      278
                   markers removed      129
                     starting cell  (2, 3)
```

And here is the result.  Since the left and right sides are identified in the opposite sense, we label the left side from bottom to top (same as the rectangular row numbers), but the right hand side from top to bottom.  The columns are labelled alphabetically from left to right:
```
>>> print(unicode_str(maze, w="N", e="NR", v="A"))
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┓
  9     ┃                   ┃   ┃                   ┃       ┃   ┃ 0
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  8 ┃       ┃           ┃               ┃       ┃   ┃       ┃     1
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
  7 ┃   ┃               ┃   ┃   ┃       ┃       ┃       ┃         2
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  6         ┃           ┃   ┃       ┃   ┃       ┃   ┃       ┃   ┃ 3
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃   ┃   ┃       ┃       ┃       ┃   ┃       ┃   ┃   ┃ 4
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ┫
  4 ┃   ┃   ┃                   ┃       ┃       ┃               ┃ 5
    ┣━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  3 ┃       ┃       ┃   ┃           ┃   ┃   ┃   ┃                 6
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  2             ┃   ┃   ┃   ┃   ┃           ┃                   ┃ 7
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  1         ┃   ┃           ┃   ┃       ┃   ┃   ┃       ┃       ┃ 8
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  0 ┃   ┃       ┃           ┃       ┃   ┃       ┃   ┃       ┃     9
    ┗━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

Notice the path from the lower left corner to the upper right corner in this maze. It's quite short -- just three passages!  There is even a short path which traverses all four corners -- can you find it?
```
>>> print(unicode_str(maze, w="N", e="NR", v="A"))
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┓
  9     ┃                   ┃   ┃                   ┃       ┃ T ┃ 0
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  8 ┃       ┃           ┃               ┃       ┃   ┃       ┃ * < 1
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
  7 ┃   ┃               ┃   ┃   ┃       ┃       ┃       ┃         2
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  6         ┃           ┃   ┃       ┃   ┃       ┃   ┃       ┃   ┃ 3
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃   ┃   ┃       ┃       ┃       ┃   ┃       ┃   ┃   ┃ 4
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ┫
  4 ┃   ┃   ┃                   ┃       ┃       ┃               ┃ 5
    ┣━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  3 ┃       ┃       ┃   ┃           ┃   ┃   ┃   ┃                 6
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  2             ┃   ┃   ┃   ┃   ┃           ┃                   ┃ 7
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  1 < *     ┃   ┃           ┃   ┃       ┃   ┃   ┃       ┃       ┃ 8
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  0 ┃ S ┃       ┃           ┃       ┃   ┃       ┃   ┃       ┃     9
    ┗━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

And here is a path through all four corners -- just five steps:
```
>>> print(unicode_str(maze, w="N", e="NR", v="A"))
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳ ^ ┓
  9 > 4 ┃                   ┃   ┃                   ┃       ┃ 1 ┃ 0
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  8 ┃       ┃           ┃               ┃       ┃   ┃       ┃ * < 1
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
  7 ┃   ┃               ┃   ┃   ┃       ┃       ┃       ┃         2
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  6         ┃           ┃   ┃       ┃   ┃       ┃   ┃       ┃   ┃ 3
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃   ┃   ┃       ┃       ┃       ┃   ┃       ┃   ┃   ┃ 4
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ┫
  4 ┃   ┃   ┃                   ┃       ┃       ┃               ┃ 5
    ┣━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  3 ┃       ┃       ┃   ┃           ┃   ┃   ┃   ┃                 6
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  2             ┃   ┃   ┃   ┃   ┃           ┃                   ┃ 7
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  1 < *     ┃   ┃           ┃   ┃       ┃   ┃   ┃       ┃       ┃ 8
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  0 ┃ 0 ┃       ┃           ┃       ┃   ┃       ┃   ┃       ┃ 3 > 9
    ┗━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻ ^ ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```
Of course that will not always happen!

## Example 2 - changing the sense vertically

We might prefer the reversed identification to be along the bottom and top edges.  That can be done with the parity option:
```
>>> maze = Maze(KleinGrid(10, 15, parity=True))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       60
                             cells      150
                          passages      149
                 paths constructed       60
                     cells visited     1287
                          circuits      351
                    markers placed      876
                   markers removed      727
                     starting cell  (7, 9)
>>> print(unicode_str(maze, h="N", s="A", n="R"))
      O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳   ┳   ┳   ┳━━━┳   ┳   ┳   ┳   ┳━━━┳━━━┳━━━┳━━━┳━━━┳   ┓
  9 ┃   ┃   ┃           ┃       ┃   ┃   ┃               ┃   ┃   ┃ 9
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ┫
  8     ┃   ┃       ┃       ┃               ┃       ┃   ┃         8
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  7 ┃           ┃   ┃   ┃       ┃       ┃   ┃   ┃               ┃ 7
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ┫
  6     ┃   ┃           ┃   ┃   ┃   ┃           ┃       ┃   ┃     6
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃   ┃   ┃           ┃               ┃       ┃   ┃   ┃ 5
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  4 ┃   ┃   ┃       ┃   ┃           ┃   ┃   ┃           ┃       ┃ 4
    ┣   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  3     ┃       ┃   ┃       ┃   ┃       ┃                         3
    ┣   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  2 ┃       ┃           ┃   ┃   ┃   ┃   ┃               ┃       ┃ 2
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  1         ┃   ┃       ┃           ┃   ┃   ┃   ┃   ┃             1
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  0                     ┃           ┃   ┃   ┃   ┃   ┃       ┃     0
    ┗   ┻━━━┻━━━┻━━━┻━━━┻━━━┻   ┻   ┻   ┻   ┻━━━┻   ┻   ┻   ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

This one also has a short traversal of the four corners.  Can you find it?

(Spoiler) Here it is:
```
      O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳   ┳   ┳   ┳━━━┳   ┳   ┳   ┳   ┳━━━┳━━━┳━━━┳━━━┳━━━┳ ^ ┓
  9 ┃ 1 ┃   ┃           ┃       ┃   ┃   ┃               ┃   ┃ 2 ┃ 9
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ┫
  8 < * ┃   ┃       ┃       ┃               ┃       ┃   ┃     * < 8
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  7 ┃           ┃   ┃   ┃       ┃       ┃   ┃   ┃               ┃ 7
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ┫
  6     ┃   ┃           ┃   ┃   ┃   ┃           ┃       ┃   ┃     6
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  5 ┃   ┃   ┃   ┃   ┃           ┃               ┃       ┃   ┃   ┃ 5
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  4 ┃   ┃   ┃       ┃   ┃           ┃   ┃   ┃           ┃       ┃ 4
    ┣   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  3     ┃       ┃   ┃       ┃   ┃       ┃                         3
    ┣   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  2 ┃       ┃           ┃   ┃   ┃   ┃   ┃               ┃       ┃ 2
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  1         ┃   ┃       ┃           ┃   ┃   ┃   ┃   ┃             1
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  0 < 3                 ┃           ┃   ┃   ┃   ┃   ┃       ┃ 4 < 0
    ┗ ^ ┻━━━┻━━━┻━━━┻━━━┻━━━┻   ┻   ┻   ┻   ┻━━━┻   ┻   ┻   ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```
Just five passages!