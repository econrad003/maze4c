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

## Example 2 - Simple variations

The implementation allows for a considerable range of reconfiguration.  These will be discussed at some length here.

### Merging in rows (flip1)

This corresponds to the bias parameter in the basic implementations of simple binary tree and sidewinder.  The default is a simple head/tail coin toss.  The head (True) carves forward and the tail (False) does not carve.

In the implementation of Eller's algorithm, the option is *flip1*, and by default it maps to a triple:

```
        flip1 = (coin_toss, (), {"bias":0.5})
```
The method *coin\_toss* is defined in module *mazes.Algorithms.eller*.  It ignores all of its arguments except the bias option.  The bias option is the probability of a head.  The default value (0.5) corresponds roughly to the behavior of a fair coin.

In practice, the triple is used as follows:

```
     OPTION
        flip1 = (foo, (arg1, arg2, ...), {"option1":value1, ...})

     USED AS
        head = foo(cell, cell.west, arg1, arg2, ..., option1=value1, ...)
```
The first two arguments are the cell and its predecessor in the row and the decision is whether to join them by carving a passage (head) or to retain the wall that separates them (tail).

For our example, we will increase the probability of a leftward merge to 65%.

### Required carve up (required\_choice)

In sidewinder, in each run, there is one cell with a passage carved upward.  In Eller's algorithm, instead of runs, we consider components.  From each component, we carve *at least one* upward.  The option *required\_choice* makes the decision for the mandatory first choice.

```
        required_choice = (select_pair, (), {})
```

The default selection function (method *select\_pair* defined in module *mazes.Algorithms.eller*) simply makes a unformly random choice from the
run that it is given.  It ignores any other arguments.  A custom choice function (*e.g* *foobar*) is declared in the same way that a custom flip function is declared:

```
     OPTION
        required_choice  = (foobar, (arg1, ...), {"option1":value1, ...})

     USED AS
        item = foo(items, arg1, ..., option1=value1, ...)
```

In this case, *items* is a *list* of *(cell, nbr)* pairs where *cell* is in the current row and *nbr* is a neighboring cell in the following row.  The result is one of the ordered pairs in the list.

For this example, our choice function will always return the first item.

### Optional carve up (flip2)

This option has no analogue in sidewinder of the simple binary tree.  The default is a simple unfair head/tail coin toss.  The head (True) carves upward and the tail (False) does not carve.  The toss occurs for every cell in the row where we can but haven't already carved upward.  The option is *flip2*, and by default it maps to a triple:

```
        flip2 = (coin_toss, (), {"bias":1/3})
```
The method *coin\_toss* was described above. The default value (1/3) corresponds roughly to the behavior of a cubic die where a toss of 1 or 6
is treated as a head and 2, 3, 4, or 5 as a tail.

To define a custom toss, the syntax and semantics are essentially the same as for flip1:

```
     OPTION
        flip2 = (bar, (arg1, arg2, ...), {"option1":value1, ...})

     USED AS
        head = bar(cell, cell.north, arg1, arg2, ..., option1=value1, ...)
```
The first two arguments *cell* and *cell.north* are respectively a cell in the current row and one of its neighbors in the succeeding row.  For rows and columns in the usual rectangular grid, this will be uniquely determined.  (In Example 3, we consider a variant where some cells may have more than one neighbor in the next "row".)

For this example, our flip function will return True if the given cell is in an odd column.

### Rows and columns

We can change direction in a row or column, or we can use a column-major approach instead of a row-major approach. If we hang a typical Mercator projection map of the world, we typically hang it with the north pole up and Asia (east) to the right.  We could easily hang it with the north pole to the left and Asia up.  (This is a 90-degree counterclockwise rotation.)  Or we could rotate 180 degrees or 270 degrees.   Suppose there is a map on the back with the same north edge on both sides.  If we hang the map with the back side facing us and north up, then Asia (on the front) is now on the left side.  This is one of four "reflections".  There are a total of eight orientations using the the four rotations and the four reflections.

