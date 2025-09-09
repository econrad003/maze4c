# Console Tools

This module provides additional methods for working on the console instead of using graphical methods.

The following methods have been implemented:

* *unicode\_str* - alternate display of rectangular mazes using Unicode block characters.

## 1 - Method *unicode\_str*

### Usage

```
maze4c$ python
Python 3.10.12
>>> help(mazes.console_tools.unicode_str)
Help on function unicode_str in module mazes.console_tools:

unicode_str(maze: (Maze, Grid), **kwargs)
    produce a string representation of a rectangular maze

    POSITIONAL ARGUMENTS

        grid - a rectangular maze or grid instance

    KEYWORD ARGUMENTS

        s, e, n, w, h, v - boundary label arguments (default: None)
            The choices are:
                "A" - alphabetic labels
                "N" - numeric digit labels
                "RA" - reverse alphabetic labels
                "RN" - reverse numeric digit labels
            "RA" can be abbreviated to "R".

            Numeric digit labels run from "0" to "9".  If more than
            ten rows or columns are to receive a label, labelling
            continues with characters that follow "9".

            Alphabetic digit labels run from "A" to "Z".  If more than
            twenty-six rows or columns are to receive a label,
            labelling continues with characters that follow "Z".

            The default value (None) indicates that no labels are to
            be supplied in the indicated direction.  The lower case
            compass directions (s, e, n, w) indicate which boundaries
            are to be labelled.  The directional options h and v (for
            horizontal and vertical) can be used in lieu of pairs of
            compass directions -- h for e and w, or v for n and s.

            Labels normally run from left to right (i.e. west to east)
            and from bottom to top (south to north).

            The label options are all a single lower case letter.  The
            horizontal and the vertical options, when set, override
            any compass direction settings.

    EXAMPLES

            For a normal rectangular grid, labels are not needed:

                print(unicode_str(maze))

            For a cylindrical grid, where the east and west edges meet
            with no twist, we might label the joined edges from the
            south row upward numerically as follows:

                print(unicode_str(maze, v="N"))

            or from the north row downward:

                print(unicode_str(maze, v="NR"))

            If there are more than 10 rows, alphabetic labels might be
            preferable: 

                print(unicode_str(maze, v="A"))

            For a Moebius strip, where the east and west edges meet with
            a half twist, we would prefer labels to go in the opposite
            directions, for example:

                print(unicode_str(maze, w="NR", e="N"))
```

### Example 1.1 - Basic rectangular grid

As noted, in a normal rectangular maze, *i.e.* a maze with no passages that pass through the sides of the rectangle, labels along the boundary are not generally needed.  In this example we carve a rectangular maze and display the result, first using the maze's *str* magic method, then using the *unicode\_tools* method.

First we carve the maze in the typical way:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.sidewinder import Sidewinder
>>> maze = Maze(OblongGrid(10, 15))
>>> print(Sidewinder.on(maze))
          Sidewinder Tree (statistics)
                            visits      151
                             cells      150
                          passages      149
                            onward  east
                            upward  north
                              bias        0.5000
```

Here is what the maze looks like using basic ASCII characters:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                           |
+   +   +---+   +---+---+---+---+   +---+---+---+   +   +---+
|   |   |       |                           |       |       |
+---+---+---+   +   +   +---+   +---+   +   +   +---+   +---+
|               |   |       |   |       |   |   |           |
+---+---+---+   +---+---+---+   +---+---+   +   +---+   +   +
|                   |           |           |   |       |   |
+---+---+   +   +---+---+   +---+   +---+   +   +---+   +   +
|           |   |               |       |   |   |       |   |
+   +---+   +   +   +   +---+   +   +   +   +   +   +   +   +
|   |       |   |   |   |       |   |   |   |   |   |   |   |
+   +   +---+---+   +   +---+   +   +   +   +---+   +   +   +
|   |       |       |       |   |   |   |   |       |   |   |
+   +   +   +---+---+---+---+---+   +   +   +   +   +   +   +
|   |   |   |                       |   |   |   |   |   |   |
+   +---+   +   +---+   +---+   +---+---+   +   +---+   +---+
|       |   |   |       |               |   |       |       |
+---+---+   +   +---+   +   +   +---+---+---+   +   +---+   +
|           |   |       |   |               |   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

And here is the result using Unicode block characters:
```
>>> from mazes.console_tools import unicode_str
>>> print(unicode_str(maze))
┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃                                                           ┃
┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
┃   ┃   ┃       ┃                           ┃       ┃       ┃
┣━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━┫
┃               ┃   ┃       ┃   ┃       ┃   ┃   ┃           ┃
┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
┃                   ┃           ┃           ┃   ┃       ┃   ┃
┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ┫
┃           ┃   ┃               ┃       ┃   ┃   ┃       ┃   ┃
┣   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
┃   ┃       ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
┣   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ┫
┃   ┃       ┃       ┃       ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃
┣   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
┃   ┃   ┃   ┃                       ┃   ┃   ┃   ┃   ┃   ┃   ┃
┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
┃       ┃   ┃   ┃       ┃               ┃   ┃       ┃       ┃
┣━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ┫
┃           ┃   ┃       ┃   ┃               ┃   ┃   ┃       ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

