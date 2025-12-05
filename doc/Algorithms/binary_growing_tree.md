# Binary (and other arity) spanning trees

## Contents

* Introduction
* Section 1. Simple binary trees
* Section 2. Greedy binary growing trees
* Section 3. Deferred reward (or "fair") binary growing trees
* Appendices
    + A. Changing the arity
    + B. Failures
    + C. Open questions

## INTRODUCTION

### Definitions

A *rooted tree* can be defined recursively as graph G=(V,E) containing a fixed node *r* in V (called the *root*), subject to the following conditions:

1. The root node *r* is the totality of nodes in the first generation; let V(1)={*r*}.
2. Let V(*n*) be the set of nodes in generation *n*>1; then for each node *v* in V(*n*), *v* has exactly one neighbor in V(*n*-1), called the *parent* of *v*.
3. The set of nodes V is the union of the generation sets V(1), ..., V(k)
4. The generation sets are pairwise disjoint.

If node *u* is *the* parent of node *v*, then *v* is a *child* of *u*, and conversely.

If the *arity* of a rooted tree is *n*, then every node in the tree has at most *n* children.  Conversely, if every node in a rooted tree has at most *n* children, then the rooted tree has arity *n*.

Note that the class of rooted trees ot arity *n*+1 includes all rooted trees of arity *n*.  Note also that the root of a rooted tree of arity *n* has degree at most *n*, while the remaining nodes have degree at least 1 and at most n+1.

A *rooted binary tree* is a rooted tree of arity 2.

In a rooted binary tree, the parent nodes form a path from any cell to the root node.

### Algorithms for rooted binary trees (arity=2)

* Simple binary tree
* Binary growing tree (greedy version)
* Binary growing tree (deferred reward)

Modules discussed are:

* *mazes.Algorithms.simple\_binary\_tree* (class *BinaryTree*)
* *mazes.Algorithms.binary\_growing\_tree1* (class *BinaryGrowingTree*)
* *mazes.Algorithms.binary\_growing\_tree2* (class *BinaryGrowingTree*)

We will deal with other arities in the appendix.

## Section 1. Simple binary trees

The simple binary tree algorithm produces rooted binary trees with a root in the northeast corner (or other chosen corner).  Using the default, the parent of any node is its linked neighbor either the east or north.

We can, in fact, choose any node of degree 1 or 2 as the root, but defining the parent relationship is more complicated.

In this example, we produce a simple binary tree whose "natural root" is the southwest corner:

### Example 1.1 a south-west simple binary tree
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree
>>> maze = Maze(OblongGrid(5,8))
>>> print(BinaryTree.on(maze, onward="south", upward="west")); print(maze)
          Simple Binary Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  south
                            upward  west
                              bias        0.5000
+---+---+---+---+---+---+---+---+
|   |   |   |           |   |   |
+   +   +   +   +---+---+   +   +
|   |   |               |   |   |
+   +   +   +---+---+---+   +   +
|       |   |               |   |
+   +---+   +   +---+---+---+   +
|   |   |       |   |       |   |
+   +   +   +---+   +   +---+   +
|                               |
+---+---+---+---+---+---+---+---+
```
Since we used a fair coin ("*bias=0.5*"), we could just as easily have said "*onward='west', upward='south'*".

Starting at any cell and stepping either south or west through a passage leads us to the root in the southwest corner.

## Section 2. Greedy binary growing trees

### Good news, bad news

The simple binary tree algorithm only works on a rectangular grid, though it can be adapted to work on some other grids.  We would like an algorithm that is more general.  There is some good news and some bad news.

First some bad news: There are connected grids which do not admit any binary spanning trees.  Here is the simplest example:
```
            +---+
            |   |
        +---+---+---+
        |   |   |   |
        +---+---+---+
            |   |
            +---+
