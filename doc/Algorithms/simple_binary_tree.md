# Simple Binary Tree

This is about as easy as the algorithms get...

## The Algorithm v1

Start with an empty rectangular grid with n cells.  In the northeast cell do nothing.  In the remaining cells in the north row, carve a passage east.  In the remainder of the east column, carve north.  In the remaining cells, toss a coin.  If it lands face up, carve north otherwise carve east.

## The Algorithm v2

```
Prerequisite: An empty rectangular grid with n cells

In each cell:
    if there is a way east:
        if there is a way north:
            toss a coin:
               (head) carve north
               (tail) carve east
        otherwise:
            carve east
    otherwise:
        if there is a way north:
            carve north
        otherwise:
            do nothing
```

See also: Jamis Buck, *Mazes for Programmers*, 2015 (Pragmatic Bookshelf), *pp* 6-8, 22-23, 249-250.

### Example 1

Let's create a maze using the algorithm:
```
    maze4c$ python
    Python 3.10.12
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(5, 8))
    4> from mazes.Algorithms.simple_binary_tree import BinaryTree
    5> print(BinaryTree.on(maze))
```

I ran the Python interpreter.  (You'll need Python 3.)  In the interpreter, I typed 5 commands.  The import lines (1, 2 and 4) bring in the important classes, namely OblongGrid, Maze and BinaryTree.  Line 3 creates the grid and places it under control of a Maze object.   Line 5 creates and prints a BinaryTree.Status object which just displays some information about maze carving.  But note that I never created a BinaryTree object -- instead I ran a class method called BinaryTree.on.  It carved the maze inside the Maze object (i.e. the value of the variable named "maze".

Here are the statistics:
```
          Simple Binary Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
```
My maze has 40 cells (since five rows by eight columns yields forty cells -- see line 3 above).  The algorithm carved 39 passage in some combination of two directions (east and north).  The simulation used a fair coin (bias 0.5 means about half the coin tosses should be heads.

To see the result, I can just use Python's print command.

```
    6> print(maze)
    +---+---+---+---+---+---+---+---+
    |                               |
    +---+---+---+   +---+---+---+   +
    |               |               |
    +   +   +   +---+---+---+   +   +
    |   |   |   |               |   |
    +---+   +---+---+---+   +   +   +
    |       |               |   |   |
    +---+   +   +---+   +---+---+   +
    |       |   |       |           |
    +---+---+---+---+---+---+---+---+
```

### Example 2

Suppose I replace east by south and north by west, but use a coin which shows a head about 75% of the time?  No problem.  I'm still in the Python interpreter, so I don't need to retype the imports:

```
    7> maze = Maze(OblongGrid(5, 8))
    8> print(BinaryTree.on(maze, onward="south", upward="west", bias=3/4))
          Simple Binary Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  south
                            upward  west
                              bias        0.7500
    9> print(maze)
    +---+---+---+---+---+---+---+---+
    |                   |       |   |
    +   +---+---+---+---+   +---+   +
    |           |   |               |
    +   +---+---+   +   +---+---+---+
    |       |       |           |   |
    +   +---+   +---+   +---+---+   +
    |                           |   |
    +   +---+---+---+---+---+---+   +
    |                               |
    +---+---+---+---+---+---+---+---+
```

In line 7, I create a new grid and embed it in a Maze object.  In line 8, I run the algorithm and display some statistics.  In line 9, I display the maze.  It appears to have favored westbound passages (the "upward" or "heads" direction.
Notice that the long northward corridor to the east and the long eastward corridor to the north were replaced, respectively, by corridors along the south and west walls.

***

## Evaluating the Results

### 1) Is it a tree?

Except when noted, our goal is to create "perfect mazes" (or "spanning trees").  In any algorithm that creates a spanning tree, we want the resulting maze to be a tree.  There are a number of ways to determine whether a maze is a tree.  Usually it's a matter of checking just two conditions.  The definition of a tree is that it is a connected graph with no circuits.  But it turns out that these two are equivalent to checking that the graph (or undirected maze) is connected and that the number of edges (two-way passages in mazes) is one less than the number of vertices (or cells).

In both examples, there were 5x8=40 cells and 39 passages.  And the algorithm itself actually carves exactly one passage from each cell except for one of the four corner cells (the northeast corner if we use the default head/north, tail/east setup).  So we have the correct number of vertices.

To check connectedness, we need to be sure that there is a path between every pair of vertices.  But there are simpler ways of verifying that condition.  One way is to choose a cell as the root and show that there is a path from ever cell to root.  For this algorithm the convenient cell is the magic corner -- the northeast corner in the description of the algorithm (in Example 2: the southwest corner).  Suppose the treasure is in the northeast corner and the archaeologist is in a random cell in the maze, equipped with a compass.  Is there a passage east?  Yes -- go east.  No -- if you can, go north.  Nowhere to go but south and west?  You have arrived... put away the compass and dig for the treasure.

### Is it a binary tree?

#### The hard way: Breadth-first search

This algorithm specifically says "*binary tree*".  One way of determining whether a graph is a binary tree is to find a root cell with one or two neighbors, and work from there using *breadth-first search*...

How does it work: place a marker in the chosen root cell and examine the neighbors of the chosen root cell.  If either one has more than *three*(!)* neighbors, then it's *not* a binary tree.  (Why three?  One has been marked -- the parent of this cell.  And these cells are allowed to have two children.)

So in each child of the current cell, we check make sure that:

* there are at most three neighbors; and
* exactly one of these is marked -- the parent of the current cell;

If either condition fails, it's not a binary tree.  The algorithm itself guarantees that each cell we visit has a marked neighbor, so if the second condition fails, we have two paths to root and thus a circuit.  (We already indirectly verified that there were no circuits.)   We place a marker in the cell and if the current cell's parent has another child, we check that one.  Once we have finished checking the children of the parent cell, we check the children...

It's systematic, but it's slow.  And since we already know that the maze is a tree, that second condition is is unnecessary.

#### A easier way

It turns out that, if we already know that it is a tree, then there are two conditions to check:

* there is a cell with one or two neighbors; and
* there are no cells with more than three neighbors.

But if every cell has three or more neighbors, there will be too many passages.  (If n is the number of cells Euler's lemma tells us that we would have at least 1.5n passages, and that's obviously more than n-1.)

So in fact, to check that a graph is a binary tree, we just need to verify that it's a tree and that none of its cells has more than three neighbors.  If we need a rooted binary tree, we can pick any cell in the tree that has fewer than three neighbors.

#### Result

The algorithm itself guarantees that no cell has more than three neighbors.  We might have passages from the west and south, but we won't have passages both north and east from any given cell.  If we want a rooted binary tree, the obvious candidate is the northeast cell since it has just two neighbors.  So yes, it's a binary tree and we even have an excellent choice for a root cell.

For Example 2, symmetry tells us to choose the southwest corner as a root for a rooted binary tree.

***

## Is this the only way to produce binary spanning trees?

No.  The growing tree algorithms and Kruskal's algorithm can both be adapted to produce binary spanning trees.  But there are some grids that don't admit binary spanning trees.

This just happens to be about as simple as spanning tree algorithms get, so I think it's reasonably fair to say that this is a simple binary tree algorithm.
