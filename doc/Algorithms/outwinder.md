# Outwinder

## Background

If you haven't already done so, read the background section of the documentation for inwinder.  Then continue with the next paragraph.

Outwinder, like its older sibling inwinder, is really just sidewinder with a small twist.  Sidewinder works in rows and columns, but outwinder works in rings.  The corner cell *gotchas* that inwinder must handle are not present in outwinder.

## Grid organization

Grid organization is as for inwinder.  See the section entitled "Grid organization" in the inwinder documentation.

Note that *every* cell in a ring other than the outermost ring (aka: perimeter ring) has *at least one* outward neighbor.  The corner cells have two.  This makes outwinder simpler than inwinder.

## Algorithm

Bear in mind that outwinder is just sidewinder with a couple of twists.

Instead of proceeding in a row, we proceed in a ring.  Whether we go clockwise or counterclockwise doesn't actually matter.  As for inwinder, I chose "clockwise" because it's easier to type.

Next we randomly pick a cell in the ring.  This cell is now the first cell in the ring, and its counterclockwise neighbor is now the last cell.

If we are not in the last cell or in the outermost ring, we flip a coin.  If it lands face down, we continue clockwise, extending our run by carving a passage clockwise.  If it lands face up, we choose a cell in the current run and carve a passage outward.

If we are in the last cell and not in the outermost ring, we close out the run and carve outward from somewhere in the run.

Finally if we are in the last cell of the outermost ring, we do nothing.

## Example

Outwinder is less complicated than inwinder, so one example should suffice.  The *flip*, *run\_choice* and *which* options are handled as in sidewinder and inwinder, so we will not discuss them here.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.outwinder import Outwinder
    5> print(Outwinder.on(maze))
          Outwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       60
                           outward       43
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                         M                         |
    +   +---+   +---+   +---+   +   +   +---+   +---+   +
    |   |       |           |   |   |   |       |       |
    +   +   +---+   +   +   +   +---+   +   +   +---+   +
    |   |       |   |   |   |     T |   |   |   |       |
    +   +   +   +---+   +---+---+---+   +---+---+---+   +
    |   |   |     i | i | i   i   i   i   i |           |
    +   +---+---+   +---+---+---+---+---+---+   +   +   +
    |           | i | i | i | i   i | i | i |   |   |   |
    +   +---+---+---+   +   +---+   +   +   +   +---+   +
    |       | S |   |   |   |           |       |   |   |
    +   +---+   +   +   +   +---+   +---+---+---+   +   +
    |           |   |   |   |       |   |   |   |       |
    +   +---+---+   +   +   +---+   +   +   +   +---+   +
    |                         F | L                     |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

(I manually labelled cells the innermost ring with 'i'.)  Unlike inwinder, the innermost ring is not special.  Regardless of whether it consists of a single cell, a single row or column of cells, or (as above) two rows or two columns of cells, we just divide it into one or more clockwise runs, then choose one of the cells in each run and carve outward.

The outermost ring is special.  Here I labelled the first cell with an 'F' and the last with an 'L'.  Note that the outermost ring is one long clockwise path from F to L.  (The implementation randomly chooses the first cell in each ring.)

Solving the maze is easy.  Suppose we are given two random cells like the ones that I labelled 'S' (for 'source') and 'T' (for 'target').  Here is an easily programmed algorithm:

1.  Find a path from S to L by finding a path outward to the outermost ring and then going clockwise to L.
2.  Likewise, find a path from T to L by finding a path outward to the outermost ring and then going clockwise to L.
3.  Note where two paths first meet.  Lets call that cell M.  (For S and T above, I labelled the meeting point "M".)  Then trace the first path from S to M, and continue following the second path in reverse from M to T.

For an informal algorithm, we could choose any cell in the outermost ring in place of L.  For a computer program implementation, it's simpler to avoid additional backtracking by specifying either F or L as the common destination for both of the trial paths in (1) and (2).