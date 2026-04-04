# Hierholzer's Algorithm

Hierholzer's algorithm is an algorithm for finding Eulerian tours or Eulerian trails in graphs that happen to admit them.

In 1735, Leonhard Euler (1707-1783) established that a *closed walk* (or *tour*) covering every edge in a graph exactly once is only possible if every vertex in the graph is incident to an even number of edges.  He also established that an *open walk* (or *trail*) covering every edge in a graph exactly once (starting and ending in different vertices) is only possible when exactly two vertices are incident to an odd number of vertices.  In this case, the odd vertices are the terminal vertices for the walk.  He suspected but did not prove that these conditions were not only necessary but also sufficient.  He was able to show that the two problems were actually equivalent.  (To prove equivalence, imagine that you can teleport between the odd-degree vertices.  Adding a teleporting edge links the two problems.)

His results in 1741 in proceedings of the Academy in Saint Petersberg (modern-day Leningrad).  His study was a reply to Christian Goldbach about a problem that is now known as the Königsberg Bridges problem.  The paper is generally considered to be a founding paper both for topology and for graph theory.  Euler's name for the area was *geometria situs* (geometry of location), from a coinage by Gottfried Leibniz.

Euler didn't use modern graph theory language (*i.e.* vertex/edge or node/arc) -- instead he thought of land masses (riverbanks and islands) that are connected by bridges.  He implicitly assumed that the graphs (land/bridge networks were connected, *i.e.*, that one could reach any landmass from any other landmass by crossing a sequence of bridges.

Sufficiency of Euler's conditions was proved by Carl Hierholzer (1840-1871) in 1871.  A collegue arranged for posthumous publication in 1873.  Hierholzer's algorithm is implicit in his proof.

## The algorithm

Essentially one starts with a (possibly partial) tour which is possible since every vertex has even degree.  Start in some given vertex.  Entering another vertex leaves a free edge since the number of incident edges is odd.  So eventually one must return the starting vertex.  If there there are still free edges in some vertex in the tour, we can insert a tour at that vertex.  If the graph is connected, we will eventually exhaust the edge set.

The algorithm is approximately linear in the number of edges.

## Demonstration module

We can demonstrate the algorithm on the console using rectangular mazes, but the graphics leave a lot to be desired.  The biggest problem with Eulerian tours and trails are that vertices can be traversed more than once and our basic tools don't provide a good way to label edges.  With that in mind, let's look at the demonstration module help:

```
    $ python -m demos.hierholzer -h
    usage: hierholzer.py [-h] [-d ROWS COLS] [--trail]

    Hierholzer's algorithm demonstration

    options:
      -h, --help            show this help message and exit
      -d ROWS COLS, --dim ROWS COLS
                            dimensions of the maze.
      --trail               set this flag to create an Eulerian trail.

    Some dimension won't work.
```

The demonstration module creates a (non-random) maximally Eulerian maze in a rectangular grid.  If we pick grid dimensions that don't support an Eulerian maze, then an exception will be raised.  We can opt for a trail instead of a tour, in which case one passage will be removed at random to create a maximally   path-Eulerian maze.  The maze is processed using Hierholzer's algorithm and a trail or tour is returned.  The maze is displayed with two or three labelled celled, and the trail or tour is then displayed.

## Examples

### Example 1(a) - a small Eulerian tour

```
    $ python -m demos.hierholzer -d 2 2
    Namespace(dim=[2, 2], trail=False)
    Creating a maximally Eulerian 2×2 oblong maze.
              Hierholzer's Algorithm (statistics)
                                visits       12
                        isolated cells        0
                               packets        4
                               rejects        4
                               rotates        4
                            start cell  any
                            first cell  (1, 0)
    +---+---+
    | 0   1 |
    +   +   +
    | n     |
    +---+---+
    Eulerian tour:
    (1,0) -- (1,1) -- (0,1) -- (0,0) -- (1,0)
    Passages in maze: 4
      Steps in trail: 4
       Cells spanned: 4
    Passages spanned: 4
```
We asked for an Eulerian tour of a complete 2-row 2-column Von Neumann maze.  The tour is simple -- it simply follows the walls.   There are four edges in the maze.  The algorithm visits each edge exactly three times, once to add it to the tour, once to reject the edge in the reverse direction, and once to rotate the tour in search of unused edges.

