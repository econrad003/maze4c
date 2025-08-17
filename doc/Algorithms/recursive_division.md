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

## On the examples

The examples go into some detail on programming recursive division.  There is a demonstration module (*demos.recursive_division*) which supports some of the available options, which can also produce graphics and image output.  For help, run it with the help option:

```
    maze4c$ python -m demos.recursive_division -h
```

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
(manually clear rooms - to automate, see Examples 5 and 6.)
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

## Example 5.  Room plans.

In the Jamis Buck maze book, the recursive division algorithm is implemented as a wall builder.  This makes it convenient for producing random room plans, as when the recursion stops, no additional walls are erected.  In our passage carver version, to produce a room plan, we must carve additional passages to produce a room plan.  When the examples above were created, that feature had not yet been implemented.  A *carve_rooms* option is now available.  In this example, we proceed programmatically.  To recap, we start by bringing up the Python interpreter and importing a few classes:

```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.recursive_division import RecursiveDivision
```

Now all we need to do is create a rectangular grid, embed it in a Maze wrapper, and run *RecursiveDivision.on* with some suitable options.  We can combine the first two steps in a single statement:

```
>>> maze = Maze(OblongGrid(10, 15))
```

Next we must decide where we want to stop subdividing.  We will block vertical subdivisions when we arrive at a subgrid with fewer than 4 rows.  Similarly, horizontal subdivisions will be blocked when there are fewer than 6 columns.
As above, we will label the rooms.
```
>>> print(RecursiveDivision.on(maze, min_rows=4, min_cols=6,
...     carve_rooms=True, label_rooms=True))
          Recursive Division (statistics)
                            visits       45
                             cells      150
                          passages        0
                             links      201
                           unlinks        0
                             doors       22
                         max stack        6
                             rooms       23
                        room links      179
```
Notice the status is more complicated.  As there are 23 rooms in the final maze, we expect that there will be 22 doors that connect them.  Most of the passages (links) are interior to rooms, but a simple subtraction yields:
```
        links - room links = 201 - 179 = 22
```

Here is the maze, with rooms labelled:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| n   n   n   d   d   d   d   d | R   R   R   R   R | J   J |
+   +   +   +---+---+---+   +---+   +   +   +   +   +---+   +
| n   n   n | h   h   h   h   h | R   R   R   R   R | L   L |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +---+
| n   n   n | h   h   h   h   h   R   R   R   R   R   N   N |
+---+---+   +---+---+---+   +---+---+---+   +---+---+---+   +
| r   r   r | g   g   g   g   g | Q   Q   Q   Q   Q | M   M |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
| r   r   r | g   g   g   g   g | Q   Q   Q   Q   Q | M   M |
+   +   +   +   +---+---+---+---+---+---+---+---+   +   +   +
| r   r   r | j   j   j   j   j | O   O   O   O   O | M   M |
+   +---+---+   +   +   +   +   +   +---+---+---+---+---+---+
| q   q   q | j   j   j   j   j | b   b   b | Z   Z   Z   V |
+   +---+---+---+---+   +---+---+   +   +   +   +---+---+   +
| o   o   o | i   i   i   i   i | b   b   b   Y   Y   Y | V |
+   +---+---+   +   +   +   +   +   +---+---+   +   +   +   +
| k   k   k | i   i   i   i   i | a   a   a | Y   Y   Y | V |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
| k   k   k | i   i   i   i   i | a   a   a | Y   Y   Y | U |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 6.  Room plans, again

In this example, we use the demonstration program to create another room plan with the same constraints as in Example 5, but with no room labels.  The result is displayed below and has been saved in the gallery.  The demonstration module does support room labels, but only on the console display.  The graphics display and the PNG image are less cluttered as the "poles" that appear in the console display are not present on the graphics image.

The gallery image is *gallery/recursive_division.png*.

```
maze4c$ python -m demos.recursive_division -m 4 6 --rooms \
    -o gallery/recursive_division.png
Namespace(dim=(8, 13), minimums=(4, 6), rooms=True, labels=False, pen='black', output='gallery/recursive_division.png', console=False, verbose=False, no_gui=False)
          Recursive Division (statistics)
                            visits       33
                             cells      104
                          passages        0
                             links      139
                           unlinks        0
                             doors       16
                         max stack        4
                             rooms       17
                        room links      123
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |           |               |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|               |                                   |
+   +   +   +   +   +---+   +   +   +   +   +   +   +
|                       |           |               |
+---+---+---+   +   +   +---+---+---+---+---+---+   +
|               |       |               |       |   |
+---+---+---+   +   +   +   +   +   +   +   +   +   +
|               |       |               |       |   |
+---+---+   +---+---+---+   +   +   +   +   +   +   +
|                   |   |               |       |   |
+   +   +   +   +   +   +---+   +---+---+---+   +   +
|                   |   |               |       |   |
+   +   +   +   +   +   +---+---+   +---+   +   +   +
|                       |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
Saving to gallery/recursive_division.png
```


## Implementation Notes and Possible Next Steps

Much of the work is delegated to a class Subgrid defined in the *recursive\_division* module.  That module can be subclassed to allow greater control over the partitioning process.  At this writing, I haven't carried out that program with any examples.  But here are some possibilities:

1. Subdividing the rectangular grid using its ring structure instead of its blocked structure...
2. Recursive division in other grids, such as the polar (or theta) grid...
3. A more general recursive division algorithm, perhaps largely independent of grid topology.