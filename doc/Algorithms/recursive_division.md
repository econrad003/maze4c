# Recursive Division

The basic rectangular grid version of the algorithm essentially divides a room into two smaller rooms and erects a wall with one door to separate the two rooms.  This division process continues until the rooms reach their minimum size.

The algorithm is probably more natural to envision as a wall builder, but it is actually slightly simpler to implement as a passage carver.  (Our implementation here is actually a passage carver.

## The Algorithm in Detail

Start with an empty m×n rectangular grid.  This is the initial subgrid.  In addition we have a stack.  The initial subgrid is pushed on the stack.  The algorithm terminates when the stack is empty.

```
While the stack is not empty:
    pop a subgrid from the stack;
    if it can be subdivided
        decide whether to subdivide vertically or horizontally;
        subdivide the grid into two subgrids and carve a connecting door
        push each subgrid onto the stack
```

Note that every link between two cells is actually a door connecting two subgrids.

## Example 1

Let's create a maze using the implementation of the algorithm.  We begin in the usual manner...

```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(10, 15))
>>> from mazes.Algorithms.recursive_division import RecursiveDivision
>>> print(RecursiveDivision.on(maze))
          Recursive Division (statistics)
                            visits      299
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        8
```

We started with 150 cells and ended with 149 links, as expected.  Notice that the number of doors is the same as the number of links, so each link is actually a door connecting two subgrids.  Now let's look at the maze:

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |                                   |       |
+   +   +   +   +---+---+---+---+---+---+   +---+---+---+   +
|   |   |       |               |               |   |   |   |
+   +---+---+---+   +---+---+---+   +   +   +   +   +   +   +
|       |   |               |   |   |   |   |   |   |       |
+   +   +   +   +   +   +   +   +---+   +---+---+   +---+   +
|   |           |   |   |           |           |   |       |
+---+---+   +---+---+---+   +---+   +---+---+   +   +   +   +
|           |   |   |           |   |   |   |   |   |   |   |
+   +   +   +   +   +---+   +   +   +   +   +   +   +---+   +
|   |   |       |   |   |   |   |   |           |   |       |
+   +   +---+   +   +   +   +   +   +---+   +   +   +   +---+
|   |       |   |           |   |           |   |   |       |
+---+---+   +---+---+   +---+---+---+---+---+---+   +---+   +
|   |   |   |   |           |       |       |   |       |   |
+   +   +   +   +   +   +   +   +---+---+   +   +   +   +   +
|               |   |   |                   |       |       |
+---+---+   +---+   +   +---+   +   +   +   +   +   +---+   +
|               |   |       |   |   |   |       |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

```

## Example 2

The maze has a boxlike structure somewhat akin to a room plan, but, since every cell is an individual room, this box structure might not be apparent.  We can  make it a bit more apparent by stopping the recursion a bit earlier.  We start with a new grid...

```
>>> maze = Maze(OblongGrid(10, 15))
>>> print(RecursiveDivision.on(maze, min_rows=4, min_cols=6, label_rooms=True))
          Recursive Division (statistics)
                            visits       39
                             cells      150
                          passages        0
                             links       19
                           unlinks        0
                             doors       19
                         max stack        6
```
The parameters here are:
```
        min_rows = 4
```
This tells us that subgrid with fewer than 4 rows cannot be subdivided vertically.  Similarly:
```
        min_cols = 6
```
tells us not to horizontally subdivide a grid with fewer than 6 columns.
Note that neither parameter prevents a subgrid from being smaller -- they are preconditions for subdivision, not postconditions.  Finally:
```
        label_rooms = True
```
is a debugging parameter which just tells us to assign a label to each subdivision.  The cell label is determined by the final subdivision.  There are only 52 labels (26 upper case Latin letters + 26 lower case), so labels may be recycled.

Now for the result:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| h | h | h | h | h   O | S | S | S | S | S | T   R | D | D |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| h | h | h | h | h | O   S | S | S | S | S   T | R | D | D |
+---+---+---+---+---+---+---+---+---+---+---+---+   +---+---+
| h | h | h | h | h | d | d | d | X | X | X | X | X | D | D |
+   +---+---+---+---+---+---+---+---+---+---+---+---+---+   +
| j | j | j | j | j | d | d | d | X | X | X | X | X | F | F |
+---+---+---+---+---+---+---+---+---+   +---+---+---+---+---+
| j | j | j | j | j | d | d | d | Z | Z | Z | Z | Z | F | F |
+---+---+   +---+---+---+   +---+---+---+---+---+---+---+---+
| l | l | l | l | l | c | c | c | Z | Z | Z | Z | Z | F | F |
+---+---+---+---+---+---+---+---+---+   +---+---+---+---+   +
| l | l | l | l | l | c | c | c | Y | Y | Y | Y | Y | H | H |
+---+---+---+---+   +---+---+   +---+---+---+---+---+---+---+
| k | k | k | k | k | a | a | a | Y | Y | Y | Y | Y   H | H |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| k | k | k | k | k | a | a | a   Y | Y | Y | Y | Y | H | H |
+---+---+---+---+---+---+---+---+   +---+---+---+---+   +---+
| k | k | k | k | k | e | e | e | e | e   f | f | f | G | G |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

There is a subgrid in the upper left covering 3 rows and 5 columns, each cell having the label h.  This is one room in the room plan.  Below it is a 2 row, 5 column room with label j.  If we link up the cells in each room, we can better see the room plan:

```
(manually clear rooms)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| h                   O | S                 | T   R | D     |
+                   +   +                   +   +   +       +
|                   |                           |   |       |
+                   +---+---+---+---+---+---+---+   +       +
|                   | d         | X                 |       |
+   +---+---+---+---+           +                   +---+   +
| j                 |           |                   | F     |
+                   +           +---+   +---+---+---+       +
|                   |           | Z                 |       |
+---+---+   +---+---+---+   +---+                   +       +
| l                 | c         |                   |       |
+                   +           +---+   +---+---+---+---+   +
|                   |           | Y                 | H     |
+---+---+---+---+   +---+---+   +                   +       +
| k                 | a         |                           |
+                   +           +                   +       +
|                   |                               |       |
+                   +---+---+---+   +---+---+---+---+   +---+
|                   | e                   f         | G     |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that each room in the plan has _at most_ two doors.  In the lower left, we see rooms k and l.  The door between the two was the result of subdividing a larger 5 by 5 cell room.  The door from room l to room j was the result of an earlier subdivision which created the room that was partitioned to form rooms k and l.


## Example 3 - Binary Recursive Division

By default, the subdividing process simply randomly selects a row or column to act as the end of the first subgrid.  For example, if our subgrid consists of a portion of rows 5 through 10, we can create a vertical subdivision by selecting any of rows 5 through 9 as the top row of the first subgrid.  If we select row 6, the first subgrid ranges from row 5 to row 6 and the second from row 7 to row 10.  Note that row 10 would not work as a divider since that would mean the second subgrid contained no cells.

We might want a more equal subdivision.  In the extreme case, we have binary recursive division - where we always choose the median.

```
>>> median = lambda x, y: (x+y) // 2
>>> maze = Maze(OblongGrid(10, 15))
>>> print(RecursiveDivision.on(maze, vertical_cutter=median, horizontal_cutter=median))
          Recursive Division (statistics)
                            visits      299
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        7
```

Again we see that our maze consists of 149 links, each a door from one room to another.  The boxy structure may be a little more evident than in the result of example 1.  Here is the maze.

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |   |           |       |   |   |       |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |       |       |   |   |   |           |   |       |
+---+---+---+   +   +---+---+---+---+   +---+---+---+   +---+
|       |       |       |                               |   |
+   +---+   +---+---+   +   +---+---+   +---+   +---+   +   +
|   |   |                       |   |   |   |   |   |       |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|           |   |   |   |   |   |       |       |       |   |
+---+---+---+---+   +---+---+---+   +---+---+---+---+---+---+
|           |   |   |       |   |       |       |           |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |       |       |       |   |       |   |   |   |   |
+---+   +---+---+---+---+---+   +   +---+---+---+---+   +---+
|       |       |               |       |       |           |
+   +---+   +---+   +---+   +---+---+   +   +---+   +---+   +
|   |           |       |   |   |   |   |           |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|       |   |       |   |       |           |   |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 4

In another extreme, suppose we always cut one row at a time...

```
>>> first = lambda x, y: x
>>> print(RecursiveDivision.on(maze, vertical_cutter=first, horizontal_cutter=first))
          Recursive Division (statistics)
                            visits      299
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack       24
```

Note that this required a much larger stack.  Taking the median as the divider each time minimized the stack usage.  Peeling off just one row or just one column at a time will require a significantly larger stack.

The resulting maze shares some similarities with a breadth-first search maze.  But there are also some very definite differences.
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |       |   |       |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |       |   |   |   |   |   |   |       |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +---+
|   |   |   |   |   |   |       |   |   |       |   |       |
+   +   +   +   +   +   +   +   +   +   +   +   +---+---+   +
|   |   |   |   |   |   |   |   |   |   |   |               |
+   +   +   +   +   +   +   +   +   +   +   +---+---+---+   +
|   |   |   |   |   |   |   |   |       |   |               |
+   +   +   +   +   +   +   +   +   +   +   +---+---+---+---+
|       |   |   |   |   |   |   |   |   |                   |
+   +   +   +   +   +   +   +   +   +---+---+   +---+---+---+
|   |       |   |   |   |   |       |                       |
+   +   +   +   +   +   +   +   +---+---+   +---+---+---+---+
|   |   |   |       |   |   |   |                           |
+   +   +   +   +   +   +   +---+---+   +---+---+---+---+---+
|   |   |   |   |       |   |                               |
+   +   +   +   +   +   +---+---+---+---+---+---+---+   +---+
|   |   |       |   |   |                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Implementation Notes and Possible Next Steps

Much of the work is delegated to a class Subgrid defined in the *recursive\_division* module.  That module can be subclassed to allow greater control over the partitioning process.  At this writing, I haven't carried out that program with any examples.  But here are some possibilities:

1. Subdividing the rectangular grid using its ring structure instead of its blocked structure...
2. Recursive division in other grids, such as the polar (or theta) grid...
3. A more general recursive division algorithm, perhaps largely independent of grid topology.