```
This grid is an example of a graph called a 4-star.  It consists of a central node with four neighbors (the "points") and no other edges.  The only spanning tree of a star is the star itself, so stars with four or more points do not have binary spanning trees.

(With a 3-star, any of the three points can be taken as root, so a 4-star is the smallest counterexample.)

Now for the good news: Most of the grids typically used in maze generation will have binary spanning trees.

But there is a bit of bad news: Even if the grid has a binary spanning tree, the algorithm might not find one.

And a bit of good news: Most of the time in practice, the algorithm succeeds in finding one.

### Greedy vs deferred reward

The difference between the greedy algorithm and the deferred reward is significant.  The greedy algorithm takes as many children as it can from the unvisited neighbors, while the deferred reward algorithm takes one child at a time.  In the greedy algorithm, a cell never has a grandchild before its second child. In the deferred reward algorithm, whether this is possible depends on the queue discipline. grandchild before its second child.

Without further ado, we give examples.

### Example 2.1 Greedy with stack

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.binary_growing_tree1 import BinaryGrowingTree
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze)); print(maze)
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (3, 2)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |   |   |   |   |           |       |
+   +---+   +   +   +   +   +   +   +   +---+   +---+
|   |                   |           |       |       |
+   +---+---+---+---+   +   +---+   +   +---+   +---+
|       |   |   |   |       |       |               |
+   +---+   +   +   +   +---+---+   +---+   +---+   +
|       |           |   |               |   |       |
+   +---+   +---+   +---+---+   +---+---+---+   +   +
|       | S     |       |               |       |   |
+   +   +---+---+   +---+---+---+   +---+   +   +---+
|   |           |           |   |       |   |   |   |
+---+   +   +---+   +   +---+   +   +---+   +---+   +
|   |   |       |   |       |           |           |
+   +---+   +   +---+   +---+   +---+---+   +   +---+
|           |   |                   |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

There are a total of 8 times 13 or 104 cells.  All cells were visited, so this is a binary spanning tree (or more strictly: a spanning binary tree).  All cells have at least one wall, so all cells have degree less than 4.  Hence this is a binary tree.  We can take any cell of degree 1 or 2 as root, but the natural choice is the cell in row 3 (counting the bottom row as row 0) column 2, here labelled "S".  Note that this is a degree 2 cell.  It has no parent, and two of its neighbors were adopted as children before returning control to the queue.

Cells that were popped early tended to adopt two children; those which were late tended to have fewer unvisited neighbors.  That tell-tale indicator of depth-first search, a long path from the starting cell, is in evidence here.

### Example 2.2 Greedy with stack, no shuffling

```
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, shuffle=False)); print(maze)
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (3, 1)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |               |               |       |
+   +   +---+   +---+   +---+   +---+   +---+   +---+
|   |       |       |       |       |       |       |
+   +   +---+   +---+   +---+   +---+   +---+   +---+
|   |       |       |       |       |       |       |
+   +   +---+   +---+   +---+   +---+   +---+   +---+
|   |       |       |       |       |       |       |
+   +   +---+   +---+   +---+   +---+   +---+   +---+
|   | S     |       |       |       |       |       |
+   +---+---+   +---+   +---+   +---+   +---+   +---+
|       |           |       |       |       |       |
+   +---+   +---+---+   +---+   +---+   +---+   +---+
|       |       |           |       |       |       |
+   +---+   +---+   +---+---+   +---+   +---+   +---+
|               |                   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The greediness is in evidence here.  Before returning control to the stack, a cell attempted to adopt two cells as children.  The starting cell (an orphan) has degree 2. Most of the remaining cells have degree 3 (one parent, two children).

### Example 2.3 Greedy with queue

