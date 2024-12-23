# Hunt and Kill

The hunt and kill algorithm is a modification of Aldous/Broder.  Instead of simply stepping at random, the hunt and kill algorithm on steps on unvisited cells.  Thus there are effectively no wasted visits.  The name comes from its two types of steps or visits:

1. *kill* - if the current cell has an unvisited neighbor, then an unvisited neighbor is chosen at random.  A passage is carved from the cell to the chosen neighbor, and the chosen neighbor becomes the current cell.
2. *hunt* - if the current cell does not have an unvisited neighbor, the a cell having at least one visited neighbor is chosen at random.  A passage is carved from the cell to one of its visited neighbors, and the cell becomes the current cell.

In our implementation, the visited area and a frontier are maintained as sets. The frontier consists of all unvisited cells with visited neighbors.

The algorithm tends to produce spanning trees with relatively large diameters and with relatively few dead ends.  (A dead end is node of degree 1, *i.e.* a cell with just one incident passage.)

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8,13))
    4> from mazes.Algorithms.hunt_kill import HuntKill
    5> print(HuntKill.on(maze))
          Hunt and Kill (statistics)
                            visits      103
                             cells      104
                          passages      103
                              hunt       13
                              kill       90
                     starting cell  (0, 4)
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |               |               |       |
    +   +   +---+   +---+---+   +   +   +---+   +   +   +
    |   |   |       |           |   |       |       |   |
    +---+   +   +   +   +---+---+---+---+   +---+---+   +
    |           |   |       |               |       |   |
    +   +---+---+   +---+   +---+   +---+---+   +   +---+
    |       |       |               |           |       |
    +---+   +   +---+   +---+---+---+   +   +---+---+   +
    |       |       |               |   |   |           |
    +---+---+   +   +---+---+---+   +---+   +   +   +---+
    |           |   |       |       |       |   |   |   |
    +   +---+---+   +   +---+   +---+   +---+---+   +   +
    |       |   |   |           |       |           |   |
    +---+   +   +   +---+---+   +   +---+   +---+---+   +
    |           |       |           |                   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```