### Example 1.2 - Diagonal connections (with programming details)

Limited support is provided for diagonal connections.  We will *carefully* add four diagonal passages to illustrate their use.  To do this properly, we will need need to add "southeast", "northeast", "northwest", and "southwest" grid connections, as these are not provided in grid class *OblongGrid*.  And, of course, we will need link the cells.  We start from two neighboring cells, which we label:

```
>>> cell = maze.grid[5,5]
>>> cell2 = cell.west
>>> cell.label = '1'
>>> cell2.label = '2'
```

Next we make the diagonal grid connections.  (This would normally be handled automatically by a more appropriate grid object.  In any case, this is effectively how it can done.)  The *unicode\_str* method assumes that the passages are undirected, so we must not forget that the grid connections must also be reversed:

```
>>> cell["northeast"] = cell.north.east
>>> cell["northeast"]["southwest"] = cell
>>> cell["northwest"] = cell.north.west
>>> cell["northwest"]["southeast"] = cell
```

We make the same four grid connections for *cell2*:

```
>>> cell2["northeast"] = cell2.north.east
>>> cell2["northeast"]["southwest"] = cell2
>>> cell2["northwest"] = cell2.north.west
>>> cell2["northwest"]["southeast"] = cell2
```

Now we are ready to link the two cells to their diagonal neighbors in the row above:
```
>>> maze.link(cell, cell["northeast"])
>>> maze.link(cell, cell["northwest"])
>>> maze.link(cell2, cell2["northeast"])
>>> maze.link(cell2, cell2["northwest"])
```

The diagonal connections are marked with either a slash (for a southwest-northeast passage), a backslash (for a southeast-northwest passage), or a capital X in the event tha both types of passages cross.  In this example, we have a pair of diagonal passage that cross, and one of each type with no crossing.  The result isn't pretty, but (we hope) it is useful.  And here is the result:
```
>>> print(unicode_str(maze))
┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃                                                           ┃
┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
┃   ┃   ┃       ┃                           ┃       ┃       ┃
┣━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━┫
┃               ┃   ┃       ┃   ┃       ┃   ┃   ┃           ┃
┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
┃                   ┃           ┃           ┃   ┃       ┃   ┃
┣━━━╋━━━╋   ╋   \━━━X━━━/   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ┫
┃           ┃   ┃ 2   1         ┃       ┃   ┃   ┃       ┃   ┃
┣   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
┃   ┃       ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
┣   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ┫
┃   ┃       ┃       ┃       ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃
┣   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
┃   ┃   ┃   ┃                       ┃   ┃   ┃   ┃   ┃   ┃   ┃
┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
┃       ┃   ┃   ┃       ┃               ┃   ┃       ┃       ┃
┣━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ┫
┃           ┃   ┃       ┃   ┃               ┃   ┃   ┃       ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

### Example 1.3 - Cylindrical maze (E/W)

First we create a cylindrical maze with 10 rows and 15 columns:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.cylinder import CylinderGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> maze = Maze(CylinderGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1434
                             cells      150
                          passages      149
                     starting cell  (0, 7)
```