```
>>> from mazes.Queues.queue import Queue
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, QueueType=Queue)); print(maze)
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (2, 2)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |                       |
+   +   +   +   +   +   +   +   +---+---+---+---+---+
|   |   |       |   |   |   |                       |
+   +   +   +---+   +   +   +   +---+---+---+---+---+
|   |   |       |                                   |
+   +   +   +---+   +---+---+---+---+---+---+---+---+
|   |   |                                           |
+   +   +   +   +---+---+---+---+---+---+---+---+---+
|           |       |   |       |                   |
+---+---+   +   +---+   +   +---+   +---+---+---+---+
|       | S |   |       |       |                   |
+   +---+   +---+---+   +   +---+   +---+---+---+---+
|                                                   |
+---+   +---+   +   +---+---+   +---+---+---+---+---+
|       |       |           |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The starting cell has no parent and two children.  Near the starting cell, there is considerable chaos that results from the limits on the number of children.  As we move away, the relationship between breadth-first search and grid distance takes precedence.

### Example 2.4 Greedy with split stack

```
>>> from mazes.Queues.split_stack import SplitStack
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, QueueType=SplitStack)); print(maze)
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (2, 3)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |       |       |                               |
+   +   +---+---+   +   +---+---+---+---+---+---+---+
|   |           |   |       |   |   |   |   |   |   |
+   +---+   +---+   +   +---+   +   +   +   +   +   +
|   |   |       |   |       |                       |
+   +   +   +---+   +   +---+   +---+---+---+---+---+
|                           |                       |
+---+---+---+   +---+---+---+   +   +---+---+---+---+
|           |                   |       |   |   |   |
+---+   +   +   +   +   +   +   +---+---+   +   +   +
|   |   |     S |   |   |   |                       |
+   +---+   +---+   +   +---+   +   +   +---+---+---+
|               |   |       |   |   |               |
+   +   +---+   +   +   +   +---+---+   +   +---+---+
|   |       |   |   |   |           |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
A split stack with a split length of 10 (the default) was used above.  Contrast the result with the same starting cell and a split length of 1.

```
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, maze.grid[2,3],
          QueueType=SplitStack, qkwargs={"target_length":1}))
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (2, 3)
                             cells      104
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |               |       |                   |
+---+   +   +---+   +---+---+   +   +---+---+---+---+
|   |           |       |   |                       |
+   +   +---+---+   +   +   +   +---+   +   +   +   +
|           |       |   |           |   |   |   |   |
+   +---+---+---+   +---+   +---+---+---+---+   +   +
|       |           |       |   |   |           |   |
+   +---+---+---+   +---+   +   +   +---+   +   +   +
|       |   |       |               |       |   |   |
+   +---+   +---+---+---+---+---+   +---+   +---+   +
|       |     S |   |   |   |   |       |   |       |
+   +---+   +   +   +   +   +   +   +---+---+   +   +
|   |       |           |           |           |   |
+   +---+   +   +---+   +   +---+   +   +---+   +---+
|           |   |               |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 2.5 Greedy with random queue

```
>>> from mazes.Queues.random_queue import RandomQueue
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, maze.grid[4,6], QueueType=RandomQueue)); print(maze)
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (4, 6)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |           |       |               |
+   +   +   +   +---+---+   +   +---+---+   +---+---+
|                       |   |       |       |   |   |
+---+---+---+---+   +   +   +   +---+---+   +   +   +
|   |   |   |       |       |           |   |       |
+   +   +   +---+---+   +---+   +---+---+   +   +---+
|           |           | S                         |
+   +---+   +---+   +   +   +---+---+---+---+---+   +
|   |           |   |                           |   |
+---+---+---+   +---+   +---+   +   +---+---+---+---+
|                       |       |                   |
+---+---+---+---+---+---+---+   +   +---+---+---+---+
|                               |                   |
+   +---+   +   +---+---+---+   +   +   +---+   +---+
|   |       |   |               |   |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Section 3. Deferred reward (or "fair") binary growing trees

In module *mazes.Algorithms.binary_growing_tree2*, the cell in the front of the queue takes control for just one iteration in its neighborhood.  Whatever happens to be in front gains control in the next visit.  This increases the number of visits.  Apart from a negligible amount of additional overhead, the time complexity is the same as for the greedy algorithm.  The results will have different characteristics.

### Example 3.1 Deferred with stack

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.binary_growing_tree2 import BinaryGrowingTree
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze)); print(maze)
          Binary Growing Tree (statistics)
                            visits      468
                        start cell  (7, 4)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       | S |                       |       |
