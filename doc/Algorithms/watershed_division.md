# Recursive division using watersheds

The algorithm is essentially the same as rectangular recursive division, but instead of dividing horizontally or vertically, we divide a connected region aribitrarily into several connected sub-regions.  As in rectangular recursive division, we complete the process by separating the sub-regions and connecting the system with some passages between the subregions.  For a more detailed look a how this is done, see the documentation file *watershed.md* in the *doc* folder.  The algorithm is implemented as a passage carver, so one starts with an empty connected grid.  (The algorithm is commonly implemented as a wall builder, but it really can be implemented either way.)

In the discussion for each example below, we start with an unlinked connected grid.  We will use a rectangular grid, but the algorithm doesn't require that.  Before proceeding, we should look at the options...

## Options

The module documentation is terse:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.watershed_division import WatershedDivision
>>> help(WatershedDivision.Status.parse_args)
Help on function parse_args in module mazes.Algorithms.watershed_division:

parse_args(self, min_cells: int, pumps: (int, callable), *args,
        ReservoirType: object=Reservoir, SchedulerType:object = None,
        targs:tuple=(), error_action:('ignore', 'fix')='ignore',
        carve_rooms:bool=False, label_rooms:bool= False,
        extra_pumps_trace:bool=False, **kwargs)

    parse constructor arguments

    POSITIONAL ARGUMENTS

        maze - handled by __init__ in the base class.
        min_cells   the minimum number of cells in a subdividable
                basin.  This value must be at least 2.
        pumps       this can either be a fixed integer or a function
                of the number of cells, as with fewer cells, we might
                want fewer pumps.

            For example, consider the following pump function:
                def pumps(cells:int):
                    return 4 if cells > 100 else 2
            If there are more than 100 cells in a given basin,
            the number of pumps will be set at 4, yield smaller
            subdivisions than if two pumps are used.  This will
            tend to result in fewer levels of recursion.
        args    additional positional arguments

    KEYWORD ARGUMENTS
     *  debug (default=False)
            set to True for detailed stack analysis
        ReservoirType (default=Reservoir defined above)
            can be modified to change the way the algorithm
            recursively subdivides the grid.
        WatershedType (default=Watershed defined in mazes.watershed)
            the watershed object type.
     *  FloodgateCarver (default=Kruskal)
            a passage carving algorithm to be used to carve the
            floodgates (doors).

            Kruskal's algorithm is preferred since it can accept
            a disconnected grid and reports the number of components.
            Use of an algorithm that forbids disconnected grids
            (like Aldous/Broder) may result in unpredictable
            failures.
        error_action (default='ignore')
            the possible values are 'ignore' or 'fix'.
                'ignore' - if there are disconnected basins, a
                    message will be printed but no action will
                    be taken at the end to connect the maze.
                'fix' - if there are disconnected basins, a
                    message will be printed, and Kruskal's
                    algorithm will be used at the end to connect
                    the maze.  This option is not available if
                    the cell minimum is larger than two unless
                    rooms are carved.
        extra_pumps_trace (default=False)
            set to True to get basin information for extra pumps.
            See the documentation for more details.
     *  QueueType (default=maze.Queues.Queue)
            a queuing type.
     *  qargs (default={})
            queuing arguments (e.g. for type PriorityQueue)
        SchedulerType (default=maze.Tournament)
            a scheduler type
        targs (default={})
            task arguments for the scheduler (e.g. tournament task weights)
        carve_rooms (default=False)
            if True, rooms will be carved when the subgrid is
            too small to subdivide.  This will make no difference
            if min_cells is equal to 2.
        label_rooms (default=False)
            if true, the cells in the basin will be labelled.  The
            labels will only be displayed in console displays, so
            they are of no use for grids that can only be displayed
            as graphic objects.
        kwargs
            unparsed keyword arguments to pass to the ReservoirType
            object

    Except for "debug", the starred arguments are carried in "kwargs"
    and passed along for parsing in the Reservoir and Watershed
    initializations.  The "debug" option is both parsed and passed
    along.
