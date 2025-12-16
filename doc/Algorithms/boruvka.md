# Borůvka's minimum weight spanning tree algorithm

* Module: *mazes.Algorithms.boruvka*
* Class: *Boruvka*

Examples:

* Example 1.  Basic operation
* Example 2.  Expanding a maze using Borůvka's algorithm
* Example 3.  A simple weight function
* Example 4.  A fancier weight function
* Note.  Duplicate weights

## Introduction

The algorithm was discovered and first published by Otakar Borůvka in 1926 for optimizing Moravia's electrical network.  It was rediscovered by Gustave Choquet in 1938, by several researchers in the 1950s, and again by Georges Sollin in 1965.  It is also known as Sollin's algorithm.

It is of special interest because, unlike *Prim's algorithm* (discovered by Vojtěch Jarník in 1930 and rediscovered bt Robert Clay Prim in 1957) and *Kruskal's algorithm* (discovered by Joseph Kruskal, 1956), *Borůvka's algorithm* is inherently parallel.  (It can easily be implemented serially, as it is in this implementation.)

The prerequisites are a linearly ordered and injective (*i.e.* one to one) set of edge weights,  If the weight function is not one-to-one, the resulting spanning subgraph may contain circuits.

## Our implementation

Our implementation takes three arguments:

* an empty maze on a grid;
* an optional weight map; and
* an optional flag which, when set, will raise a *Warning* exception if a circuit is created.

If the maze is not empty, then cells will be collected into components before processing starts.

If no weight map is supplied, a random one-to-one map will be generated.  If a supplied weight map is not one-to-one and a circuit is detected, then either an exception is raised (*verify=True*) or the status will indicate that a circuit is present.  Since our intention is to create mazes, the default is not to raise the exception.  A *KeyError* exception will, however, be raised if a grid edge is missing from a supplied weight map.

## Example 1.  Basic operation

```
$ python
Python 3.10.12 (main, Nov  4 2025, 08:48:33) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.boruvka import Boruvka
>>> maze = Maze(OblongGrid(8,13))
>>> print(Boruvka.on(maze))
          Borůvka's minimum weight spanning tree algorithm (statistics)
                            visits        4
                             cells      104
                          passages      103
                   visits (serial)      351
                          discards      164
                             links      103
                            merges      103
                   components (in)      104
                  components (out)        1
```
The maze was empty going in, so there was one component for each cell going in.  Since there were 103 passages, 104 cells, and 1 component going out, we know that the maze is a spanning tree on the grid.

The 4 visits indicate that a lot was happening in parallel.  Of course, our implementation is serial as indicated by the "serial visits", the discards (of unneeded edges), and the merges (of components).
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |                           |       |       |   |
+   +---+   +---+---+   +---+   +   +---+   +   +   +
|       |   |           |       |       |   |       |
+   +   +---+   +   +---+   +---+   +---+   +---+---+
|   |           |   |   |       |               |   |
+---+---+---+   +   +   +---+---+---+   +   +---+   +
|               |           |           |           |
+   +---+---+---+---+   +---+---+   +---+   +---+   +
|   |               |   |   |   |   |           |   |
+   +   +   +---+   +   +   +   +   +---+---+---+   +
|   |   |       |   |       |   |           |       |
+   +---+---+   +   +   +   +   +   +---+   +---+   +
|   |           |       |   |   |   |           |   |
+   +---+   +   +   +---+   +   +   +---+   +---+---+
|   |       |   |       |           |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 2.  Expanding a maze using Borůvka's algorithm

In this example, we deliberately create a circuit in the southwest corner:
```
>>> maze = Maze(OblongGrid(8,13))
>>> cell = maze.grid[0,0]
>>> maze.link(cell, cell.north)
>>> maze.link(cell, cell.east)
>>> maze.link(cell.east, cell.east.north)
>>> maze.link(cell.north, cell.north.east)
```
Our implementation will treat this 4-cell circuit as if it were a single cell.  So when we look at the statistics, we should think of our input as a 101-cell grid (100 isolated cells plus the 4-cell circuit, or 101 components).

Now we carve the maze:
```
>>> print(Boruvka.on(maze))
          Borůvka's minimum weight spanning tree algorithm (statistics)
                            visits        4
                             cells      104
                     passages (in)        4
                          passages      104
                   visits (serial)      343
                          discards      160
                             links      100
                            merges      100
                   components (in)      101
                  components (out)        1
```
101 components going in, 100 merges and 1 component going out tells us we have a spanning tree on the components going in.  But 104 cells, 104 passages and 1 component tells us we are one passage in excess of a spanning tree on the grid.  Borůvka's algorithm didn't create a new circuit, so no circuit is indicated.

Here is the maze with a nice 4-cell circuit in the lower left.
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |   |           |               |       |
+---+   +   +   +---+   +---+   +---+---+---+   +---+
|   |   |       |           |       |               |
+   +   +---+   +---+---+   +   +---+---+---+   +---+
|           |       |       |   |           |       |
+---+   +---+---+   +   +---+   +---+---+   +---+   +
|           |               |               |       |
+---+   +   +---+   +---+---+   +---+   +---+---+   +
|       |   |           |   |   |                   |
+   +---+---+---+---+   +   +---+   +   +---+---+   +
|   |   |   |   |               |   |       |       |
+   +   +   +   +---+---+   +   +---+   +---+---+   +
|                           |               |       |
+   +   +---+   +   +---+   +---+   +   +---+---+   +
|           |   |       |       |   |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 3.  A simple weight function