+   +   +   +   +   +---+---+---+   +---+   +   +   +
|   |   |   |       |           |       |   |   |   |
+---+   +   +---+---+   +---+   +---+   +   +   +   +
|       |   |           |   |           |   |   |   |
+   +   +   +---+   +---+   +---+---+---+   +---+   +
|   |   |   |       |       |           |       |   |
+   +---+   +   +---+   +   +   +---+   +---+   +   +
|       |       |   |   |       |       |       |   |
+   +   +---+---+   +   +---+---+   +   +   +---+   +
|   |               |       |       |   |       |   |
+   +---+   +---+---+---+   +   +   +---+---+   +   +
|   |   |           |       |   |   |       |   |   |
+   +   +---+---+   +   +---+   +---+   +   +   +   +
|               |           |           |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Note that the starting cell (root) has degree 1.  As soon as the root cell had a child, that child was placed at the top of the stack.  It take 12 steps from root to arrive at a cell which has more than 1 child.  In the greedy version, the root cell would have two children, and there would be more branching in the first few steps from root.

As with unrestricted randomized DFS, we get a long chain with few branches.  Restricting the arity to 2 guarantees that the maze will have no degree 4 nodes.  In practice, unrestricted DFS gives very few degree 4 nodes.  The greedy binary growing tree algorithm favors degree 3 nodes (one parent, two children).

### Example 3.2 Deferred with stack, no shuffling

```
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, shuffle=False)); print(maze)
          Binary Growing Tree (statistics)
                            visits      478
                        start cell  (2, 8)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +---+---+---+---+---+---+---+---+---+---+---+   +
|                                               |   |
+---+---+---+---+---+---+---+---+---+---+---+   +   +
|                                               |   |
+   +---+---+---+---+---+---+---+---+---+---+---+   +
|                                               |   |
+---+---+---+---+---+---+---+---+---+---+---+   +   +
|                                               |   |
+   +---+---+---+---+---+---+---+---+---+---+---+   +
|                               | S                 |
+---+---+---+---+---+---+---+   +---+---+---+---+---+
|                           |                       |
+   +---+---+---+---+---+   +---+---+---+---+---+   +
|                       |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The result with no shuffling is a single chain,  Unrestricted DFS gives the same result for the same starting cell (subject to differences in the implementation of Python dictionaries).  Compare this to Example 2.2 for the greedy binary growing tree -- in that result, most of the nodes were degree 3 because children were allocated before returning control to the queue.

### Example 3.3 Deferred with queue

```
>>> from mazes.Queues.queue import Queue
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, QueueType=Queue)); print(maze)
          Binary Growing Tree (statistics)
                            visits      456
                        start cell  (5, 3)
                             cells      104
                          passages      103
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |           |                                   |
+   +---+---+   +   +---+---+---+---+---+---+---+---+
|               |                                   |
+---+   +   +---+   +---+---+---+---+---+---+---+---+
|       |     S     |   |                           |
+---+   +   +---+   +   +   +---+---+---+---+---+---+
|       |       |                                   |
+---+---+   +---+   +---+---+---+---+---+---+---+---+
|   |   |       |                                   |
+   +   +   +   +   +   +   +---+---+---+---+---+---+
|           |   |   |   |                           |
+---+---+   +   +   +   +   +---+---+---+---+---+---+
|           |   |   |   |                           |
+   +   +   +   +   +   +   +---+---+---+---+---+---+
|   |   |   |   |   |   |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Results here are essentially the same as the greedy case.  The root cell retains control because it is already in the front of the queue.  In both cases, the first child will be in the front of the queue when the root cell is exhausted.  Unrestricted breadth-first search will differ: the degree of the root cell would be the same as the number of grid neighbors.

### Example 3.4 Deferred with split stack