To specify which of tje orientations we want, we can specify an onward direction (four possibilities) and an upward direction (two possibilities, perpendicular to the chosen onward direction.)

Since the default is *onward="east"* and *upward="north"*, this example will use *onward="south"* and *upward="west".  We proceed as usual by first creating an empty maze:

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
```

Next we import the algorithm class (*Eller*) from the *eller* module.  We will need *coin\_toss* for the first flip, so we import that as well:

```
    4> from mazes.Algorithms.eller import Eller, coin_toss
```

We need a choice function and a flip-flop function, so we create those on the fly:

```
    5> def choice(run:list, *args, **kwargs):
    ...     return run[0]
    ...
    6> def flip(cell1, cell2, *args, **kwargs):
    ...     return cell1.index[1] % 2 == 1
    ...
```

We are ready.  Note carefully the form of each argument:
```
    7> print(Eller.on(maze, onward="south", upward="west",
    ...   flip1=(coin_toss, (), {"bias":0.65}),
    ...   required_choice=(choice, (), {}),
    ...   flip2=(flip, (), {})))
          Martin Eller's Spanning Tree (statistics)
                            visits       13
                             cells      104
                          passages      103
               optional merge left       43
               required merge left        1
             required carve upward       26
             optional carve upward       33
                            onward  south
                            upward  west
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |       |               |                   |
    +---+   +---+   +---+   +---+   +---+   +---+   +   +
    |       |       |       |               |       |   |
    +---+   +---+   +---+   +---+   +---+   +   +---+   +
    |       |       |       |       |       |       |   |
    +---+   +---+   +---+   +---+   +---+   +---+   +   +
    |       |       |       |       |       |       |   |
    +   +---+   +---+---+   +---+   +---+---+---+   +---+
    |       |               |       |       |           |
    +---+   +---+   +---+   +---+---+   +---+---+   +---+
    |       |       |       |       |       |           |
    +---+   +---+   +---+   +---+   +   +---+---+   +   +
    |       |       |       |               |       |   |
    +---+   +---+   +   +---+---+   +---+   +   +---+---+
    |               |               |       |           |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Let's take a close look at the statistics.  First, our maze has 104 cells and 103 passages. As it seems to be connected and the number of passages is exactly one less than the number of cells, it is a tree.  Our last "row" was actually the westmost column.  The required "merge left" (actually: merge up) must have occurred in row 3 column 0.  It was required because, if there were a wall between that cell and the cell in row 4 column 0, then the cells in rows 4 through 7 columns 0 and 1 would be walled off from the rest of the maze.  Adding the merges and carves, we have the total number of passages:

```
            43 + 1 + 26 + 33 = 103.
```

The almost regular structure of the maze is due to the fact that optionally carving west ("upward") depended only on the column.  In columns 1, 3, 5, 7, 9 and 11, we always carve a passage from a cell to its westward neighbor.  In columns 2, 4, 6, 8, 10 and 12, the only westward passages were the ones that were required to maintain connectivity.  For the even columns, there was some *apparent* randomness in the choice of the mandatory westward passages.  This is governed by the way the components are managed.  To eliminate this apparent randomness, our choice function would need to return a "least element" from the list of (cell, cell.west) pairs instead of the first pair in the list.

## Example 3 - Outward Eller

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

Note the cell in row 1 column 1.  It is a corner in the third ring from the center.  It has two outward neighbors, namely the two neighbors of the cell in
the southwest corner.  Outward passages were carved in both directions from this cell.  (This situation occurs working outward in rings but not when working in rows or in columns.

The *OutwardEller.Status* class is built as a subclass of the *Eller.Status* class.  The changes to made to handle rings all take place during argument parsing, initialization and configuration.  The code to handle the carving decisions amd maze carving remains entirely in the parent class.