In the maze itself, we labelled the terminal cell as "0", its successor in the tour as "1" and its predecessor (*i.e.* the penultimate or next-to-last cell) as "n".

The tour starts in the NW corner cell (1,0), and proceed clockwise around the maze.  The statistics displayed after the tour confirm that all four edges wer included in the tour.

### Example 1(a) - a small Eulerian trail

```
    $ python -m demos.hierholzer -d 2 2 --trail
    Namespace(dim=[2, 2], trail=True)
    Creating a maximally Eulerian 2×2 oblong maze.
    Deleting the passage between (0, 1) and (1, 1)
              Hierholzer's Algorithm (statistics)
                                visits        9
                        isolated cells        0
                               packets        3
                               rejects        3
                               rotates        3
                            start cell  (0, 1)
                            first cell  (0, 1)
    +---+---+
    |     Y |
    +   +---+
    |     X |
    +---+---+
    Eulerian trail:
    (0,1) -- (0,0) -- (1,0) -- (1,1)
    Passages in maze: 3
      Steps in trail: 3
       Cells spanned: 4
    Passages spanned: 3
```

If we delete one edge from an Eulerian maze, we get two odd-degree cells and a maze with an Eulerian tour.  Here the demonstration module deleted the edge along the east wall.  Note that each of the three remaining edges was visited three times, one to add the edge to the trail, once to reject a return edge and once to rotate the trail to find unused edges.

The trail starts in the SE corner in cell "X" and proceeds clockwise to cell "Y".

### Example 2 (a) - A long tour

The default is an 8-row 13-column maze with 164 edges,

```
    $ python -m demos.hierholzer
    Namespace(dim=(8, 13), trail=False)
    Creating a maximally Eulerian 8×13 oblong maze.
              Hierholzer's Algorithm (statistics)
                                visits      492
                        isolated cells        0
                               packets      164
                               rejects      164
                               rotates      164
                            start cell  any
                            first cell  (0, 3)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |       |       |       |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |                                                   |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |                                                   |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |             1                                     |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |           | 0   n |       |       |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The tour started and ended in the bottom row.  From the statistics, each edge was visited three times.  Using the displayed tour below, here is the first part of the tour:
```
    +---+---+   +   +
    | K ← J ← I
    + ↓ +---+ ↑ +   +
    | L → M → ⬑ ← G
    +---+---+ ↓ + ↑ +
    | C → D → ⇸ → F
    + ↑ +---+ ↓ +   +
    | B ← A ← ↰ → Q
    +---+---+ ↑ +   +
    | 4 ← 3 ← ⇷ ← 1
    + ↓ +---+ ↑ + ↑ +
    | 5 → 6 → 7 | 0   n |
    +---+---+---+---+---+---+