```

The error action and extra pumps trace options are for debugging.  The problem that they were intended to detect turned out to be unrelated to the algorithm.

The scheduler type option and the task arguments  option ("targs") are new (as of v0.10.9).  The original implementation used a round robin scheduler.  The current default is a tournament scheduler with equally weighted tasks.  This change will affect the algorithms biases.  Examples 1 through 5 below were created using the original implementation and there may be some minor qualitative differences with the updated module.  See Examples 6, 7 and 8 for more information on these two options.

## Example 1.  A simple example.

There are three required arguments, namely a Maze object, the number of cells required for subdividing a region, and the number of pumps.  The mininum number of cells must be at least 2.  (If a value less than 2 is entered, 2 will be used.)  In addition, the number of pumps must be at least 2 and can depend on the number of cells in the region being subdivided.  For our example, we will use 2 cells as the minimum subdividable region and 3 as the number of pumps.  A region with 3 or more cells will thus be subdivided into 3 basins, while a region of two cells will have just two subdivisions of one cell each.

We start with three imports:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.watershed_division import WatershedDivision
```

Next we create a connected grid and embed it in a maze object:
```
>>> maze = Maze(OblongGrid(10,15))
```

Now we run the watershed recursive division algorithm with a minimum of 2 cells and 3 pumps per basin:

```
>>> print(WatershedDivision.on(maze, 2, 3))
          Watershed Recursive Division (statistics)
                            visits      311
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack       10
```
The number of cells exceeds the number of passages by 1, a necessary condition for a perfect maze.  (To be sufficient, the maze must be connected.)

Here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |                                           |   |       |
+   +---+---+---+   +---+---+---+---+---+   +---+   +   +   +
|           |               |               |           |   |
+---+---+   +---+   +---+   +---+---+   +---+   +   +---+   +
|       |   |       |           |   |           |   |   |   |
+---+   +   +   +---+   +---+---+   +---+---+   +   +   +   +
|   |       |       |       |           |   |   |   |       |
+   +   +---+   +   +   +---+---+---+   +   +---+---+   +---+
|           |   |   |   |               |           |       |
+   +---+---+   +---+---+---+   +---+   +---+   +---+   +---+
|       |   |   |   |               |       |   |       |   |
+---+   +   +   +   +   +---+   +---+   +   +   +   +   +   +
|           |   |   |   |   |   |   |   |           |       |
+---+---+   +   +   +   +   +   +   +   +---+---+---+---+---+
|               |   |       |       |                       |
+   +---+---+---+   +---+---+---+   +---+---+   +---+   +---+
|       |               |       |   |           |   |       |
+   +---+   +---+   +   +---+   +---+   +---+   +   +---+---+
|               |   |       |           |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 2.  A room plan.

The option *carve\_rooms* allows us to carve rooms whenever the basin size is below the minimum.

```
>>> maze = Maze(OblongGrid(10,15))
>>> print(WatershedDivision.on(maze, 30, 3, carve_rooms=True))
          Watershed Recursive Division (statistics)
                            visits       10
                             cells      150
                          passages        0
                             links      227
                           unlinks        0
                             doors        6
                         max stack        4
                             rooms        7
                        room links      221
```
We ended up with 7 rooms, each with no more than 29 cells (since the minimum number of cells, the second argument, was 30).  There were 6 "doors", one less than the number of rooms.  Viewed a a maze of weirdly shaped rooms on a floor in a haunted house, it is a perfect maze.  221 of the 227 links are simply passages between two cells in the same room.

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                           |               |
+   +   +   +   +   +   +   +   +   +   +---+   +   +   +   +
|                   |                                       |
+   +   +   +   +   +   +   +   +   +---+   +   +   +   +   +
|                   |               |                       |
+   +   +   +   +   +   +   +---+---+---+---+---+---+---+---+
|                   |       |                               |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|               |           |                               |
+---+   +   +   +   +   +   +---+---+   +   +   +   +   +   +
|   |           |       |           |                       |
+   +---+---+   +---+---+   +   +   +---+---+---+   +---+---+
|           |   |       |           |                       |
+   +   +   +---+   +---+   +   +   +---+   +   +   +   +   +
|                   |                   |                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                       |                   |
+   +   +   +   +   +---+   +   +   +   +---+   +   +   +   +
|                       |                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