Compare this example with Example 2.4:
```
>>> from mazes.Queues.split_stack import SplitStack
>>> from mazes.Queues.split_stack import SplitStack
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, maze.grid[2,3],
          QueueType=SplitStack, qkwargs={"target_length":1}))
          Binary Growing Tree (statistics)
                            visits      446
                        start cell  (2, 3)
                             cells      104
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |                               |       |
+   +---+---+---+   +---+   +---+---+   +---+   +---+
|                   |               |       |   |   |
+   +   +   +   +   +---+---+   +---+   +---+   +   +
|   |   |   |   |   |       |       |       |       |
+   +---+---+---+---+   +---+   +---+   +---+---+   +
|                           |       |       |       |
+   +   +   +---+   +---+---+   +---+   +---+---+   +
|   |   |   |   |       |   |       |               |
+---+---+---+   +   +---+   +   +---+   +   +   +   +
|             S |   |   |           |   |   |   |   |
+---+   +   +---+---+   +   +---+---+---+---+---+   +
|       |   |   |   |           |                   |
+---+   +---+   +   +   +---+---+---+   +   +   +   +
|                           |           |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 3.5 Deferred with random queue

For comparison with Example 2.5:
```
>>> from mazes.Queues.random_queue import RandomQueue
>>> maze = Maze(OblongGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, maze.grid[4,6],
          QueueType=RandomQueue))
          Binary Growing Tree (statistics)
                            visits      443
                        start cell  (4, 6)
                             cells      104
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |                   |       |   |       |       |
+   +---+---+   +---+---+---+   +   +   +---+   +---+
|                   |       |   |   |               |
+   +   +---+---+   +   +---+   +   +   +   +---+---+
|   |       |                           |       |   |
+---+   +   +   +---+---+   +---+---+   +---+---+   +
|       |   |   |   |   | S         |               |
+---+   +   +---+   +   +---+   +   +---+   +---+---+
|       |   |   |               |       |   |       |
+   +   +   +   +---+---+---+   +---+---+---+---+   +
|   |   |       |                               |   |
+---+   +   +---+   +---+---+---+   +   +---+---+   +
|       |   |           |           |               |
+   +   +   +---+---+---+   +   +   +---+---+---+   +
|   |   |   |               |   |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

## APPENDIX A: Changing the arity

The binary growing tree modules can produce mazes with arities other than 2.  For our example we will produce a ternary tree (arity=3).  But we have a small problem:

**Lemma A.1**:  Every spanning tree on a Von Neumann (N/S/E/W) rectangular grid has arity 3.

**Proof**:  Since every cell has just four neighbors, the degree of every cell must be at most 4.  If the arity is not 3, then the root cell must have degree 4.  But a corner cell has maximum degree 2, so we can take any corner a the root.  Since the root of the tree has degree 2 and every cell has degree at most 4, the spanning tree has arity 3.
```
Another way to establish a contradiction is to use a counting argument to establish the following useful lemma:

**Lemma A.2**:  Every tree with at least two cells has at least one cell of degree 1.

**Proof**:  Let *T* be a tree with at least two cells and let *v* be the number of cells in the tree.  Then *v*-1 is the number of passages.  Suppose *T* has no cells of degree 1.  There are two possibilities:
1.  *T* has a cell with degree 0.  But, since *T* has two cell, this implies that *T* is not connected.
2.  Every cell in *T* has degree at least 2.  Then the sum of the degrees of the cells is at least 2*v*.  *Euler's Lemma* tells us that the sum of the degrees of the cells in an undirected maze is twice the number of passages, so the sum for a tree is exactly 2(*v*-1). But:
```
            2v > 2v - 2 = 2(v-1).
```
In either case, we have a contradiction.

Using *Lemma A.2*, it follows that if the maximum degree of a cell in a tree with two vertices is *n*, then it has arity *n*.  (We can take a degree 1 cell as the root cell.)  If the tree has just one vertex, that vertes is degree 0, so the tree must have arity 1.

As a resullt, to illustrate our ternary tree, we need to use a grid with some cells of degree 5 or more.  We will use a Moore grid (with neighbors on the diagonals as well as in row and column).

### Example A.1 Ternary growing tree on a Moore grid

We will use the greedy growing tree algorithm with arity 3 and a stack.  Use of the greedy algorithm insures that the root is degree 3 and that we have some degree 4 cells early in sequence.  All cells should be of degree 1, 2, 3 or 4.

We start with the imports:
```
$ python
>>> from mazes.Grids.oblong8 import MooreGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.binary_growing_tree1 import BinaryGrowingTree
```

We create our empty maze and use it to carve a ternary tree (*arity*=3). We will specify a root cell in the center of the maze and verify that it has degree 3.
```
>>> maze = Maze(MooreGrid(8,13))
>>> print(BinaryGrowingTree.on(maze, start_cell=maze.grid[4,6], arity=3))
          Binary Growing Tree (statistics)
                            visits      104
                        start cell  (4, 6)
                             cells      104
                          passages      103