```
Notice that the trail meets at many of the vertices (in fact, all vertices of degree greater than 2).  I attempted to emphasize the first passage through the cell, but it's admittedly hard to follow.  The complete tour is below.
```
    Eulerian tour:
    (0,3) -- (1,3) -- (1,2) -- (1,1) -- (1,0) -- (0,0) -- (0,1) -- (0,2)
       -- (1,2) -- (2,2) -- (2,1) -- (2,0) -- (3,0) -- (3,1) -- (3,2)
       -- (3,3) -- (4,3) -- (4,2) -- (5,2) -- (5,1) -- (5,0) -- (4,0)
       -- (4,1) -- (4,2) -- (3,2) -- (2,2) -- (2,3) -- (3,3) -- (3,4)
       -- (4,4) -- (5,4) -- (6,4) -- (6,5) -- (7,5) -- (7,6) -- (6,6)
       -- (5,6) -- (4,6) -- (3,6) -- (3,7) -- (3,8) -- (4,8) -- (4,9)
       -- (5,9) -- (5,10) -- (4,10) -- (4,11) -- (5,11) -- (5,12)
       -- (4,12) -- (4,11) -- (3,11) -- (2,11) -- (2,10) -- (2,9)
       -- (3,9) -- (3,8) -- (2,8) -- (1,8) -- (0,8) -- (0,7) -- (1,7)
       -- (1,8) -- (1,9) -- (0,9) -- (0,10) -- (1,10) -- (2,10) -- (3,10)
       -- (3,9) -- (4,9) -- (4,10) -- (3,10) -- (3,11) -- (3,12) -- (2,12)
       -- (2,11) -- (1,11) -- (1,12) -- (0,12) -- (0,11) -- (1,11)
       -- (1,10) -- (1,9) -- (2,9) -- (2,8) -- (2,7) -- (2,6) -- (1,6)
       -- (1,7) -- (2,7) -- (3,7) -- (4,7) -- (5,7) -- (5,6) -- (5,5)
       -- (6,5) -- (6,6) -- (6,7) -- (5,7) -- (5,8) -- (5,9) -- (6,9)
       -- (6,10) -- (5,10) -- (5,11) -- (6,11) -- (7,11) -- (7,12)
       -- (6,12) -- (6,11) -- (6,10) -- (7,10) -- (7,9) -- (6,9) -- (6,8)
       -- (7,8) -- (7,7) -- (6,7) -- (6,8) -- (5,8) -- (4,8) -- (4,7)
       -- (4,6) -- (4,5) -- (4,4) -- (4,3) -- (5,3) -- (6,3) -- (6,4)
       -- (7,4) -- (7,3) -- (6,3) -- (6,2) -- (7,2) -- (7,1) -- (7,0)
       -- (6,0) -- (6,1) -- (6,2) -- (5,2) -- (5,3) -- (5,4) -- (5,5)
       -- (4,5) -- (3,5) -- (2,5) -- (1,5) -- (0,5) -- (0,6) -- (1,6)
       -- (1,5) -- (1,4) -- (1,3) -- (2,3) -- (2,4) -- (2,5) -- (2,6)
       -- (3,6) -- (3,5) -- (3,4) -- (2,4) -- (1,4) -- (0,4) -- (0,3)
```
And here is confirmation that all was accounted for:
```
    Passages in maze: 164
      Steps in trail: 164
       Cells spanned: 104
    Passages spanned: 164
```

### Example 2 (b) - a long Eulerian trail

```
    $ python -m demos.hierholzer --trail
    Namespace(dim=(8, 13), trail=True)
    Creating a maximally Eulerian 8×13 oblong maze.
    Deleting the passage between (3, 7) and (3, 6)
```
The wall that was erected in the passage's place is marked by the cells labelled "X" and "Y" in the grid below.  Note that they both have odd degree.
```
              Hierholzer's Algorithmm (statistics)
                                visits      489
                        isolated cells        0
                               packets      163
                               rejects      163
                               rotates      163
                            start cell  (3, 7)
                            first cell  (3, 7)
```
We start the trail in one of the two odd-degree cells (cell (3,7) labelled "X") and finish the trail in the other (cell (3,6) labelled "Y").  Again each passage in the maze was visited exactly 3 times, evidence again that the time complexity algorithm is roughly linear in the the number of edges.
```
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |       |       |       |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |                                                   |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |                         Y | X                     |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |                                                   |
    +---+---+   +   +   +   +   +   +   +   +   +   +---+
    |                                                   |
    +   +---+   +   +   +   +   +   +   +   +   +   +   +
    |           |       |       |       |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here is the actual trail:
```
Eulerian trail:
(3,7) -- (3,8) -- (4,8) -- (5,8) -- (6,8) -- (6,7) -- (7,7) -- (7,8)
   -- (6,8) -- (6,9) -- (7,9) -- (7,10) -- (6,10) -- (6,9) -- (5,9)
   -- (5,8) -- (5,7) -- (5,6) -- (5,5) -- (6,5) -- (7,5) -- (7,6)
   -- (6,6) -- (6,5) -- (6,4) -- (5,4) -- (5,5) -- (4,5) -- (4,6)
   -- (4,7) -- (4,8) -- (4,9) -- (5,9) -- (5,10) -- (4,10) -- (4,11)
   -- (4,12) -- (5,12) -- (5,11) -- (6,11) -- (7,11) -- (7,12)
   -- (6,12) -- (6,11) -- (6,10) -- (5,10) -- (5,11) -- (4,11)
   -- (3,11) -- (2,11) -- (1,11) -- (0,11) -- (0,12) -- (1,12)
   -- (1,11) -- (1,10) -- (2,10) -- (2,9) -- (3,9) -- (3,10) -- (3,11)
   -- (3,12) -- (2,12) -- (2,11) -- (2,10) -- (3,10) -- (4,10)
   -- (4,9) -- (3,9) -- (3,8) -- (2,8) -- (1,8) -- (1,9) -- (0,9)
   -- (0,10) -- (1,10) -- (1,9) -- (2,9) -- (2,8) -- (2,7) -- (1,7)
   -- (1,8) -- (0,8) -- (0,7) -- (1,7) -- (1,6) -- (0,6) -- (0,5)
   -- (1,5) -- (1,4) -- (2,4) -- (3,4) -- (3,5) -- (2,5) -- (2,4)
   -- (2,3) -- (1,3) -- (1,4) -- (0,4) -- (0,3) -- (1,3) -- (1,2)
   -- (0,2) -- (0,1) -- (0,0) -- (1,0) -- (1,1) -- (1,2) -- (2,2)
   -- (2,1) -- (2,0) -- (3,0) -- (3,1) -- (3,2) -- (2,2) -- (2,3)
   -- (3,3) -- (4,3) -- (4,4) -- (3,4) -- (3,3) -- (3,2) -- (4,2)
   -- (4,3) -- (5,3) -- (6,3) -- (6,4) -- (7,4) -- (7,3) -- (6,3)
   -- (6,2) -- (6,1) -- (6,0) -- (7,0) -- (7,1) -- (7,2) -- (6,2)
   -- (5,2) -- (4,2) -- (4,1) -- (4,0) -- (5,0) -- (5,1) -- (5,2)
   -- (5,3) -- (5,4) -- (4,4) -- (4,5) -- (3,5) -- (3,6) -- (2,6)
   -- (1,6) -- (1,5) -- (2,5) -- (2,6) -- (2,7) -- (3,7) -- (4,7)
   -- (5,7) -- (6,7) -- (6,6) -- (5,6) -- (4,6) -- (3,6)
```
Finally, we note that each of the passages in the maze appeared exactly once
in the trail.  (Many of the cells, of course, appear more than once.)
```
Passages in maze: 163
  Steps in trail: 163
   Cells spanned: 104
Passages spanned: 163
```

As the trail contains 163 passages (or steps), it must contain 164 stepping stones (or cells).  Since all 104 cells appear in the trail, we have:
```
        164 - 104 = 60 cells reached more than once. 
```
The degree 2 cells are all in the first, second, and last columns, or in the top or bottom row:
```
          26    cells in top or bottom row (13 x 2)
          24    cells in first, second, or last row (8 x 3)
        -  6    cells counted twice above (2 x 3)
        =====
          44    cells of degree 2
```
The cells of degree 3 or 4 appear in 6 rows and 10 columns, for a total of 60 cells which must be traversed twice in the trail.  Note that 60+44=104, the total number of cells.  And since the 60 degree 3 or 4 cells are traversed exactly twice, we have accounted for all of the repetitions.

### Example 3 - the devil is in the details

