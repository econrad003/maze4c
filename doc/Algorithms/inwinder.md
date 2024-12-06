# Inwinder

## Background

Inwinder is really just sidewinder with a small twist.  Sidewinder works in rows and columns, but inwinder works in rings.  There are a couple of *gotchas*, but inwinder just looks at the grid in a different way.

In the section on polar grids, there is an exercise:

> *Growing a Circular Binary Tree*: Yes, Binary Tree (and Sidewinder, too) can work on a circular maze! You get a rather mesmerizing pinwheel effect, actually...

> See: Jamis Buck, *Mazes for Programmers*, 2015 (Pragmatic Bookshelf), *p* 111.

(It's a wonderful book!)

In 2019, I wrote a Python 2 program to implement sidewinder on a polar grid.  As I was implementing this 2024 rewrite, I realized that this same sort of "pinwheel" effect could also be achieved on an ordinary rectangular grid.

## Grid organization

Here is how the grid is organized for inwinder:

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.Grids.oblong_rings import ConcentricOblongs
    3> grid = OblongGrid(8, 13)
    4> rings = ConcentricOblongs(grid)
    5> for cell in grid:
    ...     cell.label = rings.tier_for(cell)
    ...
    6> print(grid)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
> (By the way, "Oblong" is another name for "rectangle".  "Oblong" works as both a noun and an adjective, whereas the adjective form of "rectangle" is "rectangular" which is cumbersome to type.  "Square" likewise works as both as both a noun and an adjective, but I prefer to reserve "square" for rectangles with equal sides.)

The outermost ring is ring 0.  The ring number of the innermost ring as well as its shape depends on the numbers of rows and columns in the maze.  In the example above the innermost tier, ring 3, is a 2x7 rectangle.  Here is a breakdown how the innermost tier appears.  Let *m* and *n* be the numbers of rows and columns in the grid.  Then:

* *m=n*, both odd: the innermost ring will be a single cell
* *m=n*, both even: the innermost ring will be a 2x2 square
* *m<n*, *m* odd: the innermost ring will have a single row and *n-m+2* columns
* *m<n*, *m* even: the innermost ring will have a 2 rows and *n-m+2* columns
* *m>n*, *n* odd: the innermost ring will have a single column and *n-m+2* rows
* *m>n*, *n* even: the innermost ring will have a 2 columns and *n-m+2* rows

Note that each cell in all but the innermost ring has an inward neighbor *unless* it is a corner.  (The corner cells present a small technical problem.)  Now let's talk about the algorithm.

## Algorithm

Bear in mind that inwinder is just sidewinder with a couple of twists.

Instead of proceeding in a row, we proceed in a ring.  Whether we go clockwise or counterclockwise doesn't actually matter.  For no particular reason except that "clockwise" is shorter than "counterclockwise" or "anticlockwise", we will go clockwise.  It's a completely arbitrary choice.

Next we ramdomly pick a cell in the ring.  This cell is now the first cell in the ring, and its counterclockwise neighbor is now the last cell.

If we are not in a corner cell and not in the last cell, we flip a coin.  If it lands face down, we continue clockwise, extending our run by carving a passage clockwise.  If it lands face up, we choose a cell in the current run (but not a corner cell!) and carve a passage inward.

If we are in a corner cell and not the last cell, we just continue the clockwise run.

If we are in the last cell and it is not a corner cell, we close out the run and carve inward from somewhere in the run.

Finally if we are in the last cell and it is a corner cell we carve a passage from this cell to its predecessor.  If the run is still open, we also carve inward from the run.

### The innermost tier

In the innermost ring, there is no way to carve inward, so we simply carve clockwise from first to last.

Ah! But if the smaller dimension is odd there's a problem!  We have either a single strand in a row or column,  In this case, we simply carve a passage from one end to the other.

## Example 1

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.inwinder import Inwinder
    5> print(Inwinder.on(maze))
          Inwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       61
                            inward       41
                          backward        1
```

Notice that "backward" was posted as 1.  The last cell in one of the rings was a corner in the ring.

```
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |   |           |                   |
    +---+   +---+---+   +---+   +---+   +---+---+---+---+
    |   |       |   |   |               |   |   |   |   |
    +   +   +---+   +   +---+---+---+   +   +   +   +   +
    |   |               |       |   |                   |
    +   +   +---+---+   +---+   +   +---+   +---+   +---+
    |       |   |                       |       |   |   |
    +---+---+   +   +---+---+---+---+---+   +---+---+   +
    |                                           |       |
    +   +---+   +   +   +---+---+   +   +   +---+   +---+
    |   |       |   |   |           |   |               |
    +   +---+   +---+   +---+---+---+   +---+   +---+---+
    |   |           |           |       |               |
    +   +---+   +   +   +---+---+---+   +---+   +---+---+
    |       |   |   |               |   |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

To find a path joining two cells, look to the center.  Start in one cell and work inwards toward the center.  Then do the same with the other.  If the paths meet, follow one to the meeting point and then follow the other back to its source.  If the two paths don't meet, simply continue in the center until they do.

Let's do this with an example.  We'll label the cells as before.  Then we'll work out a path from the southwest corner to the northeast corner.

```
    7> from mazes.Grids.oblong_rings import ConcentricOblongs
    8> rings = ConcentricOblongs(maze.grid)
    9> for cell in maze.grid:
    ...     cell.label = rings.tier_for(cell)
    ...
    10> print(maze)

        Legend:
          0, 1, 2, 3 - ring labels from above
          S - the source (southwest corner)
          T - the target (northeast corner)
          * - path to center
          X - where a path enters the innermost ring
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 0   0   0   0 | 0 | 0   0   0 | *   *   *   *   T |
    +---+   +---+---+   +---+   +---+   +---+---+---+---+
    | 0 | 1   1 | 1 | 1 | 1   1   1   * | 1 | 1 | 1 | 0 |
    +   +   +---+   +   +---+---+---+   +   +   +   +   +
    | 0 | 1   2   2   2 | 2   2 | 2 | *   *   2   1   0 |
    +   +   +---+---+   +---+   +   +---+   +---+   +---+
    | 0   1 | 2 | 3   3   3   3   3   3 | X   2 | 1 | 0 |
    +---+---+   +   +---+---+---+---+---+   +---+---+   +
    | *   *   *   X   3   3   3   3   3   3   2 | 1   0 |
    +   +---+   +   +   +---+---+   +   +   +---+   +---+
    | * | 1   2 | 2 | 2 | 2   2   2 | 2 | 2   2   1   0 |
    +   +---+   +---+   +---+---+---+   +---+   +---+---+
    | * | 1   1   1 | 1   1   1 | 1   1 | 1   1   1   0 |
    +   +---+   +   +   +---+---+---+   +---+   +---+---+
    | S   0 | 0 | 0 | 0   0   0   0 | 0 | 0   0   0   0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

There is just one path that joins the two cells marked with an X.  It runs through innermost ring cells.

## Example 2

The innermost ring is always a path.  This is least obvious if the maze is square with an odd length side.  In this case, the innermost ring is a single cell.

```
    11> maze = Maze(OblongGrid(9, 9))
    12> print(Inwinder.on(maze))
          Inwinder Tree (statistics)
                            visits        6
                             cells       81
                          passages       80
                             tiers        5
                            onward       38
                            inward       42
                          backward        0
    13> print(maze)
    +---+---+---+---+---+---+---+---+---+
    |       |   |               |       |
    +---+   +   +---+   +---+---+   +   +
    |       |   |           |       |   |
    +   +   +   +---+   +---+   +---+---+
    |   |               |   |       |   |
    +---+---+   +---+---+   +   +---+   +
    |               |   |               |
    +---+   +   +   +   +   +---+   +---+
    |       |   |               |       |
    +---+   +---+   +   +---+---+---+---+
    |       |       |           |   |   |
    +   +   +   +   +   +   +---+   +   +
    |   |   |   |   |   |               |
    +   +   +   +   +   +---+   +   +---+
    |   |   |   |   |       |   |       |
    +   +---+   +   +   +   +---+   +---+
    |   |       |   |   |       |       |
    +---+---+---+---+---+---+---+---+---+
```

That degree 4 cell in the center of the maze is the innermost ring.

## Example 3

The implementation doesn't offer options for onward or inward as onward (clockwise or counterclockwise) makes no difference and there is only one way to go inward.  But it does allow for modifying the coin toss behavior or the run choice behavior.

In line 15, I set the *which* option to -1 to always take the last element (clockwise) in the run.

```
    14> maze = Maze(OblongGrid(9, 9))
    15> print(Inwinder.on(maze, which=-1))
          Inwinder Tree (statistics)
                            visits        6
                             cells       81
                          passages       80
                             tiers        5
                            onward       33
                            inward       46
                          backward        1
    16> print(maze)
    +---+---+---+---+---+---+---+---+---+
    |       |       |   |   |   |   |   |
    +---+   +---+   +   +   +   +   +   +
    |       |   |       |   |   |       |
    +---+   +   +---+   +   +   +   +---+
    |                       |           |
    +   +---+---+---+---+   +   +---+---+
    |   |               |       |       |
    +---+---+   +---+   +   +---+   +---+
    |           |       |   |       |   |
    +   +   +---+   +   +   +   +---+   +
    |   |   |       |                   |
    +---+---+   +---+   +   +---+---+---+
    |               |   |               |
    +---+   +   +   +---+   +   +---+---+
    |       |   |       |   |       |   |
    +---+   +---+---+   +---+   +   +   +
    |               |       |   |       |
    +---+---+---+---+---+---+---+---+---+
```
Note the degree 4 cell southeast of the center.  This is not a binary tree.  In normal sidewinder, always choosing the last cell in the run is equivalent to running simple binary tree. Organizing the grid into rings introduces some complexity that isn't present in the usual row-column organization.

There is another degree 4 cell two rows down and two columns to the left of the center cell.

Note that the last cell backward adjustment was made this time.  So there was a ring whose last cell was a corner.