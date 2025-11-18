# The DFS circuit locator

## Setup

Before use the circuit locator, we need a maze which has some circuits.  The easiest way to do this is to configure a grid, wrap it in a maze object, and use the maze's *link\_all()* method.  We start in the Python interpreter with a couple of imports:
```
$ python
Python 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
```

And now we prepare a maze with lots of circuits.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> maze.link_all()
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

There is just one component, so how many passages do we need to rease to get a perfect maze?
```
>>> v, e = len(maze.grid), len(maze)
>>> print(f"{v=}, {e=}")
v=104, e=187
>>> e-v
83
```
We need to erase 84 passages without disconnecting the maze!

## Locating and eliminating a circuit

We will use the DFS circuit locator.  It works like most of our algorithms, but if we nee to do anything but locate one edge in a circuit, we will need to use the status object.  (Don't wrap the *on()* method in a *print()* statement!)  So one import, save the status, and then we can do some work... We can, of course, *print* the saved status...
```
>>> from mazes.Algorithms.dfs_circuit_locator import CircuitFinder
>>> status = CircuitFinder.on(maze)
>>> print(status)
          DFS Circuit Locator (statistics)
                            visits       20
                        start cell  (0, 11)
                  components found        1
               components finished        0
                     cells visited       14
                           shuffle        1
               maximum stack depth       14
                           circuit  ((5, 5), (4, 5))
```
The last line is the edge which was located.  Notice that quite a bit of work was required to find a circuit.  So where is the circuit?  The status provides two tools for accessing the entire circuit.  The *circuit* property returns the cells in the circuit, and the *label\_circuit* method will label the circuit for you, with asterisks by default:
```
>>> status.circuit
[SquareCell object, SquareCell object, SquareCell object, SquareCell object]
>>> len(status.circuit)
4
>>> status.label_circuit()
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                 *   *                             |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                 *   *                             |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Of course we haven't done anything to the maze.  We need to remove a passage.  Is there an easy way?  The *result* property returns *None* if no circuit was found.  If a circuit was found it returns three pieces of information:

* the cell at the top of the stack;
* the edge or arc that completed the circuit; and
* the cell that was previously visited.

If we aren't sure (as in a program), we should use an *if* structure, for example:
```python
          status = CircuitFinder.on(maze)
          if status.result:
                  # there is a circuit
              cell1, edge, cell2 = status.result
              do_something_with(maze, status.circuit)
          else:
                  # there is no circuit
              no_circuit_action(maze)
```

For our demonstration, we only need to remove the passage:
```
>>> cell1, edge, cell2 = status.result
>>> maze.unlink(edge)
```
Breaking a circuit does not increase the number of components, so we now have only 83 passages that we need to remove.  Of course each one must be in a circuits when it is removed.  Just to be sure:
```
>>> v, e = len(maze.grid), len(maze)
>>> print(f"{v=}, {e=}")
v=104, e=186
>>> e-v
82
```
Yes, 83 more passages, one more than the difference...  Here is the maze as it stands with just one wall:
```

>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                 *   *                             |
+   +   +   +   +   +---+   +   +   +   +   +   +   +
|                 *   *                             |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Let's erase those asterisks:
```
>>> status.label_circuit(label=" ")
```

And let's erect another wall:
```
>>> status = CircuitFinder.on(maze)
>>> cell1, edge, cell2 = status.result
>>> maze.unlink(edge)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +---+   +   +   +   +   +   +   +
|                                                   |
+   +   +---+   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Two down, 82 to go...  As a tribute to Douglas Adams, let's do 42 more:
```
>>> for _ in range(42):
...     status = CircuitFinder.on(maze)
...     cell1, edge, cell2 = status.result
...     maze.unlink(edge)
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +---+   +   +   +---+   +   +   +
|                   |   |                       |   |
+   +---+   +   +   +   +   +   +   +   +---+   +   +
|   |       |                                       |
+---+   +---+   +   +---+   +   +---+   +   +   +   +
|           |   |                           |   |   |
+   +---+---+   +   +   +   +   +   +---+   +   +   +
|       |       |       |                       |   |
+   +   +   +   +---+---+   +   +   +   +---+   +   +
|   |   |                           |               |
+   +   +   +---+   +   +---+   +   +---+   +   +   +
|       |           |   |   |   |           |       |
+---+   +---+   +---+   +   +   +   +   +   +---+   +
|           |                                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> v, e = len(maze.grid), len(maze)
>>> print(f"{v=}, {e=}")
v=104, e=143
>>> e-v
39
```
44 down, 40 to go.  Let's look at the last status:
```
>>> print(status)
          DFS Circuit Locator (statistics)
                            visits        7
                        start cell  (3, 8)
                  components found        1
               components finished        0
                     cells visited        6
                           shuffle        1
               maximum stack depth        6
                           circuit  ((1, 9), (2, 9))
>>> status.label_circuit(); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +---+   +   +   +---+   +   +   +
|                   |   |                       |   |
+   +---+   +   +   +   +   +   +   +   +---+   +   +
|   |       |                                       |
+---+   +---+   +   +---+   +   +---+   +   +   +   +
|           |   |                           |   |   |
+   +---+---+   +   +   +   +   +   +---+   +   +   +
|       |       |       |                       |   |
+   +   +   +   +---+---+   +   +   +   +---+   +   +
|   |   |                           | *   *         |
+   +   +   +---+   +   +---+   +   +---+   +   +   +
|       |           |   |   |   |     *   * |       |
+---+   +---+   +---+   +   +   +   +   +   +---+   +
|           |                                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We can see the circuit that we "broke" when we erected the newest wall.

Let's erase those breadcrumbs and do the remaining 40 walls:
```
>>> status.label_circuit(label=" ")
>>> for _ in range(40):
...     status = CircuitFinder.on(maze)
...     cell1, edge, cell2 = status.result
...     maze.unlink(edge)
... 
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |           |                   |
+   +---+   +---+   +---+   +   +---+---+   +---+   +
|   |       |   |   |   |   |       |       |   |   |
+   +---+   +   +   +   +   +---+   +   +---+   +   +
|   |       |           |   |   |       |       |   |
+---+   +---+   +---+---+---+   +---+---+---+   +   +
|           |   |   |           |           |   |   |
+   +---+---+   +   +   +   +---+---+---+   +   +   +
|   |   |       |       |   |               |   |   |
+   +   +   +   +---+---+   +   +   +   +---+   +   +
|   |   |   |       |   |       |   |       |       |
+   +   +   +---+   +   +---+   +   +---+   +   +---+
|       |   |       |   |   |   |   |       |       |
+---+   +---+   +---+   +   +---+   +---+   +---+   +
|           |                       |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> v, e = len(maze.grid), len(maze)
>>> print(f"{v=}, {e=}")
v=104, e=103
```
This is our final maze.  It should not have any circuits...
```
>>> status = CircuitFinder.on(maze)
>>> status.result
>>> print(status)
          DFS Circuit Locator (statistics)
                            visits      311
                        start cell  (1, 8)
                  components found        1
               components finished        1
                     cells visited      104
                           shuffle        1
               maximum stack depth       31
                           circuit  None
```
We did not see a response to *status.result*, so the value is *None*.  And displaying the status confirms the result.

## A wall builder

Collecting the details above gives us a simple implementation of a wall building algorithm:

```python
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.dfs_circuit_locator import CircuitFinder

def wallbuilder(rows, cols):
    """perfect maze creation by erecting walls"""
    maze = Maze(OblongGrid(rows, cols))
    maze.link_all()
    v, e = len(maze.grid), len(maze)
    chi = e - v + 1
    for _ in range(chi):
        status = CircuitFinder.on(maze)
        cell1, edge, cell2 = status.result
        maze.unlink(edge)
    v, e = len(maze.grid), len(maze)
    chi = e - v + 1
    print(f"{e=}, {v=}, {chi=}")
    return(maze)
```

## Testing the wallbuilder:

```
 python
Python 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.dfs_circuit_locator import CircuitFinder
>>> 
>>> def wallbuilder(rows, cols):
...     """perfect maze creation by erecting walls"""
...     maze = Maze(OblongGrid(rows, cols))
...     maze.link_all()
...     v, e = len(maze.grid), len(maze)
...     chi = e - v + 1
...     for _ in range(chi):
...         status = CircuitFinder.on(maze)
...         cell1, edge, cell2 = status.result
...         maze.unlink(edge)
...     v, e = len(maze.grid), len(maze)
...     chi = e - v + 1
...     print(f"{e=}, {v=}, {chi=}")
...     return(maze)
...
>>> maze = wallbuilder(10, 16)
e=159, v=160, chi=0
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |                       |   |           |   |
+   +---+   +---+   +   +---+---+---+---+   +   +   +---+   +   +
|   |   |               |                   |   |       |   |   |
+   +   +---+---+---+---+   +---+---+   +---+   +---+   +   +   +
|   |               |   |   |       |       |   |       |       |
+---+   +---+---+---+   +   +   +   +---+---+   +   +   +---+   +
|                       |       |   |       |       |   |       |
+   +---+---+---+   +---+---+   +   +   +   +---+---+---+   +---+
|       |       |   |       |   |   |   |           |       |   |
+---+   +---+   +   +   +---+   +---+---+---+---+   +   +---+   +
|       |           |       |       |       |       |   |       |
+   +   +---+---+   +   +   +   +   +   +---+   +---+   +   +   +
|   |           |       |       |   |       |   |           |   |
+   +---+---+   +---+   +---+---+   +---+   +   +---+   +   +   +
|   |       |   |               |           |   |       |   |   |
+   +   +   +   +---+---+---+---+---+   +---+   +---+---+   +   +
|   |   |   |   |           |   |       |       |           |   |
+   +---+   +   +   +---+   +   +   +   +   +---+   +   +---+---+
|           |           |       |   |               |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Let's bring in the Dijkstra toolbox and compare this to a DFS maze.  The maze is a tree, so we can calculate its diameter using the toolbox:
```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> dijkstra.distance(dijkstra.farthest)
64
```
The diameter is 64 passages.

How about DFS? Well...
```
>>> from mazes.Algorithms.dfs_better import DFS
>>> maze2 = Maze(OblongGrid(10,16))
>>> print(DFS.on(maze2))
          Depth-first Search (DFS) (statistics)
                            visits      319
                        start cell  (7, 15)
               maximum stack depth      102
                             cells      160
                          passages      159
>>> dijkstra2 = Dijkstra(maze2, maze2.grid[0,0])
>>> source2 = dijkstra2.farthest
>>> dijkstra2.calculate(source2)
>>> dijkstra2.distance(dijkstra2.farthest)
101
```
The maximum stack depth was 102 cells, so the diameter is 101 passages.  The Dijkstra toobox agrees.  Athough circuit detection used depth-first search, the wall builder doesn't tend to produce a large diameter.

Here are results for Wilson's algorithm:
```
>>> from mazes.Algorithms.wilson import Wilson
>>> maze3 = Maze(OblongGrid(10,16))
>>> print(Wilson.on(maze3))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       74
                             cells      160
                          passages      159
                 paths constructed       74
                     cells visited      469
                          circuits      101
                    markers placed      294
                   markers removed      135
                     starting cell  (4, 4)
>>> dijkstra3 = Dijkstra(maze3, maze3.grid[0,0])
>>> source3 = dijkstra3.farthest
>>> dijkstra3.calculate(source3)
>>> dijkstra3.distance(dijkstra3.farthest)
49
```
If these results are typical, then our wall builder is not uniform and produces mazes with larger than average diameters, but much smaller than those produced by DFS.

Here is a longest path (or diameter path):
```
>>> dijkstra.label_path(sink)                 |
>>> print(maze)                               V
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |                       | S | *   *   * |   |
+   +---+   +---+   +   +---+---+---+---+   +   +   +---+   +   +
|   |   |               |                   | * | *   * | * |   |
+   +   +---+---+---+---+   +---+---+   +---+   +---+   +   +   +
|   |               |   |   |       |       | * | *   * | *   * |
+---+   +---+---+---+   +   +   +   +---+---+   +   +   +---+   +
| *   *   *   *   *     |       |   |       | *   * |   | *   * |
+   +---+---+---+   +---+---+   +   +   +   +---+---+---+   +---+
| *   * |       | * |       |   |   |   |           | *   * |   |
+---+   +---+   +   +   +---+   +---+---+---+---+   +   +---+   +
|     * |         * | *   * | *   * |       |       | * |       |
+   +   +---+---+   +   +   +   +   +   +---+   +---+   +   +   +
|   | *   *   * | *   * | *   * | * |       |   |     *   * |   |
+   +---+---+   +---+   +---+---+   +---+   +   +---+   +   +   +
|   |       | * |               | *   *     |   |       | * |   |
+   +   +   +   +---+---+---+---+---+   +---+   +---+---+   +   +
|   |   |   | * | *   *   * | T |     * |       | *   *   * |   |
+   +---+   +   +   +---+   +   +   +   +   +---+   +   +---+---+
|           | *   *     | *   * |   | *   *   *   * |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```