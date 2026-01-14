# A different hunt and kill algorithm

The first implementation (in module *mazes.Algorithms.hunt\_kill*) of hunt and kill maintains a frontier set.  When the a visit fails to find a kill, *i.e.* when the current cell does not have an unvisited neighbor, the first version selects a random frontier cell.  (In this implementation, we convert the frontier set to a list and choose a random element using *random.choice()*.  This is presumably O(n) where n is the number of elements in the set.)

This version (in module *mazes.Algorithms.hunt\_kill2*) does not maintain a frontier.  Instead, when the visit fails to find a kill, this version scans the unvisited cells to find an unvisited cell with a visited neighbor.

This version will probably produce mazes which are less random.  For the oblong grid, the corridors will probably tend to have a horizontal bias.  I suspect this version also requires more time.  (These statements should be treated as conjecture -- they should probably be verified with some statistics.)

The implementation here is a drop-in replacement for the first version -- it uses the same class name (*HuntKill*).  Maze programmers might want to experiment by creating subclasses which replace the *HuntKill.Status.scan()* method.

## Example

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.hunt_kill2 import HuntKill
>>> maze = Maze(OblongGrid(8, 13))
>>> print(HuntKill.on(maze))
          Hunt/Scan and Kill (statistics)
                            visits      103
                             cells      104
                          passages      103
                              hunt       11
                              kill       92
                             scans      114
                     starting cell  (4, 4)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |           |               |
+   +---+---+   +   +   +---+   +   +---+---+   +---+
|   |       |   |   |   |       |           |       |
+   +   +   +   +   +   +   +---+---+---+   +---+   +
|   |   |       |   |   |   |       |   |           |
+---+   +---+---+   +   +   +---+   +   +---+   +---+
|       |       |   |   |       |   |       |       |
+   +---+   +   +---+   +---+   +   +---+   +---+---+
|   |       |       |                       |       |
+   +---+   +---+   +   +---+---+---+---+---+   +   +
|           |   |       |               |       |   |
+   +---+   +   +---+---+   +   +---+   +   +   +   +
|   |   |   |               |   |       |   |   |   |
+   +   +   +---+---+---+---+   +   +---+---+   +   +
|       |                       |               |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```