Since the leftmost and rightmost columns are joined, it is helpful to label the west and east rows.  Since the join is without a twist, the labels should be the same and in the same order.  In this particular example the ends of row 2 are joined by a passage.  We will also label these two cells as "s" and "t":
```
>>> from mazes.console_tools import unicode_str
>>> cell = maze.grid[2,0]
>>> cell.label = "s"
>>> cell.west.label = "t"
>>> print(unicode_str(maze, h="N"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9 ┃           ┃       ┃   ┃   ┃       ┃       ┃   ┃   ┃       ┃ 9
    ┣━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  8         ┃                       ┃       ┃   ┃           ┃     8
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
  7             ┃       ┃       ┃       ┃       ┃                 7
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  6 ┃       ┃                       ┃               ┃   ┃       ┃ 6
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ┫
  5 ┃   ┃               ┃           ┃       ┃       ┃   ┃   ┃   ┃ 5
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  4 ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃           ┃   ┃   ┃       ┃ 4
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━┫
  3 ┃       ┃   ┃   ┃   ┃       ┃   ┃   ┃           ┃           ┃ 3
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  2   s         ┃               ┃           ┃   ┃   ┃         t   2
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━┫
  1             ┃                   ┃   ┃   ┃       ┃       ┃     1
    ┣   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  0 ┃   ┃       ┃       ┃   ┃           ┃       ┃       ┃       ┃ 0
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

### Example 1.4 - Cylindrical maze (N/S)

First we create a cylindrical maze with 10 rows and 15 columns.  To orient the cylinder vertically, we set the parity to True:
```
>>> maze = Maze(CylinderGrid(10, 15, parity=True))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1648
                             cells      150
                          passages      149
                     starting cell  (2, 4)
```

There are more than 10 columns, so alphabetic labels are preferable.  Note that there are north/south boundary connections in columns B, E, I and N:
```
>>> print(unicode_str(maze, v="A"))
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
┏━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┳━━━┳━━━┳   ┳━━━┓
┃               ┃   ┃   ┃                                   ┃
┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
┃       ┃           ┃       ┃       ┃       ┃   ┃       ┃   ┃
┣━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ┫
┃       ┃   ┃               ┃   ┃   ┃               ┃       ┃
┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ┫
┃   ┃   ┃       ┃   ┃   ┃       ┃       ┃           ┃       ┃
┣   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
┃   ┃   ┃   ┃               ┃   ┃           ┃   ┃       ┃   ┃
┣   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
┃   ┃               ┃   ┃   ┃       ┃           ┃   ┃       ┃
┣   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ┫
┃       ┃   ┃   ┃           ┃       ┃           ┃       ┃   ┃
┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
┃   ┃           ┃       ┃       ┃   ┃       ┃   ┃       ┃   ┃
┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━┫
┃           ┃       ┃       ┃       ┃       ┃               ┃
┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ┫
┃   ┃               ┃           ┃               ┃           ┃
┗━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻━━━┻   ┻━━━┛
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

### Example 1.5 - Möbius strip maze (E/W)

A Möbius strip maze is like a cylindrical maze except the strip is given a half twist before the ends are joined.  In this case we reverse the labels on one end of the strip:
```
>>> from mazes.Grids.moebius import MoebiusGrid
>>> maze = Maze(MoebiusGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     2082
                             cells      150
                          passages      149
                     starting cell  (9, 6)    
>>> print(unicode_str(maze, w="N", e="NR"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9         ┃           ┃   ┃   ┃               ┃                 0
    ┣   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━┫
  8     ┃   ┃   ┃           ┃       ┃   ┃           ┃       ┃ y   1
    ┣━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
  7     ┃   ┃   ┃       ┃               ┃   ┃   ┃   ┃       ┃   ┃ 2
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━┫
  6 ┃   ┃   ┃       ┃       ┃               ┃       ┃   ┃         3
    ┣   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ┫
  5     ┃   ┃   ┃   ┃       ┃       ┃   ┃   ┃   ┃   ┃       ┃     4
    ┣━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━┫
  4             ┃   ┃   ┃       ┃   ┃                             5
    ┣━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ┫
  3     ┃   ┃   ┃   ┃       ┃   ┃               ┃   ┃   ┃   ┃   ┃ 6
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ┫
  2 ┃       ┃           ┃   ┃       ┃   ┃   ┃       ┃   ┃         7
    ┣   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ┫
  1   x ┃       ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃       ┃     8
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  0     ┃           ┃           ┃       ┃                   ┃     9
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Note here the passages associated with the row labels 0, 1, 3, 4, 5, 7, 8 and 9.  For example, moving west from cell (1,0), marked here as "x", one arrives by passage in cell (8, 14), marked here as "y".

(NOTE: the bottom row is row 0 and the leftmost column is column 0.  Coordinates are (row, column).)

### Example 1.6 - Möbius strip maze (N/S)

Since there are more than 10 columns, alphabetic labels are preferable. Only the first and last characters of the label string are inspected, any first character except "N" yields alphabetic labels and any last character except "R" does not reverse the order of the labels.  For that reason, "R" and "AR" are synonymous.  We will label the north row in reverse order:
```
>>> maze = Maze(MoebiusGrid(10, 15, parity=True))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1878
                             cells      150
                          passages      149
                     starting cell  (5, 6)