```
We have the right number of passages, so the was successful in finding a spanning tree.

We programmatically label the root cell and display the maze:
```
>>> maze.grid[4,6].label="S"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |                               |   |   |
+---\   +---\---/---/---/---/---/---/---/   \   /---+
|   |   |       |   |   |   |   |   |   |   |   |   |
+   /---+---/---+---+---+---\---+---+---+---+---\   +
|   |       |           |   |           |   |       |
+   +---+   X---+---+---+   +---+---+---+---\---/---+
|   |       |   |   |   | S |   |   |   |       |   |
+---\---/---+---+---X---/   +   /---/---+---+---\   +
|       |   |           |   |           |   |   |   |
+   +   +   +---+   +   +---/---+---\---/---+---\   +
|   |   |   |       |   |       |   |       |   |   |
+   \---+   +---+   \---+---\---/---/---+---/---/---+
|   |   |       |   |       |   |       |           |
+   \---/---\---\---+   \---/---\---\---/---\---\---+
|   |       |   |   |   |       |   |       |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The root cell has passages leading north, south, and southwest.  So it indeed has degree 3.  Its southwest child has three children: one each to the west, south, and northwest.  The north and south children of root are both childless, so the southwest child of root was the first child.  Note that its west child must be the first grandchild of root -- it has three children while the other two grandchildren of root are childless.  There is a long path emanating from root, a clear mark of depth-first search.