We can supply weights to the grid edges instead of letting the weight mapping be created randomly.  Here we simply assign each edge a consecutive number the first time that it is encountered.  Since dictionaries (like the grid's indexed list of cells and the cell's indexed list of neighbors) are not randomly ordered in Python 3, one might expect the structure of the underlying maze to be fairly predictable.  But let's see what happens.

We start fresh:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.boruvka import Boruvka
>>> maze = Maze(OblongGrid(8,13))
```

We need to create a dictionary containing the edge weights.  The edges are represented as frozenset objects.  (The edges are unordered, so we need a set instead of a list.  Dictionary keys need to be hashable, so we would replace lists by tuples, or, in this case, sets by frozenset objects.  Note that we check here whether an edge is already a key before we assign a weight.
```
>>> weights = dict()
>>> w = 0
>>> for cell in maze.grid:
...     for nbr in cell.neighbors:
...         edge = frozenset([cell, nbr])
...         if edge not in weights:
...             w += 1
...             weights[edge] = w
...
```

How many grid edges are there?
```
>>> print(w)
187
```
We can check that using Euler's Lemma:
```
                                             cells   degree   product
    Corner cells (degree 2)                      4 × 2 =            8
    Perimeter cells (degree 3)    2(6+11)=34    34 × 3 =          102
    Interior cells (degree 4)      (6×11)=66    66 × 4 =          264
                                               ----              -----
    Sums                                       104 cells     2e = 374

    Number of edges     e = 374/2 = 187
```
Now let's carve the maze:
```
>>> print(Boruvka.on(maze, edge_weights=weights))
          Borůvka's minimum weight spanning tree algorithm (statistics)
                            visits        1
                             cells      104
                          passages      103
                   visits (serial)      187
                          discards        0
                             links      103
                            merges      103
                   components (in)      104
                  components (out)        1
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Does that look reasonably predictable?

## Example 4.  A fancier weight function

Here we'll use a simple linear congruential recurrence to generate some pseudo-random numbers.  The recurrence is:
```
              z[t+1] = (11 z[t] + 7) mod 29
    with      z[0] = 0

    So:       z[1] = 7
              z[2] = (77 + 7) mod 29  = 84 - 58 = 26
              z[3] = (286+7) mod 29 = 293 mod 29 = 3
    And so on...
```
It has period 29, i.e. it repeats after 29 times:
```
>>> z = 0
>>> zed = lambda t: (11*z + 7) % 29
>>> zees = list()
>>> for t in range(30):
...    zees.append(z)
...    z = zed(t)
...
>>> zees
[0, 7, 26, 3, 11, 12, 23, 28, 25, 21, 6, 15, 27, 14, 16, 9, 19, 13, 5, 4, 22, 17, 20, 24, 10, 1, 18, 2, 0, 7]
```
Looks good!  But let's see how we fair.  We'll include a sequence number to make it unique:  (z(t), t).  It has period 29:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.boruvka import Boruvka
>>> maze = Maze(OblongGrid(8,13))
>>> z = 0
>>> n = 0
>>> weights = dict()
>>> for cell in maze.grid:
...     for nbr in cell.neighbors:
...         edge = frozenset([cell, nbr])
...         if edge not in weights:
...             z = (11*z + 7) % 29
...             n += 1
...             weights[edge] = (z, n)
...
>>> print(Boruvka.on(maze, edge_weights=weights))
          Borůvka's minimum weight spanning tree algorithm (statistics)
                            visits        4
                             cells      104
                          passages      103
                   visits (serial)      364
                          discards      177
                             links      103
                            merges      103
                   components (in)      104
                  components (out)        1
```
The proof as they say is in the pudding:
```>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |           |       |           |   |   |
+   +   +   +---+   +   +---+   +---+   +---+   +   +
|   |   |   |   |   |           |   |   |   |       |
+---+   +---+   +   +---+---+---+   +   +   +   +---+
|           |                   |       |           |
+---+   +   +---+   +---+   +---+   +   +---+   +---+
|   |   |           |   |   |   |   |               |
+   +   +---+---+---+   +   +   +   +---+---+---+   +
|           |       |       |           |           |
+---+   +---+   +---+   +   +---+   +   +   +---+---+
|       |   |   |   |   |           |   |   |   |   |
+---+   +   +   +   +   +---+   +---+---+---+   +   +
|       |       |           |               |       |
+   +   +   +   +---+   +   +   +---+   +   +   +---+
|   |   |   |           |   |   |       |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
As general rule, it's probably better to use Python's random number generator, but the results here were satisfactory.

## Note.  Duplicate weights

Prim's algorithm and Kruskal's algorithm work in the presence of collisions (*i.e.* duplicate weights), but Borůvka's algorithm can fail.  When it does fail, it produces circuits.  Note, however, that failure is not guaranteed...

In particular, if the edge traversal is stable, *i.e.* equal weight edges are always traversed in the same order, then Borůvka's algorithm won't fail.  Stability might depend on the particulars of the Python implementation.  In any case, I was unable to generate a failure.

Shuffling each cell's incident joins before traversing them would probably generate circuits with some frequency in the presence of equal weights.  But this would be at a small cost to running time.