>>> print(unicode_str(maze, n="R", e="A"))
>>> print(unicode_str(maze, n="R", s="A"))
  O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
┏━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┓
┃           ┃       ┃               ┃     y ┃       ┃       ┃
┣━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
┃       ┃   ┃       ┃   ┃       ┃   ┃               ┃   ┃   ┃
┣━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ┫
┃           ┃       ┃   ┃   ┃   ┃   ┃   ┃       ┃       ┃   ┃
┣━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ┫
┃       ┃   ┃   ┃   ┃   ┃       ┃               ┃           ┃
┣   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ┫
┃   ┃   ┃           ┃       ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃
┣━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
┃               ┃       ┃   ┃           ┃           ┃       ┃
┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
┃       ┃       ┃   ┃       ┃   ┃           ┃   ┃   ┃       ┃
┣   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
┃       ┃               ┃           ┃   ┃       ┃   ┃   ┃   ┃
┣━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ┫
┃       ┃   ┃       ┃   ┃   ┃           ┃   ┃       ┃   ┃   ┃
┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ┫
┃           ┃     x             ┃       ┃       ┃       ┃   ┃
┗━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┛
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

Note here the passages associated with the column labels B, E, I, K and N.  For example, moving south from cell (0, 4), marked here as "x", one arrives by passage in cell (9, 10), marked here as "y".

### Example 1.7 - Toroidal grid