If we take out the isolated plus symbols, the floor plan might be more obvious.  We can also number the rooms, though, in the case of rooms 5 and 6 below, it isn't clear to which room the cell that joins them belongs.
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                           |               |
+                   +                   +---+               +
|                   |                               3       |
+                   +               +---+                   +
|        1          |               |                       |
+                   +   2   +---+---+---+---+---+---+---+---+
|                   |       |                               |
+               +---+       +                               +
|               |           |                 4             |
+---+           +       +   +---+---+                       +
|   |           |       |           |                       |
+   +---+---+   +---+---+           +---+---+---+   +---+---+
|           |   |       |           |                       |
+           +---+   +---+           +---+                   +
|                   |        6          |                   |
+                   +                   +        5          +
|       7                               |                   |
+                   +---+               +---+               +
|                       |                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Setting the *label\_rooms* option to True would have marked every cell in a room with the same label.

## Example 3. Rooms without doors.

The door carving is based on an auxiliary maze which shows how regions are connected in the grid.  By default, that maze is carved using Kruskal's algorithm.  (The number of cells in that maze is always the same as the number of pumps.  So the number of grid connections is small.  With two pumps, Kruskal's algorithm will take just one visit to carve a link.  (For more information, about the choice of Kruskal's algorithm for carving floodgates, see Example 6 below.)

We could also simply not carve any doors at all.  It would not make sense if we set the minimum basin size to 2 cells.  But could set a larger minimum.

First, we design a maze algorithm which does nothing:

```
>>> class Foobar(object):
...     @staticmethod
...     def on(maze:Maze):
...         """do nothing"""
...         return "Nothing happens"
...
```

Next we create the maze using the watershed algorithm:
```
>>> maze = Maze(OblongGrid(10,15))
>>> print(WatershedDivision.on(maze, 30, 3, carve_rooms=True, FloodgateCarver=Foobar))
          Watershed Recursive Division (statistics)
                            visits       13
                             cells      150
                          passages        0
                             links      199
                           unlinks        0
                             doors        0
                         max stack        5
                             rooms        9
                        room links      199
```

Now the only links are room links.  Here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |           |                                       |
+   +   +   +   +---+   +   +   +   +   +---+   +   +   +---+
|       |       |                       |   |           |   |
+   +   +   +   +---+---+---+---+---+---+   +---+---+---+   +
|       |       |                   |               |       |
+   +   +   +   +   +   +---+   +   +   +   +   +   +   +   +
|       |       |       |   |       |               |       |
+   +   +   +   +---+---+   +---+---+   +   +   +   +   +   +
|       |           |               |               |       |
+   +   +---+---+   +   +   +   +---+---+---+---+---+---+   +
|           |   |   |           |                       |   |
+   +   +---+   +---+   +   +   +   +   +   +   +   +   +   +
|       |       |               |                       |   |
+---+---+   +---+   +   +   +   +   +   +   +   +   +---+   +
|           |                   |                   |       |
+   +   +   +   +   +   +   +   +   +---+   +   +   +   +   +
|           |                   |   |   |           |       |
+   +   +   +   +   +   +   +   +---+   +---+---+---+   +   +
|           |                   |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

9 rooms and no doors!  And notice that room shapes can get pretty wild!

If we had set *debug=True*, we would have seen that "Nothing happens" message several times in the resulting trace..

## Example 4. A floor plan using stacks.

The watersheds by default use queues, so the filling algorithm is basically a modified breadth-first search.  With three pumps we can think of it as a game between three players to claim property.  Each player starts some place.  They place neighbors in a queue, but they can only claim the least recent available neighbor.

We can also use other queuing objects such as stacks and priority queues.  With a stack, the underlying game is based on depth-first search.

As with the previous example, we will not carve any doors.  We will use just two pumps.  Just as depth-first search tends to create mazes with long twisty passages, we might expect our rooms to be long and twisty.  But bear in mind that this isn't solitaire -- with two pumps, it's two players in competition -- the round-robin algorithm in the watershed object insures that unless one player is blocked, both players can claim a cell...

We need access to the *Stack* class:
```
>>> from mazes.Queues.stack import Stack
```

We change the number of pumps to 2 and add the *QueueType* option:
```
>>> maze = Maze(OblongGrid(10,15))
>>> print(WatershedDivision.on(maze, 30, 2, carve_rooms=True, FloodgateCarver=Foobar, QueueType=Stack))
          Watershed Recursive Division (statistics)
                            visits       17
                             cells      150
                          passages        0
                             links      192
                           unlinks        0
                             doors        0
                         max stack        4
                             rooms        9
                        room links      192
```

Our auxiliary maze carving algorithm *Foobar* does not carve any passages, so we're left with some rooms with no doors.  In the result below, note the cell that we marked with an X.  Was it's shape somehow related to our queuing algorithm?  And consider the room containing the cell marked with a Y...
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |               |                   |           |
+   +   +   +   +   +   +   +---+---+---+---+---+---+   +   +
|     Y     |                   |                   |       |
+   +   +   +---+   +   +---+---+   +   +   +---+   +---+   +
|               |       |                   |   |       |   |
+---+---+   +   +   +   +   +   +   +   +   +   +---+---+   +
|   |   |       |       |                   |               |
+   +   +   +   +   +   +   +   +   +---+---+   +   +   +   +
|   |   |       |       |           |       |               |
+   +   +---+   +---+---+   +   +   +   +---+   +   +   +   +
|   |       |           |           |   |                   |
+   +---+   +   +   +   +---+---+---+---+---+   +   +   +   +
|       |   |                   |           |               |
+   +   +   +---+   +   +   +   +---+   +---+---+---+---+   +
|       |       |                   |   |               |   |
+   +   +---+   +   +   +---+---+---+---+   +   +   +---+   +
|           |   |       |                           |       |
+   +   +   +   +---+---+   +   +   +   +   +   +   +   +   +
|           |                     X                 |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 5A.  A watershed recursive maze using stacks.

```
>>> maze = Maze(OblongGrid(10,15))
>>> print(WatershedDivision.on(maze, 2, 2, QueueType=Stack))
          Watershed Recursive Division (statistics)
                            visits      379
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack       11
```

Before we display the maze, let's find a longest path using Dijkstra's algorithm.

```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> cell0 = maze.grid[0,0]
>>> dijkstra = Dijkstra(maze, cell0)
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> sink = dijkstra.farthest
>>> dijkstra.distance(sink)
48
```

So a longest path in the maze covers almost a third of the maze.  Now let's look at the maze and the longest path found.  The source is S and the sink (or target) is T:
```
>>> dijkstra.label_path(sink)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| *   *     | *   *     |   |   |   |           |       |   |
+   +   +---+   +   +---+   +   +   +   +---+---+---+   +   +
| * | *   T | * | *     |                               |   |
+   +---+---+   +   +---+---+---+---+---+---+---+   +---+   +
| *   *   *   * | *     |       | *   S |     *   * |       |
+   +---+---+   +   +   +---+   +   +---+---+   +   +   +---+
|           |   | * |       |   | * | *   *   * | *   *     |
+---+---+   +---+   +---+---+   +   +   +---+---+---+   +   +
|   |       | *   * |     *   * | *   * | *   *   *   * |   |
+   +---+   +   +---+---+   +   +---+---+   +---+   +   +   +
|       |   | * |   |     * | *   *   *   * |       |   |   |
+   +   +---+   +   +---+   +   +---+   +---+---+---+---+   +
|   |   | *   * | *   *   * |   |               |   |       |
+---+   +   +---+   +---+---+---+---+   +---+   +   +   +---+
|       | *   *   *             |           |       |       |
+   +   +---+---+---+   +   +   +---+---+   +---+---+   +   +
|   |       |           |   |   |       |           |   |   |
+   +---+---+---+---+   +   +   +   +   +---+   +---+---+   +
|                       |   |   |   |           |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Of course a single example is evidence of almost nothing...

## Example 5B.  Longest path in a queue-based maze.

Let's run the same experiment with queues instead of stacks...

```
>>> maze = Maze(OblongGrid(10,15))
>>> print(WatershedDivision.on(maze, 2, 2))
          Watershed Recursive Division (statistics)
                            visits      386
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        9
```

Now run Dijkstra's longest path algorithm:
```
>>> cell0 = maze.grid[0,0]
>>> dijkstra = Dijkstra(maze, cell0)
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> sink = dijkstra.farthest
>>> dijkstra.distance(sink)
57
```
Longer than with stacks, but bear in mind that this is a single example.  (In the absence of conclusive evidence, always keep an open mind!)

Now mark the path and display the maze.
```
>>> dijkstra.label_path(sink)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |         *   * | *   *   * |     *   *         |
+---+   +   +---+---+   +   +   +---+   +   +   +   +---+---+
|   | *   *   * |   | * | *   * | T   * |   | * | *   *   * |
+   +   +   +   +   +   +---+   +---+---+---+   +---+   +   +
|     * |   | *   *   * |       |       |     * |       | * |
+---+   +---+   +---+   +---+---+   +---+---+   +   +---+   +
|     *   * |       |   |   |           | *   * |   | *   * |
+---+---+   +---+   +   +   +   +---+   +   +---+   +   +---+
|       | * |       |   |       |   |   | S |       | * |   |
+   +---+   +---+---+---+   +---+   +---+---+---+---+   +   +
|   |     *   * |   |   |           |       |       | *   * |
+   +   +---+   +   +   +   +   +---+   +   +   +---+---+   +
|           | *     |   |   |       |   |       |         * |
+---+---+---+   +   +   +   +---+   +   +---+---+---+---+   +
|             * |           |       |   |       | *   * | * |
+   +---+---+   +---+---+---+---+   +   +---+   +   +   +   +
|   |       | *   *   *   * |       | *   *   *   * | *   * |
+---+---+   +---+   +---+   +---+---+   +---+---+---+---+---+
|                       | *   *   *   *                     |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The longest path in the previous example tended to be bunched up like a partially coiled snake.   In this example, the path was more like a travelling snake -- not straight, but with very little coiling,

## Example 5C. Comparison with depth-first search

For comparison, we consider depth-first search:

```
>>> from mazes.Algorithms.dfs import DFS
>>> maze = Maze(OblongGrid(10,15))
>>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      241
                        start cell  (0, 13)
               maximum stack depth      117
                             cells      150
                          passages      149
>>> cell0 = maze.grid[0,0]
>>> dijkstra = Dijkstra(maze, cell0)
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> sink = dijkstra.farthest
>>> dijkstra.distance(sink)
93
```
In this example, a longest path occupies almost 2/3 of the grid.  Apparently the change from queues to stacks in the watersheds isn't as dramatic as the change from stacks to queues in growing tree algorithms.

For comparison, here is a longest path produced in DFS.  That's one long snake!
```
>>> dijkstra.label_path(sink)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| T   *   *   *   *   *     | *   *   *   *   *   * | S   * |
+---+---+---+---+---+   +---+   +---+---+---+   +   +---+   +
| *   * | *   *   *   * | *   * |           |   | *   * | * |
+   +   +   +---+---+---+   +---+   +   +---+   +---+   +   +
| * | * | *   *   * | *   * |       |       |       | * | * |
+   +   +   +---+   +   +---+---+---+---+   +---+   +   +   +
| * | * |       | * | * | *   *   * |       |       | * | * |
+   +   +---+---+   +   +   +---+   +   +   +   +---+   +   +
| * | *   * | *   * | *   * |   | *   * |   |   | *   * | * |
+   +---+   +   +---+---+---+   +---+   +---+   +   +---+   +
| *   * | *   * | *   *   *   * | *   * |       | *   * | * |
+   +   +---+---+   +---+---+   +   +---+   +---+---+   +   +
|   | *   *   * | * |   | *   * | * |   |           | *   * |
+   +---+---+   +   +   +   +   +   +   +---+---+   +---+   +
|   |   | *   * | * |   | * |   | *   *   * |   |       |   |
+   +   +   +   +   +   +   +---+---+---+   +   +---+   +---+
|       | * |   | * |   | *   *   *   *   * |       |       |
+---+   +   +---+   +   +---+---+---+---+---+---+   +---+   +
|       | *   *   *                                 |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 6 - round robin scheduling

Examples 1 through 5 above were created when round robin scheduling was hard-coded.  The current scheduling algorithm is an equally weighted tournament.  But round robin scheduling is still available using the *RoundRobin* class.

We start with some imports:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.watershed_division import WatershedDivision
>>> from mazes.round_robin import RoundRobin
```

Watershed division is a passage carver that can be used with any connected grid.  We use a N/S/E/W rectangular grid to make it easy to display the result.  We need a maze object:
```
>>> maze = Maze(OblongGrid(10, 15))
```

We will use a minimum basin size of two (the default) and we will use 3 pumps to form the basins and fill the reservoir.  Each pump is associated with a task that shoots a shoots a small jet of water -- just enough to claim one more cell for the pumps basin.  In a round robin, each pump takes one turn *in order*.  Pump 1 takes a turn, then pump 2, then pump 3, then back to pump 1.  But if there are no cells next to a given basin, then that pump loses all subsequent turns.

```
>>> print(WatershedDivision.on(maze, 2, 3, SchedulerType=RoundRobin))
          Watershed Recursive Division (statistics)
                            visits      313
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack       10
                       extra pumps        0
                  watershed errors        0
```

With 150 cells, we expect 149 passages in the final maze.  Since our minimum cell size is 2, all these passages will be "inter-basin doors" connecting basins to one another.  None of these passages will be "intra-basin" passages.  The status report verifies that each of our 149 links was an inter-basin door.

Here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |               |           |       |
+   +---+---+---+   +   +---+---+   +---+   +   +---+---+   +
|           |   |   |               |       |   |       |   |
+---+   +---+   +   +---+---+---+---+   +   +   +   +---+   +
|           |                           |   |   |   |       |
+---+   +---+---+---+   +---+---+---+---+---+   +   +---+   +
|                       |               |               |   |
+   +---+---+---+---+---+   +---+---+   +   +---+---+   +   +
|               |       |       |       |       |   |       |
+   +---+   +---+   +   +   +   +---+   +   +   +   +---+---+
|       |   |       |   |   |   |   |   |   |   |           |
+   +   +---+   +   +   +---+   +   +   +   +   +   +---+   +
|   |   |       |   |           |       |   |   |   |       |
+   +   +---+---+---+   +---+---+---+---+---+   +   +---+---+
|   |       |   |                           |       |   |   |
+---+   +   +   +   +   +---+---+   +---+   +   +---+   +   +
|       |   |   |   |       |   |       |   |           |   |
+   +---+   +   +   +---+   +   +   +---+---+---+   +   +   +
|       |               |   |                   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 7 - unweighted tournament scheduling

The default (as of v0.10.9) is tournament scheduling with equally weighted tasks, or unweighted tournament scheduling.  This sort of scheduling uses the class *Tournament* found in module *mazes.tournament*.  The module is imported by the *Watershed* class, so we don't need to import the module directly.

We accordingly start with three of the four imports in Example 6:
We start with some imports:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.watershed_division import WatershedDivision
```

We create a maze object and run the *WatershedDivision* algorithm using only the maze object, the minimum cell threshold, and the number of pumps:
```
>>> maze = Maze(OblongGrid(10, 15))
>>> print(WatershedDivision.on(maze, 2, 3))
          Watershed Recursive Division (statistics)
                            visits      295
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        9
                       extra pumps        0
                  watershed errors        0

```
The key difference is that, instead of taking turns in sequence, a die is tossed and the number on the die determines which pump gets the next turn.  There is a very tiny chance that the first pump might actually get every turn, but in practice, the tasks will tend to get roughly the same number of turns in the long run.

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |                               |       |           |
+   +   +---+   +---+   +   +---+---+   +---+   +---+---+   +
|   |           |       |           |                       |
+---+---+---+---+   +---+---+   +   +---+---+---+   +---+---+
|           |               |   |       |   |           |   |
+---+   +---+   +   +---+---+---+---+---+   +---+   +---+   +
|       |       |   |                       |   |           |
+   +---+---+   +   +   +---+---+---+---+   +   +---+---+   +
|               |       |           |   |   |           |   |
+   +---+---+---+---+---+---+---+   +   +   +   +---+   +---+
|           |   |   |       |   |       |       |   |   |   |
+---+---+---+   +   +   +---+   +   +   +---+   +   +   +   +
|               |               |   |   |   |       |       |
+   +---+---+   +   +---+   +---+   +   +   +---+   +---+   +
|       |           |   |       |   |       |       |   |   |
+---+---+---+---+---+   +   +   +---+   +---+---+   +   +   +
|       |   |   |           |       |   |       |   |       |
+   +---+   +   +   +---+---+   +   +   +---+   +   +   +   +
|                           |   |                   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 8 - weighted tournament scheduling

By default, each task gets the same weight -- namely a weight of 1.  But we can give tasks larger weights.  One result will be that, at each stage, the pump whose weight is highest will tend to form the largest basin.

The imports are as in Example 7 since the *Tournament* class is used for scheduling.  The main difference is that we supply three weights, *i.e.* one weight per pump:
```
>>> maze = Maze(OblongGrid(10, 15))
>>> print(WatershedDivision.on(maze, 2, 3, targs=(5, 1, 1)))
          Watershed Recursive Division (statistics)
                            visits      324
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        9
                       extra pumps        0
                  watershed errors        0
```
In this example, pump 1 received a weight of 5, while pumps 2 and 3 received weights of 1.  The total weight is 7, so the scheduler chooses the task for pump 1 with probability 5/7 and the tasks for pumps 2 and 3 each with probability 1/7.  The result is that, for larger reservoirs, the basin for pump 1 will tend to be substantially larger than the other two basins.  The main consequence is likely an increase in average run time.  It is less clear how this might affect the resulting maze.
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |       |                                   |           |
+   +   +   +   +   +---+---+   +   +   +---+---+---+   +   +
|       |       |   |       |   |   |       |           |   |
+   +---+   +---+   +   +---+---+---+   +   +   +   +---+   +
|   |   |       |       |       |   |   |       |       |   |
+   +   +---+---+---+---+   +   +   +---+   +---+   +---+   +
|       |   |       |       |   |       |   |   |   |       |
+---+---+   +   +---+---+---+   +---+   +   +   +---+   +---+
|   |       |           |       |   |   |       |       |   |
+   +---+   +---+   +---+---+   +   +   +   +---+   +---+   +
|           |   |                           |   |           |
+---+   +---+   +---+---+   +---+---+---+   +   +   +---+---+
|   |                       |       |       |               |
+   +---+---+   +---+   +---+   +   +   +---+---+---+---+   +
|               |               |   |   |   |       |       |
+---+---+   +   +   +---+---+---+   +---+   +---+   +   +---+
|       |   |   |   |           |       |               |   |
+   +---+---+---+   +   +   +   +---+---+---+   +---+---+   +
|                       |   |       |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