Let's check the degree sequence.  We shouldn't have any cells with degree greater than 4, so a list with five entries will suffice.  (Indexing of lists in Python starts with 0, so we need a slot for degree 0.
```
>>> degseq = [0,0,0,0,0]
>>> for cell in maze.grid:
...     degree = len(list(cell.passages))
...     degseq[degree] += 1
...
```

Here is the degree sequence
```
>>> print(degseq)
[0, 58, 9, 18, 19]
```
Quite a few cells of degree 4!

Let's verify that each cell was counted:
```
>>> print(sum(degseq))
104
```
All cells were counted!

Now let's verify Euler's Lemma for this maze:
```
>>> sum(i*degseq[i] for i in range(5))/2
103.0
```
The weighted sum does indeed give us twice the number of passages.

This maze is a spanning termary tree on the underlying grid.

## APPENDIX B: Failures

One failure to complete a perfect maze on the rectangular 4-grid did occur in the 3 December 2025 statistical experiments, but the raw data (*i.e.* the maze) is too big to display and is, in any case, not saved.

Cases where either algorithm as implemented fails to produce a spanning tree on a rectangular 4-grid seem to be exceedingly rare.  But after a brute force trial where I failed to produce a 6×6 after 10,000 tries, I did finally manage to produce an 8×8 example after just 7839.  Here is the script -- first the imports:

### Example B.1 a failure that can be fixed
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.binary_growing_tree1 import BinaryGrowingTree
>>> from mazes.Queues.split_queue import SplitQueue
```
In the 3 December 2025 statistics, the greedier algorithm failed in one instance using a split queue with a target length of 1.  So that seemed to be a good place to search.

Here I failed to fail on 6×6 after 10,000 tries:
```
>>> for _ in range(10000):
...     maze = Maze(OblongGrid(6, 6))
...     status = BinaryGrowingTree.on(maze, QueueType=SplitQueue, qargs=(1,))
...     if status["passages"] != 35:
...         print(status)
...         break
...
>>>
```
Note that I would have printed the status if fewer than 35 passages were carved.

And I succeeded to fail on 8×8:
```
>>> for _ in range(10000):
...     maze = Maze(OblongGrid(8, 8))
...     status = BinaryGrowingTree.on(maze, QueueType=SplitQueue, qargs=(1,))
...     if status["passages"] != 63:
...         print(status)
...         break
...
          Binary Growing Tree (statistics)
                            visits       63
                        start cell  (3, 5)
                             cells       63
                          passages       62
>>> print(maze)
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |       |   |
+   +   +   +   +   +   +---+   +
|               |       |       |
+---+---+---+   +---+   +---+   +
|                               |
+---+---+---+---+   +---+   +---+
|           |       |   |       |
+---+---+   +---+   +---+   +   +
|       |       |   |       |   |
+---+   +   +---+---+   +   +---+
|                       |       |
+---+---+---+   +   +   +   +---+
|               |   |   |       |
+---+   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```
And to show that this was after 7839 failed failures:
```
>>> print(_)
7840
```
Let's take a closer look at this maze.  First note that the failure cell is just above the starting cell.  If we focus on the cells that surround the failure cell, we can obtain a 4x4 configuration which forces a failure:
```
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |       |   |
+   +   +   +   +   +   +---+   +
|               |     5 |       |
+---+---+---+   +---+   +---+   +
|             6   5   4   3   4 |
+---+---+---+---+   +---+   +---+
|           | 7   6 | F | 2   3 |
+---+---+   +---+   +---+   +   +
|       |       | 7 | S   1 |   |
+---+   +   +---+---+   +   +---+
|                     1 |       |
+---+---+---+   +   +   +   +---+
|               |   |   |       |
+---+   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```
Here is the 5x5 configuration
```
            +---+
            x 3 x               Legend:
        + x +   + x +              S = start cell (root)
        x 1   2   3 x              F = orphan cell
    + x +   +---+   + x +          1 = first generation children
    | 1   S | F | 4   5 |          2 = second generation children
    + x +---+---+   + x +          3, 4, 5, 6, 7 etc.
        x 7   6   5 x              x = don't care (wall or passage
        + x +   + x +
        x   x 7 x
            +---+
```
At this point each of the four neighbors of the failure cell has two children.  Except for the starting cell each also has one parent.  Can you see the fix?

<center>**SPOILER**</center>

### Example B.2 Fixing the failure

We can fix this by carving a wall from the failure cell to the starting cell.  In the 5x5 configuration:
```
            +---+
            x 3 x               Legend:
        + x +   + x +              S = original start cell
        x 1   2   3 x              F = original orphan cell (root)
    + x +   +---+   + x +          1 = first generation children
    | 1   S   F | 4   5 |          2 = second generation children
    + x +---+---+   + x +          3, 4, 5, 6, 7 etc.
        x 7   6   5 x              x = don't care (wall or passage
        + x +   + x +
        x   x 7 x
            +---+
```
And here is the *perfect* binary maze -- a spanning *binary* tree on the 8x8 Von Neumann rectangular grid:
```
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |       |   |
+   +   +   +   +   +   +---+   +
|               |       |       |
+---+---+---+   +---+   +---+   +
|                               |
+---+---+---+---+   +---+   +---+
|           |     S   F |       |
+---+---+   +---+   +---+   +   +
|       |       |   |       |   |
+---+   +   +---+---+   +   +---+
|                       |       |
+---+---+---+   +   +   +   +---+
|               |   |   |       |
+---+   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```

## APPENDIX C: Open questions

* What kinds of configurations lead to failure cells?  Note that the example could be extended to an example in which several failure cells are surrounded, for example:
```
            +---+---+---+---+---+---+
            |         9 | 8         |   Legend:
            +---+---+   +   +---+---+     S = the start cell
            |     9   8   7   6     |     1, 2, 3, ... = generations of
            +---+---+---+---+---+---+             children
            | 1   S | F | F | 5   6 |     F = failure cells
            +---+---+---+---+---+---+     space = cells that can be
            | 2   1   2   3   4     |             ignored
            +---+---+   +   +---+---+
            |         3   4         |
            +---+---+---+---+---+---+
```
Connecting the blank cells *binarily* in a different way does not structurally change the configuration.  For example, this is essentially the same failure:
```
            +---+---+---+---+---+---+
            |         9 | 8 |       |   Legend:
            +   +---+   +   +   +---+     S = the start cell
            |   | 9   8   7   6     |     1, 2, 3, ... = generations of
            +---+---+---+---+---+---+             children
            | 1   S | F | F | 5   6 |     F = failure cells
            +---+---+---+---+---+   +     space = cells that can be
            | 2   1   2   3   4 |   |             ignored
            +   +---+   +   +   +---+
            |       | 3   4 |       |
            +---+---+---+---+---+---+
```
And in a weaker sense, both of these conditions reduce to the failure described in Example B.1.
* Is the starting cell always adjacent to a failure cell?

