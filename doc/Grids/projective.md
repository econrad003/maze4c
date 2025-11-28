# The real projective planar grid

## Revised: 27 November 2025

The corner cells are now handled correctly.

## Introduction

A real projective plane is a surface that, like the Klein bottle, can be realized in four dimensions, but not in three.  It can be constructed from a rectangle by identifying both pairs of opposite sides individually in the opposite sense (as in constructing a Möbius strip).  We can do the same thing starting with a rectangular grid...

We offer a single example keeping comments to a minimum.  (You might want to look over the documentation for cylindrical, Möbius strip, and Klein bottle grids to get some insight.)  There is, however, one special peculiarity of the projective grid that does require comment.  This is a very unusual grid!

### Example 1 The projective grid

We begin with some imports, namely a grid class (*ProjectiveGrid*), our usual maze class (*Maze*), and a maze carving class (*Wilson*):
```
$ python
>>> from mazes.Grids.projective import ProjectiveGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
```
The corner cells of the rectangle require very special handing when the grid is configured.  The special handling is actually required so that they aren't special in the grid topology.  We will have more to say about that in a moment,  To help explain, we will label the corner cells and their neighborhoods.  To do that, we set the *label\_corners* option in the grid constructor,


```
>>> maze = Maze(ProjectiveGrid(8, 13, label_corners=True))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       41
                             cells      102     <--- NOTE!
                          passages      101
                 paths constructed       41
                     cells visited      380
                          circuits       82
                    markers placed      257
                   markers removed      156
                     starting cell  (2, 3)
>>> print(maze)
      M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳━━━┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳━━━┳━━━┳   ┳━━━┓
  7 ┃ x   e ┃   ┃   ┃   ┃       ┃   ┃   ┃         W ┃ O ┃ 0
    ┣   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  6 ┃ s ┃   ┃       ┃   ┃       ┃       ┃   ┃         S ┃ 1
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  5     ┃   ┃       ┃       ┃   ┃       ┃                 2
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  4 ┃       ┃   ┃   ┃       ┃   ┃           ┃   ┃         3
    ┣━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  3     ┃           ┃           ┃           ┃           ┃ 4
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ┫
  2     ┃   ┃           ┃   ┃       ┃           ┃         5
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
  1 ┃ N     ┃   ┃       ┃   ┃               ┃         n ┃ 6
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  0 ┃ O ┃ E         ┃       ┃   ┃   ┃   ┃   ┃     w ┃ x   7
    ┗   ┻   ┻━━━┻━━━┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
```

### Cells and the grid

**Locally:** Without looking at the cell's index and without dropping breadcrumbs, you can't tell where you are in the grid.  Each cell has a neighbor to the south, to the east, to the north, and to the south.

With the usual rectangular grid, you can get some information.  For example, if you look south and there is no cell, then you are in row 0.  If you look west and find nothing, you are in column 0.

Now in the grid pictured above, if (i) you drop a breadcrumb in the cell you are in, (ii) take steps north, and (iii) see the breadcrumb, then you are in one of the squares in column labelled G.  Yes, you can get information about the grid, but that requires landmarks (such as breadcrumbs, labels, passages, and indices).

**Globally:** There are 104 squares in the rectangle and there are 102 cells in the grid.  Two of the cells each occupy a pair of diagonally opposite corner squares, but the remaining 100 cells occupy one square each.  Each square is occupied by exactly one cell.

**Moving around in the rectangle:**  If you're in a cell which is somewhere in the bottom row (say the column labelled K *below*), and then step south, you end up in a cell in the top row of squares (in particular, the square which sits below the letter K).

The rows are labelled on the left: from 0 at bottom up to 7 at top; and on the right: from 7 at bottom down to 0 at top. Stepping west from the cell to the right of the 2 on the left takes you to the cell to the left of the 2 on the right.

**The corner squares:**  Two of them have been labelled "O" (upper case) and two have been labelled "x" (lower case).  The bottom left and the top right corner (capital "O") are occupied by a single cell.  Likewise, the top left and bottom right corners are both held by a single cell.  Cell O has four neighbors in squares labelled "S", "E", "N" and "W",  The neighbors of cell x are in squares labelled "s", "e", "n" and "w".


