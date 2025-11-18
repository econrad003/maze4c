# The basic wall builder

* module *mazes.WallBuilders.basic\_wallbuilder*
* class *BasicWallbuilder*

## The algorithm

```
    Given a maze M:
        while there is a circuit C in M:
            let e be a passage in C
            delete passage e
```

If *M'* is the maze obtained from *M* by the algorithm described above, then:

* *M'* is *spanning forest* in *M*, *i.e.*,
* each component of *M'* is a tree which spans the corresponding component in *M*.

Equivalently:

* the number of connected components in *M'* is the same as the number of connected components in *M*, and
* each component of *M* is has a spanning tree in a component of *M'*.

## The circuit locator

* Module: *mazes.Algorithms.dfs\_circuit\_locator*
* Class: *CircuitFinder*

It locates a circuit using a depth-first search. The search can be randomized or it can proceed in cell-passage order. The starting cells are chosen at random.

## Example 1 - Random traversal of passages

We start with four imports.  There are no restrictions on the grid class.
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
```

We create a maze with circuits.  In this example, we simply link all the available edges.  Since there are 8 rows with 13 columns each:
```
        the number of cells:    v = 8 • 13 = 104 cells
                degree              number      product
                     2                   4            8
                     3     2•6 + 2•11 = 34          102
                     4         6 • 11 = 66          264
                        Sum:       v = 104     2e = 374
        the number of passages:                 e = 187

        the number of components:               k = 1

        Euler characteristic:   χ = e - v + k = 84
```
So we must break 84 circuits (or remove 84 suitably chosen passages) in order to end up wit a perfect maze.

Here is the starting maze:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> maze.link_all()
```

At this point we call the class method *BasicWallbuilder.on()*.  The default is to process the passages in random order.  So we only need to supply the maze.
```
>>> print(BasicWallbuilder.on(maze))
          maze algorithm (statistics)
                            visits       85
                     finder passes     2713
                           unlinks       84
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                   |               |
+   +---+---+---+   +   +---+---+   +   +---+---+---+
|   |   |       |   |   |       |   |   |           |
+---+   +   +   +---+   +   +   +---+   +---+   +   +
|           |               |   |           |   |   |
+   +---+   +---+   +---+---+   +---+   +   +   +   +
|   |           |           |       |   |       |   |
+   +   +---+---+---+---+---+---+   +---+---+---+   +
|   |               |           |       |           |
+   +---+---+---+---+   +---+---+   +   +---+   +---+
|       |   |           |   |       |       |       |
+   +---+   +   +   +---+   +   +   +---+   +---+   +
|   |           |   |           |   |       |       |
+   +---+---+---+   +   +---+---+   +---+   +   +   +
|                   |   |               |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that 84 unlinks were the precise number needed for a perfect maze.  More than 84 would disconnect the maze.  A traveral shows that there is exactly one component. Since (a) the number of passages is one shy of the number of cells and (b) the maze is connected, it follows that it is a tree (*i.e.* a perfect maze).

## Non-random traversal

The elements in hashed structured like sets and dictionaries in Python are not traversed randomly in any sense of the word.  If we traverse a dictionary in dictionary order, we can expect more order in the out.  (The details will depend on the actual implementation of certain Python modules, and, as such, the outcomes may vary depending on the Python version and other specifics.)

Using the imports above, we configure another rectangular maze to include all grid edes as passages:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> maze.link_all()
```

We call the *BasicWallbuilder.on()* method with the *shuffle* option turned off.  (This will in turn call the *CircuitFinder* class with *shuffle* turned off.  The position of the starting cell is random.)
```
>>> print(BasicWallbuilder.on(maze, shuffle=False))
          maze algorithm (statistics)
                            visits       85
                     finder passes     6802
                           unlinks       84
```
The number of calls to the *CircuitFinder* constructor is the same, but there are (in this case) about three times as many finder passes -- *CircuitFinder* did about three times as much work to locate the circuits.

And here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                               |                   |
+   +---+---+---+---+---+---+   +---+---+---+---+   +
|                           |                       |
+   +---+---+---+---+---+   +---+---+---+---+---+---+
|       |                   |                       |
+---+---+   +---+---+---+---+   +---+   +---+---+   +
|       |   |                   |       |           |
+---+   +   +   +   +---+   +---+   +---+   +---+---+
|       |   |   |   |       |   |       |   |       |
+   +---+   +   +---+---+---+   +---+   +   +   +   +
|       |   |               |   |       |   |   |   |
+---+   +   +---+---+---+   +   +   +   +   +   +   +
|       |                   |       |   |       |   |
+   +---+---+---+---+---+---+---+---+---+---+---+   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that this maze is far more ordered than its randomize counterpart above!