For a toroidal grid, the *unicode\_str* method is built into the class string magic method by default.  See the setter method for "fmt" for options.  The default format "N" labels rows numerically (as console limits make more than ten rows impractical, and labels columns alphabetically.  We give one example -- using the default format:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.torus import TorusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> maze = Maze(TorusGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1005
                             cells      150
                          passages      149
                     starting cell  (2, 7)
>>> print(maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏   ┳   ┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┓
  9     ┃   ┃           ┃       ┃       ┃       ┃           ┃     9
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  8             ┃       ┃           ┃       ┃   ┃   ┃       ┃     8
    ┣━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
  7 ┃           ┃       ┃   ┃       ┃   ┃               ┃       ┃ 7
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  6                 ┃           ┃       ┃       ┃   ┃   ┃   ┃     6
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  5 ┃       ┃           ┃   ┃   ┃   ┃   ┃   ┃               ┃   ┃ 5
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ┫
  4 ┃       ┃   ┃       ┃   ┃   ┃           ┃       ┃           ┃ 4
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ┫
  3             ┃   ┃               ┃   ┃   ┃   ┃   ┃             3
    ┣   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  2 ┃       ┃   ┃       ┃           ┃                   ┃   ┃   ┃ 2
    ┣   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  1 ┃   ┃       ┃   ┃           ┃   ┃           ┃       ┃   ┃   ┃ 1
    ┣━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ┫
  0         ┃   ┃   ┃       ┃           ┃   ┃       ┃             0
    ┗   ┻   ┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```
Note that the labels are the same north and south, also also east and west, as the sides are joined without twisting.

### Example 1.8 - Klein bottle grid (E/W)

With a Klein bottle, one pair of edges is joined in the opposite sense (as in a Moebius strip), while the other is joined in the same send.  As with the torus, a format can be used to insure that labels are properly oriented.  The default is numeric labels for the rows and alphabetic labels for the columns.

```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.klein import KleinGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> maze = Maze(KleinGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1631
                             cells      150
                          passages      149
                     starting cell  (3, 13)
>>> print(maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    ┏━━━┳━━━┳   ┳   ┳━━━┳━━━┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳   ┳━━━┳   ┓
  9     ┃   ┃   ┃                       ┃           ┃       ┃   ┃ 0
    ┣   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
  8 ┃       ┃   ┃   ┃   ┃   ┃       ┃   ┃       ┃   ┃   ┃         1
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  7         ┃   ┃       ┃       ┃       ┃   ┃               ┃   ┃ 2
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  6 ┃   ┃   ┃   ┃           ┃   ┃   ┃               ┃       ┃     3
    ┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ┫
  5     ┃           ┃   ┃       ┃   ┃       ┃       ┃   ┃         4
    ┣━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ┫
  4         ┃                   ┃           ┃   ┃   ┃             5
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  3     ┃   ┃   ┃   ┃       ┃       ┃   ┃   ┃           ┃       ┃ 6
    ┣   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  2 ┃   ┃       ┃           ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃     7
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  1                     ┃   ┃       ┃   ┃       ┃   ┃           ┃ 8
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  0 ┃       ┃       ┃       ┃       ┃           ┃                 9
    ┗━━━┻━━━┻   ┻   ┻━━━┻━━━┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻   ┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

### Example 1.9 - Klein bottle grid (N/S)

For a Klein bottle grid with top and bottom joined in the opposite sense, it is the the column labels that are oppositely sensed:
```
>>> maze = Maze(KleinGrid(10, 15, parity=True))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1817
                             cells      150
                          passages      149
                     starting cell  (4, 4)
>>> print(maze)
      O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏━━━┳━━━┳   ┳   ┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳   ┳   ┓
  9 ┃   ┃       ┃   ┃           ┃       ┃   ┃   ┃   ┃       ┃   ┃ 9
    ┣   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋   ┫
  8         ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃         8
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━┫
  7     ┃   ┃           ┃       ┃                   ┃       ┃     7
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━┫
  6 ┃       ┃           ┃               ┃   ┃       ┃       ┃   ┃ 6
    ┣   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ┫
  5     ┃                       ┃           ┃           ┃         5
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ┫
  4     ┃   ┃               ┃   ┃       ┃   ┃   ┃   ┃             4
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ┫
  3         ┃       ┃       ┃       ┃           ┃   ┃   ┃   ┃     3
    ┣━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━┫
  2 ┃   ┃           ┃   ┃   ┃   ┃       ┃   ┃   ┃           ┃   ┃ 2
    ┣   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  1     ┃   ┃               ┃       ┃                       ┃     1
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ┫
  0 ┃   ┃   ┃   ┃       ┃       ┃   ┃   ┃           ┃           ┃ 0
    ┗   ┻   ┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻   ┻   ┻━━━┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

### Example 1.10 - Real projective plane grid

For a real projective plane implemented on a rectangular grid, both pairs of opposite sides are joined in the opposite sense.  The inner workings are essentially the same as the twists in the Klein bottle or the Moebius strip.  The topology differs (of course!).
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.projective import ProjectiveGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> maze = Maze(ProjectiveGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1067
                             cells      150
                          passages      149
                     starting cell  (0, 2)
>>> print(maze)
      O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
    ┏   ┳   ┳━━━┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┳   ┳   ┳   ┳━━━┳   ┳━━━┓
  9     ┃   ┃       ┃       ┃       ┃       ┃           ┃       ┃ 0
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
  8         ┃       ┃           ┃   ┃           ┃                 1
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  7         ┃               ┃   ┃       ┃   ┃           ┃       ┃ 2
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
  6 ┃       ┃               ┃           ┃   ┃       ┃   ┃         3
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  5             ┃       ┃   ┃               ┃                     4
    ┣   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
  4     ┃   ┃           ┃       ┃       ┃   ┃               ┃     5
    ┣━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ┫
  3     ┃       ┃   ┃   ┃       ┃   ┃   ┃   ┃           ┃       ┃ 6
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  2 ┃       ┃           ┃   ┃           ┃       ┃       ┃   ┃     7
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
  1     ┃   ┃           ┃       ┃   ┃   ┃   ┃           ┃         8
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ┫
  0 ┃               ┃                                   ┃   ┃     9
    ┗━━━┻   ┻━━━┻   ┻   ┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻━━━┻   ┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```