Let's do an example.  First we need an Eulerian maze, but preferably one we haven't seen before.  Although finding a maximally Eulerian maze in an arbitrary grid seems to be a hard problem, the *eulerian_oblong* module actually works on oblong toroidal grids when the number of rows and columns is even.  Note that for a Von Neumann oblong toroidal grid, all we need to do is include every edge.  The *eulerian_oblong* module does check that the grid is oblong, but it only assumes that the grid has north/south/east/west connections.  For the both dimensions even case, it detects border cells by checking for missing neighbors.  Since there are no missing neighbors, it ends up making every cell a degree-4 cell.  If the one or both of the dimensions are odd, the checks are more complicated, so the results may not be so nice.

With the cautions out of the way, let's proceed.  First we carve the maze:
```
    $ python
    >>> from mazes.Grids.torus import TorusGrid
    >>> from mazes.maze import Maze
    >>> maze = Maze(TorusGrid(8,10))
    >>> from mazes.Grids.eulerian_oblong import EvenEven
    >>> EvenEven(maze)
```
Next we look at it:
```
          A   B   C   D   E   F   G   H   I   J
        ┏   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┓
      7                                           7
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      6                                           6
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      5                                           5
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      4                                           4
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      3                                           3
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      2                                           2
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      1                                           1
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      0                                           0
        ┗   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┛
          A   B   C   D   E   F   G   H   I   J
```
When displaying the tour, we'll use the alphabetic column labels.  But first we need to find an Eulerian tour.  It's obvious that every cell is degree 4, so there must be one.  In fact, there are many.  (We can find a whole family by translation - shifting the tour a fixed number of rows and columns.  But even after we discard that entire family, we can consider rotations and reflections...  But that won't even scratch the surface!)

But enough! Time to show our hand:
```
    >>> from mazes.Algorithms.hierholzer import Hierholzer
    >>> status = Hierholzer.on(maze)
    >>> print(status)
              Hierholzer's Algorithm (statistics)
                                visits      480
                        isolated cells        0
                               packets      160
                               rejects      160
                               rotates      160
                            start cell  any
                            first cell  (1, 5)
```
Each cell has four incident passages, but each passage is counted twice, so we have a total of (80x4)/2 or 160 passages.  Each was visited exactly three times in Hierholzer's algorithm.

We needed to keep the status to find the tour:
```
    >>> trail = status.trail
```
Let's mark the start and end of the tour:
```
    >>> cell1, passage, cell2 = trail[0]
    >>> cell1.label = "X"
    >>> cell2.label = "<"
    >>> cell1, passage, cell2 = trail[-1]
    >>> cell1.label = ">"
    >>> assert cell2.label == "X"
    >>> print(maze)
          A   B   C   D   E   F   G   H   I   J
        ┏   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┓
      7                                           7
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      6                                           6
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      5                                           5
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      4                                           4
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      3                                           3
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      2                       <                   2
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      1                       X   >               1
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      0                                           0
        ┗   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┛
          A   B   C   D   E   F   G   H   I   J
```
The less than symbol ("&gt;") is used to label the second cell and the greater than symbol ("&lt;") the penultimate cell.  The first and last cell is labelled "X".  Note the *assert* statement.  It verifies that we have a close walk.

The variable *trail* contains our tour.  It is a list with 160 entries.  Each entry is an ordered triple (basically a specially labelled tuple which is set up to contain exactly three entries):
```
    >>> type(trail)
    <class 'list'>
    >>> len(trail)
    160
    >>> type(trail[0])
    <class 'mazes.Algorithms.hierholzer.triple'>
    >>> len(trail[0])
    3
```
The entries in the triples consist of a from-cell, a passage, and a to-cell.  We promised to use the alphabetic column labels, so let's encode the trail.  Apart from the last entry, we can simply use the from-cell.  We use the to-cell in the last entry:
```
    >>> s = ""
    >>> for step in trail:
    ...     cell1, passage, cell2 = step
    ...     i, j = cell1.index
    ...     col = chr(ord('A')+j)
    ...     s += f"{i}{col} -- "
    ...
    >>> i, j = cell2.index
    >>> col = chr(ord('A')+j)
    >>> s += f"{i}{col}"
    >>> print(s)
```
With 161 cells in the trail, we'll need to edit the output to insert a few newlines:
```
    1F -- 2F -- 3F -- 4F -- 5F -- 5E -- 4E -- 3E -- 2E -- 2D --
     1D -- 1C -- 2C -- 3C -- 4C -- 4B -- 4A -- 3A -- 3J -- 2J --
     2A -- 1A -- 0A -- 0B -- 7B -- 6B -- 6C -- 7C -- 0C -- 0B --
     1B -- 1C -- 0C -- 0D -- 7D -- 6D -- 5D -- 4D -- 4C -- 5C --
     5D -- 5E -- 6E -- 6D -- 6C -- 5C -- 5B -- 5A -- 5J -- 5I --
     4I -- 4H -- 3H -- 3I -- 4I -- 4J -- 4A -- 5A -- 6A -- 6J --
     6I -- 7I -- 7J -- 0J -- 1J -- 2J -- 2I -- 2H -- 1H -- 1I --
     2I -- 3I -- 3J -- 4J -- 5J -- 6J -- 7J -- 7A -- 0A -- 0J --
     0I -- 0H -- 7H -- 6H -- 5H -- 5I -- 6I -- 6H -- 6G -- 5G --
     5H -- 4H -- 4G -- 3G -- 3F -- 3E -- 3D -- 4D -- 4E -- 4F --
     4G -- 5G -- 5F -- 6F -- 6G -- 7G -- 0G -- 0F -- 7F -- 7G --
     7H -- 7I -- 0I -- 1I -- 1J -- 1A -- 1B -- 2B -- 2C -- 2D --
     3D -- 3C -- 3B -- 2B -- 2A -- 3A -- 3B -- 4B -- 5B -- 6B --
     6A -- 7A -- 7B -- 7C -- 7D -- 7E -- 6E -- 6F -- 7F -- 7E --
     0E -- 0D -- 1D -- 1E -- 1F -- 0F -- 0E -- 1E -- 2E -- 2F --
     2G -- 3G -- 3H -- 2H -- 2G -- 1G -- 0G -- 0H -- 1H -- 1G -- 1F
```
In the course of encoding this, we skipped over the to-cells.  They should match up with the from-cell that follows.  We should verify this:
```
    >>> for i in range(len(trail) - 1):
    ...     step1 = trail[i]
    ...     cell1 = step1[2]
    ...     step2 = trail[i+1]
    ...     cell2 = step2[0]
    ...     assert cell1 == cell2
    ...
```

### Example 4 - the devil strikes in the details

If we had used a Klein bottle grid instead of a toroidal grid, we wouldn't have been as lucky.
```
    $ python
    >>> from mazes.Grids.klein import KleinGrid
    >>> from mazes.maze import Maze
    >>> maze = Maze(KleinGrid(8,10))
    >>> from mazes.Grids.eulerian_oblong import EvenEven
    >>> EvenEven(maze)
    Traceback (exception handler)...
    File "maze4c/mazes/edge.py", line 109, in _configure
      raise NotImplementedError("parallel joins are not permitted")
    NotImplementedError: parallel joins are not permitted
```
The passage constructor was told to join two linked cells with a second passage.  (Unfortunately the error message doesn't identify the pair of cells.)

And in case someone wants to create a program which produces maximally Eulerian Klein bottle mazes, here is where things went wrong:
```
    >>> print(maze)
          A   B   C   D   E   F   G   H   I   J
        ┏   ┳━━━┳   ┳━━━┳   ┳━━━┳   ┳━━━┳   ┳━━━┓
      7 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃     0
        ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
      6     ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 1
        ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
      5 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃     2
        ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
      4         ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 3
        ┣   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
      3 ┃                                         4
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      2                                         ┃ 5
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      1 ┃                                         6
        ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
      0                                         ┃ 7
        ┗   ┻━━━┻   ┻━━━┻   ┻━━━┻   ┻━━━┻   ┻━━━┛
          A   B   C   D   E   F   G   H   I   J
```
