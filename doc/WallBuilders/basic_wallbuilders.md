# basic wallbuilders (EXAMPLES)

A more leisurely introduction is found in document *doc/basic\_wallbuilder.md*.  (Note the difference in name: singular *vs* plural.)

Contents:

*  Introduction
*  Section 1. Depth-first search
*  Section 2. Breadth-first search
*  Section 3. Wallbuilding using an edge-based priority queue
*  Section 4. Wallbuilding using a vertex-based priority queue

## Introduction

All the wallbuilders described here work in essentially the same way:

```
    procedure Wallbuilder(maze M):
        loop:
            find a passage e contained in a circuit in maze M:
            if found:
                delete passage e from maze M
            otherwise:
                exit the loop
```

The implementation of the algorithm used to find the edge strongly influences the resulting maze.

## Section 1. Depth-first search

Depth-first search is a practical method for finding an edge contained in a circuit.  It has the added advantage that the entire circuit is contained in the stack.  If implemented iteratively, the stack can be inspected to reveal the entire circuit.

### Example 1.1  Finding a circuit using depth-first search

**Warning:** We will go into considerable detail here.

One way to find an edge that is contained in a circuit is to traverse the cells in the maze without using any edge more than once.  if we arrive at a cell twice, then the most recent edge belongs to at least one circuit,  Let's look at a depth-first search implementation.  First let's create a maze and add a couple of circuits...

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(8, 13)); print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       38
                             cells      104
                          passages      103
                 paths constructed       38
                     cells visited      311
                          circuits       70
                    markers placed      203
                   markers removed      100
                     starting cell  (0, 1)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
|       |   |           |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
|           |       |   |   |   |   |       |   |   |
+---+---+   +---+   +---+   +---+   +---+---+   +   +
|               |   |       |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   |       |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
To create at least two circuits, we need to knock down two walls:
```
>>> cell1 = maze.grid[0,8]; edge1 = maze.link(cell1, cell1.east)
>>> cell2 = maze.grid[4,5]; edge1 = maze.link(cell2, cell2.north)
>>> cell1.label = "1"; cell2.label = "2"; print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
|       |   |           |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
|           |       |   |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|               |   | 2     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   |       |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Now we ask for some help from a circuit locator.  We need to use the status, so we will save it before displaying the run statistics:
```
>>> status = CircuitFinder.on(maze); print(status)
          DFS Circuit Locator (statistics)
                            visits       35
                     queuing class  Stack
                           shuffle        1
                  components found        1
               components finished        0
                     cells visited       22
                        start cell  (4, 3)
              maximum queue length       20
                           circuit  ((5, 4), (6, 4))
```
The status object keeps track of the result, a passage along with both of its endpoints.  We will label these, and for reference, we will also label the cell that was randomly chosen as a starting point:
```
>>> cell3, join, cell4 = status.result; cell3.label = "3"; cell4.label = "4"
>>> start = maze.grid[4,3]; start.label = "0"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
|       |   |     4     |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
|           |     3 |   |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|             0 |   | 2     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   |       |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The search-based circuit locators all have two methods for analyzing the queue at the point where the edge was found.  The first of these is a property called:
```
        CircuitFinder,post_mortem_dump
```
It's output is a mess, but it's intended for use by programmers.  I've edited the mess:
```
>>> status.post_mortem_dump
((<Edge object>, <Cell object>), (<Edge object>, <Cell object>), ...,
  (None, <Cell object>))
```
Let's look at the indices of the cells in first and the last entries:
```
>>> dump = status.post_mortem_dump
>>> f"first cell={dump[0][1].index}, last cell={dump[-1][1].index}"
'first cell=(5, 4), last cell=(4, 3)'
```
The first cell, *i.e.* the cell at top of the stack, is a cell in the edge that was found.  That's the cell labelled "3" above.  The last cell, the cell at the bottom of the stack, is the starting cell labelled "0" in the display above.

The stack is actually a trail which leads from the starting cell to the cell labelled "4", the other endpoint of the edge that was found.  Let's label the trail.  The default label here is "Q" for "queue", but since we have a stack, let's instead use another symbol... maybe a lower case "o" as it makes a nice marker.  The method to use is *CircuitFinder.label\_pmqueue*:
```
>>> status.label_pmqueue(label="o")
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     o   o   o |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
| o   o |   | o   o   o |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
| o   o   o |     o | o |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|         o   o | o | o     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   | o   o |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Now let's restore the other markers:
```
>>> start.label = "0"
>>> cell2.label = "2"; cell3.label = "3"; cell4.label = "4"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     o   o   o |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
| o   o |   | o   4   o |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
| o   o   o |     3 | o |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|         o   0 | o | 2     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   | o   o |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We have a trail which leads from the starting cell (labelled with a zero), and into a circuit which included the wall we knocked down (label: 2), and the ending edge (labels: 3 and 4).  It should be clear that the circuit consists of eight cells.  The trail proceeds clockwise around the circuit since cell 3 was the last cell processed before the detection of the circuit when cell 4 was reached a second time.

We can see the circuit, so presumably we can extract it.  And indeed we can -- only with depth_first search!  Two special methods are provided:  the first, property *CircuitFinder.circuit* extracts the cells:
```
>>> dump2 = status.circuit
>>> print(list(cell.index for cell in dump2))
[(6, 4), (5, 4), (4, 4), (3, 4), (3, 5), (4, 5), (5, 5), (6, 5)]
```
The *circuit* property is included primarily for the benefit of programmers.  Method *CircuitFinder.label\_circuit* provides a console display.  The optional argument *label* defaults to an asterisk.  The *source* and *target* of the edge at the top of the stack are labelled "S" and "T" respectively:
```
>>> dump2 = status.label_circuit(); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     o   o   o |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
| o   o |   | o   T   * |           |       |       |
+   +---+---+---+   +   +---+   +---+---+   +---+   +
| o   o   o |     S | * |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|         o   0 | * | *     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   | *   * |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
To turn everything into breadcrumbs:

*  `status.label_circuit(source="*", target="*")`

### Example 1.2  Eliminating a circuit

To eliminate a circuit, we simply erect a wall in place of one of the passages that form the circuit.  In fact we have one such passage. Above, we typed:

* `cell3, join, cell4 = status.result`

So we named the passage *join*.  (A join in a network is an arc (directed) or an edge (undirected) which connects two nodes (vertices or cells).  Let's remove that join:
```
>>> maze.unlink(join)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     o   o   o |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
| o   o |   | o   T   * |           |       |       |
+   +---+---+---+---+   +---+   +---+---+   +---+   +
| o   o   o |     S | * |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|         o   0 | * | *     |   |       |       |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   | *   * |       |   |       |   |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           |               |       |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       |   |       |   |       |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                                 1                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We still have a circuit, and we actually know one of its edges since we ourselves introduced the circuit.  But we want the circuit locator to find it.  A good place to start looking is the cell labelled 1 since it is part of the circuit...
```
>>> status = CircuitFinder.on(maze, start_cell=cell1); print(status)
          DFS Circuit Locator (statistics)
                            visits       44
                     queuing class  Stack
                           shuffle        1
                  components found        1
               components finished        0
                     cells visited       24
                        start cell  (0, 8)
              maximum queue length       20
                           circuit  ((0, 9), (0, 8))
>>> status.label_pmqueue(label="#"); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     o   o   o |       |                       |   |
+---+   +   +   +---+   +---+   +---+---+   +   +   +
| o   o |   | o   T   * |           |       |       |
+   +---+---+---+---+   +---+   +---+---+   +---+   +
| o   o   o |     S | * |   |   |   |       |   |   |
+---+---+   +---+   +   +   +---+   +---+---+   +   +
|         o   0 | * | *     |   |       | #   # |   |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|   |       |   | *   * |       |   | #   # | # |   |
+   +---+   +   +---+   +---+   +---+   +---+   +   +
|   |       |           | #   #   #   # | #   # |   |
+   +   +---+---+   +---+   +   +---+   +   +---+   +
|       |   |   |       | # |       |   | #   # |   |
+   +---+   +   +   +---+   +---+---+---+---+   +   +
|                         #   #   #   #   #   #     |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
If we had started outside the circuit, there would be more hash marks.

At this point we have a maze which is connected and *acyclic*, *i.e.* a perfect maze (or spanning tree.

### Example 1.3  Creating a maze by locating circuits (DFS)

To prepare a grid for a wall builder, we need to knock down all the walls.  The *Maze.link\_all* method does the job. To obtain a perfect maze, we need to keep breaking circuits (by unlinking or erecting walls) until none are left.  For a rectangular maze with 8 rows and 13 columns, we must break exactly 84 circuits.
(How we arrive at exactly 84 is described in another document.)
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
>>> print(BasicWallbuilder.on(maze)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                     finder passes     2974
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |               |                   |           |
+   +   +   +---+   +   +---+   +---+---+   +   +---+
|       |   |           |   |   |           |       |
+   +---+---+   +---+---+   +   +   +   +---+---+   +
|   |   |           |       |       |   |       |   |
+   +   +---+---+   +---+   +---+---+---+   +   +---+
|       |       |                           |       |
+---+---+   +   +---+---+   +   +---+---+---+---+   +
|           |       |       |   |       |       |   |
+   +---+---+   +   +---+---+---+   +---+   +---+   +
|       |   |   |       |                   |   |   |
+---+---+   +---+---+   +---+   +---+   +---+   +   +
|   |       |   |                   |           |   |
+   +   +   +   +---+---+---+---+   +---+---+---+   +
|       |                                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Not bad!

### Example 1.4  Starting cells and shuffling (DFS)

The circuit locator can be given a starting cell.  What happens if we use the same starting cell for all 84 circuits?  We'll try a corner and somewhere in the middle...  We'll also get rid of shuffling as that requires additional overhead... First a corner, with shuffling:
```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, start_cell=maze.grid[0,0])); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                        start cell  (0, 0)
                     finder passes     4157
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |                       |       |           |   |
+   +   +---+---+---+---+   +   +   +---+---+   +   +
|       |               |       |           |   |   |
+   +---+---+---+---+   +---+   +   +   +   +   +   +
|                       |   |   |   |   |   |       |
+---+   +   +---+---+   +   +   +---+   +---+   +---+
|       |   |               |   |           |       |
+   +   +   +---+   +---+   +---+   +---+   +---+   +
|   |   |   |   |       |   |       |   |   |   |   |
+   +---+---+   +---+   +---+   +---+   +   +   +   +
|   |               |   |       |   |       |   |   |
+---+   +---+---+   +   +   +---+   +   +   +   +   +
|       |       |   |   |   |           |           |
+   +---+   +---+   +---+   +   +---+---+---+---+---+
|   |                       |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
A bit more effort (more "finder passes"), but not shabby.

Same corner, now with no shuffling
```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, start_cell=maze.grid[0,0],
...                           shuffle=False)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                        start cell  (0, 0)
                     finder passes     8291
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
|                                                   |
+   +---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
|                                                   |
+   +---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
|                                                   |
+   +---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Reducing the ovehead actually increased the overhead.  The result isn't really my taste in mazes, but it's of theoretical interest.  It's an example of a chain, a tree with no degree-3 cells.  It has exactly two dead ends.

Let's try the center, but with shuffling:
```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> median = maze.grid[4,6]; median.label = "M"
>>> print(BasicWallbuilder.on(maze, start_cell=median)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                        start cell  (4, 6)
                     finder passes     3229
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |                       |       |           |   |
+   +---+---+---+   +---+   +   +   +   +---+   +   +
|   |           |       |       |           |       |
+   +   +   +---+---+---+---+---+---+---+---+---+   +
|   |   |           |                   |       |   |
+   +   +---+   +---+   +---+---+---+   +   +   +   +
|   |   |       |   |     M |   |   |   |   |       |
+   +   +   +   +   +---+---+   +   +   +   +---+   +
|       |   |   |               |       |   |       |
+   +---+   +   +   +---+---+   +   +---+   +   +   +
|   |       |               |   |       |   |   |   |
+   +---+---+---+---+---+   +---+---+   +   +---+   +
|               |                       |   |   |   |
+---+   +---+---+---+---+---+---+---+---+   +   +   +
|                                           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
There is a lot more order apparent here than in the maze that started in the corner,  What happens if we don't shuffle?
```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> median = maze.grid[4,6]; median.label = "M"
>>> print(BasicWallbuilder.on(maze, start_cell=median, shuffle=False)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                        start cell  (4, 6)
                     finder passes     9065
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                       |           |
+   +---+---+---+---+---+---+---+---+   +---+---+   +
|                                   |               |
+---+---+---+---+---+---+---+---+   +---+---+---+---+
|                               |                   |
+   +---+---+---+---+---+---+   +---+---+---+---+   +
|                       | M |   |                   |
+---+---+---+---+---+   +   +   +   +---+---+---+---+
|                       |   |   |                   |
+   +---+---+---+---+---+   +   +---+---+---+---+   +
|                       |   |   |                   |
+---+---+---+---+---+   +   +   +   +---+---+---+---+
|                       |   |   |                   |
+   +---+---+---+---+---+   +   +---+---+---+---+   +
|                           |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
And here we have another chain!  Again not my cup of tea.

### Example 1.5 Shuffle or no?  (DFS)

What about shuffling without specifying a starting cell?  Does it matter?

Here we shuffle the neighborhoods before we iterate through them...
```
>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                     finder passes     3060
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |       |           |           |   |
+   +   +---+   +   +---+   +   +   +---+---+   +   +
|   |       |           |   |   |               |   |
+   +---+---+   +---+---+   +---+   +---+---+---+   +
|           |       |       |       |           |   |
+---+---+   +---+   +---+   +   +---+   +---+   +   +
|       |       |           |   |   |   |           |
+   +---+---+   +   +---+   +   +   +---+   +---+   +
|           |   |   |       |   |       |   |       |
+---+   +---+   +   +---+   +   +---+   +   +---+---+
|                       |   |           |           |
+---+   +---+---+---+   +   +---+---+   +   +---+   +
|       |       |       |           |   |   |       |
+   +   +---+   +   +---+---+   +   +---+---+   +   +
|   |           |   |           |               |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Here we don't shuffle -- we use the neighborhoods im dictionary order:
```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, shuffle=False)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                     finder passes     8820
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                           |       |
+   +---+---+---+---+   +---+---+   +---+   +---+   +
|                   |   |       |       |       |   |
+---+---+---+   +   +---+---+   +---+   +---+   +   +
|               |           |               |       |
+---+---+---+---+---+---+   +   +---+---+   +---+---+
|                       |   |           |           |
+   +---+---+---+---+   +---+---+---+---+---+---+   +
|                   |       |                       |
+   +---+---+---+---+---+   +   +---+---+---+---+---+
|               |           |                       |
+---+---+---+   +   +---+---+---+---+---+---+---+   +
|               |                                   |
+   +---+---+---+---+---+---+---+---+---+---+---+   +
|                               |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Letting the circuit locators choose their own starting cells certainly helped to derange the maze, but there seems to be a bit more order here than in the shuffled predecessor.  And note that more work was done.

(This calls for some statistical analysis!)

## Section 2  Breadth-first search

Traversals other than depth-first search can locate an edge in a circuit, but don't preserve the circuit.  If you look at the code in modules *mazes.Algorithms.bfs\_circuit\_locator* and *mazes.Algorithms.dfs\_circuit\_locator*, you'll notice that both leave almost all of the work to *mazes.Algorithms.qs\_circuit\_locator*.  That's because all we really need is to change the queuing structure.  (Things get messy the queuing structure has additional arguments.)

### Example 2.1  Using the basic wallbuilder with queues (BFS)

To change the queuing discipline in the circuit locator queues, we need to switch from a stack (LIFO) to a queue (FIFO).  That requires one additional import (class *Queue*) and one additional argument (*QueueType=Queue*).  So that we can see how BFS affects the order in the maze, we'll start all the circuit locators in the middle and we won't shuffle the neighborhoods.
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Queues.queue import Queue
>>> from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, QueueType=Queue, shuffle=False,
...                           start_cell=maze.grid[4,6]))
>>> print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                        start cell  (4, 6)
                     finder passes    13109
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+   +---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+   +---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+   +---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+   +---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Depth-first search attempted to create a single chain.  Shuffling and letting the starting cell both made it harder to create that single path.  Breadth-first search strives for paths from the starting point to be as short as possible.  Now let's derange the algorithm by randomizing the neighborhoods and allowing the locators to choose their own starting points at random.

```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, QueueType=Queue)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                     finder passes     4362
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                       |           |
+   +   +---+---+---+   +   +---+   +---+---+   +   +
|   |       |   |   |   |       |           |   |   |
+   +   +---+   +   +   +   +   +---+---+---+---+   +
|   |   |           |   |   |   |       |   |   |   |
+   +---+   +---+   +   +   +---+---+   +   +   +   +
|       |   |       |   |   |       |   |   |       |
+---+   +---+   +   +---+---+   +---+   +   +   +---+
|   |   |       |   |                   |   |       |
+   +   +---+---+   +---+   +---+   +   +   +   +---+
|               |   |   |       |   |               |
+   +   +---+   +   +   +   +---+---+---+   +   +   +
|   |   |           |   |   |   |       |   |   |   |
+   +   +---+   +   +   +---+   +---+   +---+---+   +
|   |       |   |                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
More chaos (a good quality in mazes in my opinion), but some order still seems apparent.

### Example 2.2  The BFS wall builder

Module *bfs\_basic\_wallbuilder* takes an optional *start\_cell*, and *shuffle* can be set to *False*.  It hides the *Queue* class.  Apart from saving just a little coding, there are no particular advantages.  But it does serve as a template for more complicated wrappers of the *BasicWallbuilder* class.

```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.bfs_wallbuilder import BFSWallbuilder
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(BFSWallbuilder.on(maze)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  BFS Circuit Locator
                     finder passes     3367
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |               |       |   |
+   +---+   +   +---+---+   +---+---+   +   +---+   +
|   |           |   |       |           |   |       |
+   +---+   +---+   +---+---+   +---+---+   +---+   +
|   |   |                                   |   |   |
+   +   +---+   +---+---+---+---+   +   +   +   +   +
|           |           |   |   |   |   |   |   |   |
+   +   +---+---+   +---+   +   +   +---+---+   +   +
|   |   |           |       |               |   |   |
+   +---+   +---+---+   +---+---+---+---+   +   +   +
|       |   |               |   |   |               |
+   +---+   +   +---+---+   +   +   +---+   +---+   +
|           |   |   |               |   |   |       |
+   +---+---+   +   +   +---+---+---+   +---+---+   +
|               |                               |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 2.3  the BFS circuit locator

The module *bfs\_circuit_locator* is a wrapper (not a decorator!) for the *CircuitFinder* class.  All it really does is set *QueueType=Queue* to use class *Queue* instead of class *Stack*.  The start cell and the shuffle flag are optional arguments.

First we need a maze with a circuit...  We will carve a perfect maze (using Wilson's algorithm) and then tear down one wall to create a circuit.
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(8, 13)); print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       42
                             cells      104
                          passages      103
                 paths constructed       42
                     cells visited      453
                          circuits      116
                    markers placed      295
                   markers removed      192
                     starting cell  (6, 6)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |               |                   |
+   +   +---+   +---+   +---+---+   +   +---+---+   +
|   |   |       |   |           |   |       |       |
+---+   +---+---+   +---+---+   +   +   +---+---+---+
|           |   |   |       |       |       |       |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|   |       |       |   |                       |   |
+---+---+   +   +---+   +---+   +---+---+---+   +---+
|   |       |   |       |   |       |               |
+   +   +---+   +---+   +   +   +---+---+---+---+   +
|   |               |   |                   |   |   |
+   +---+   +---+   +---+---+---+   +   +   +   +   +
|               |   |               |   |       |   |
+   +   +   +---+   +---+   +   +---+   +---+   +---+
|   |   |       |           |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now we create our circuit -- we will label the endpoints of the passage that we added:
```
>>> cell0 = maze.grid[3,3]; maze.link(cell0, cell0.east)
<Edge object>
>>> cell0.label = cell0.east.label = "0"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |               |                   |
+   +   +---+   +---+   +---+---+   +   +---+---+   +
|   |   |       |   |           |   |       |       |
+---+   +---+---+   +---+---+   +   +   +---+---+---+
|           |   |   |       |       |       |       |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|   |       |       |   |                       |   |
+---+---+   +   +---+   +---+   +---+---+---+   +---+
|   |       | 0   0     |   |       |               |
+   +   +---+   +---+   +   +   +---+---+---+---+   +
|   |               |   |                   |   |   |
+   +---+   +---+   +---+---+---+   +   +   +   +   +
|               |   |               |   |       |   |
+   +   +   +---+   +---+   +   +---+   +---+   +---+
|   |   |       |           |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now let's programmaticall find an edge in the circuit.  We'll let the circuit finder choose a starting cell and we will traverse neighborhoods in a random order.  (Keyword argument *start\_cell* can be used to specify a starting cell.  If keyword argument *shuffle* is set to *False*, neighborhoods will be traversed in dictionary order.)  Two lines: first an import, and then a class method call:
```
>>> from mazes.Algorithms.bfs_circuit_locator import CircuitFinder
>>> status = CircuitFinder.on(maze)
```

Let's look at the status:
```
>>> print(status)
          BFS Circuit Locator (statistics)
                            visits      219
                     queuing class  Queue
                           shuffle        1
                  components found        1
               components finished        0
                     cells visited       76
                        start cell  (7, 12)
              maximum queue length       10
                           circuit  ((2, 4), (1, 4))
```

Let's extract the starting passage and its endpoints:
```
>>> cell1, edge, cell2 = status.result
>>> cell1.label="A"; cell2.label="B"; print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |               |                   |
+   +   +---+   +---+   +---+---+   +   +---+---+   +
|   |   |       |   |           |   |       |       |
+---+   +---+---+   +---+---+   +   +   +---+---+---+
|           |   |   |       |       |       |       |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|   |       |       |   |                       |   |
+---+---+   +   +---+   +---+   +---+---+---+   +---+
|   |       | 0   0     |   |       |               |
+   +   +---+   +---+   +   +   +---+---+---+---+   +
|   |             A |   |                   |   |   |
+   +---+   +---+   +---+---+---+   +   +   +   +   +
|               | B |               |   |       |   |
+   +   +   +---+   +---+   +   +---+   +---+   +---+
|   |   |       |           |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now let's see what breadth-first search has in its queue:
```
>>> status.label_pmqueue(label="#"); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |               |                   |
+   +   +---+   +---+   +---+---+   +   +---+---+   +
|   |   |       |   |           |   |       |       |
+---+   +---+---+   +---+---+   +   +   +---+---+---+
|           |   | # |       |       |       |       |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|   |       |       |   |                       |   |
+---+---+   +   +---+   +---+   +---+---+---+   +---+
|   |       | 0   0     |   |       |               |
+   +   +---+   +---+   +   +   +---+---+---+---+   +
|   |     #       # |   |                   |   |   |
+   +---+   +---+   +---+---+---+   +   +   +   +   +
|               | # |               |   |       |   |
+   +   +   +---+   +---+   +   +---+   +---+   +---+
|   |   |       |           |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Four cells including the two endpoints.  Endpoint *B* was earlier in queue than endpoint *A*... If we had used depth-first search, the circuit would have been traversed counterclockwise (from *B* to *A* in nineteen steps, by my count, and then one more step to return to *B*.  With breadth first search, all we have is a cell *A* and a previously unvisited passage *e* from *A* to *B*... Since *B* was already visited, we know that passage *e* is an edge in a circuit.

If delete edge *e*, we will have a new perfect maze:
```
>>> maze.unlink(edge)
>>> status = CircuitFinder.on(maze); print(status); print(maze)
          BFS Circuit Locator (statistics)
                            visits      311
                     queuing class  Queue
                           shuffle        1
                  components found        1
               components finished        1
                     cells visited      104
                        start cell  (2, 12)
              maximum queue length       11
                           circuit  None     <--- NOTE!
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |               |                   |
+   +   +---+   +---+   +---+---+   +   +---+---+   +
|   |   |       |   |           |   |       |       |
+---+   +---+---+   +---+---+   +   +   +---+---+---+
|           |   | # |       |       |       |       |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|   |       |       |   |                       |   |
+---+---+   +   +---+   +---+   +---+---+---+   +---+
|   |       | 0   0     |   |       |               |
+   +   +---+   +---+   +   +   +---+---+---+---+   +
|   |     #       # |   |                   |   |   |
+   +---+   +---+---+---+---+---+   +   +   +   +   +
|               | # |               |   |       |   |
+   +   +   +---+   +---+   +   +---+   +---+   +---+
|   |   |       |           |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## 3. Wallbuilding using an edge-based priority queue

Module *pq\_wallbuilder* replaces the stack with a priority queue.  That's messier than replacing a stack with a queue -- a priority queue has several arguments.  Prim's algorithm is a growing tree algorithm that uses edge costs in order to find a minimum edge-cost spanning tree.  (Prim's algorithm is a passage carver.)

We might consider removing circuits using edge costs in a sort of reverse-Prim, but that's not what happens here.  So we cannot go so far as to call the algorithm here "Reverse Prim".  Instead we have a simplistic version which I'll call "Simpleton's Reverse Prim" for lack of a better name.  A careful implementation of "Reverse Prim" will have to wait.

How does our simplistic version differ?  Circuits are broken independently of one another.  After we remove a circuit, we start anew with a new circuit finder.

### Example 3.1 a simpleton's reverse Prim

We start with a *complete* Von Neumann rectangular maze:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
```

**REMINDER:** "Complete" means all grid edges are passages.  "Von Neumann" means that grid  neighborhoods consist of a cell and its north, south, east and west neighbors.

Now let's import the wall builder:
```
>>> from mazes.WallBuilders.pq_wallbuilder import PQWallbuilder
```

Let's look at the documentation for *parse\_args* before we proceed:
```
>>> help(PQWallbuilder.Status.parse_args)
Help on function parse_args in module mazes.WallBuilders.pq_wallbuilder:

parse_args(self, shuffle: bool=True, start_cell:Cell=None,
        pr:(callable, dict) = dict(), prtype:str="edge",
        qtype:str = "unstable")
    parse the setup arguments

    REQUIRED ARGUMENTS

        maze - a maze object in which walls need to be erected

    KEYWORD ARGUMENTS

        shuffle (default: True) - if False, a cell's neighbors will
            be traversed in dictionary order.  If true, the neighborhood
            will be shuffled.

        start_cell (default: None) - if a starting cell is supplied,
            all circuit location passes will start there.

            If the maze is disconnected, the search will always start
            in the component containing the start cell.  For the
            remaining components, the search will start in a random cell.

        pr - a priority function or dictionary

        prtype = "vertex", "edge" (default), or "arc"

        qtype = "stable", "unstable" (default) or "antistable"
```
We encountered the *shuffle* option and the *start\_cell* arguments in Sections 1 and 2.  The priority function is a function which maps either cells (vertices), passages (edges) or (cell, passage)-pairs (arcs) to a cost.  The priority type ('prype') describes the type of the input.  The priority function can be implemented as a function or as a dictionary.  The queue type determines how equal keys are handled.

If the priority function is incomplete, it will be supplemented to insure that any given key always maps to the same cost.  As a result, the given priority function can be empty.

And now we run the wall builder:
```
>>> print(PQWallbuilder.on(maze)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Priority Queue Circuit Locator
                     finder passes     3348
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                           |                       |
+---+---+---+   +   +   +---+   +---+---+---+   +   +
|   |       |   |   |   |   |   |   |       |   |   |
+   +---+   +---+---+   +   +---+   +   +---+   +---+
|   |               |                   |           |
+   +---+   +---+   +---+   +   +   +---+   +---+   +
|       |   |               |   |       |       |   |
+   +   +   +---+---+---+---+---+---+---+   +---+   +
|   |           |                               |   |
+   +---+---+---+---+---+   +   +---+---+   +---+   +
|           |   |           |       |           |   |
+   +   +---+   +   +   +---+   +   +---+---+   +---+
|   |   |   |       |   |   |   |   |       |       |
+---+   +   +   +---+---+   +---+   +---+   +   +---+
|                       |               |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 3.2  With a start cell and no shuffling

```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> cell0 = maze.grid[4,6]
>>> print(PQWallbuilder.on(maze, start_cell=cell0, shuffle=False)); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Priority Queue Circuit Locator
                        start cell  (4, 6)
                     finder passes     5270
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |                           |   |       |
+   +---+   +---+---+   +---+---+   +   +   +---+   +
|                           |       |           |   |
+   +---+---+---+   +---+---+---+---+---+---+   +   +
|               |       |               |           |
+---+---+   +---+---+---+---+---+   +---+---+   +---+
|                           |   |       |   |       |
+---+---+   +   +---+   +   +   +   +   +   +---+   +
|       |   |       |   |   |   |   |               |
+   +---+---+---+---+   +   +   +---+   +---+   +   +
|                   |   |   |       |   |       |   |
+   +   +   +---+---+---+---+---+   +---+   +---+---+
|   |   |               |               |       |   |
+   +---+   +   +   +---+   +---+   +---+   +---+   +
|       |   |   |               |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The difference here is not as significant as it was for DFS or BFS,

### Example 3.3  the priority queue cell locator

First, we create a maze with a circuit
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(8, 13)); print(Wilson.on(maze)); print(maze)
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       39
                             cells      104
                          passages      103
                 paths constructed       39
                     cells visited      648
                          circuits      183
                    markers placed      426
                   markers removed      323
                     starting cell  (7, 10)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                       |           |
+---+   +   +---+   +---+---+   +---+   +   +---+---+
|   |   |   |   |   |   |   |   |   |   |           |
+   +---+---+   +   +   +   +   +   +   +   +---+   +
|   |           |   |               |   |   |   |   |
+   +   +---+   +   +---+   +---+---+---+   +   +   +
|   |       |       |   |       |               |   |
+   +   +   +   +---+   +   +---+   +   +---+---+---+
|       |   |   |       |   |       |               |
+   +---+---+---+   +---+---+   +   +---+---+   +   +
|       |                       |       |   |   |   |
+   +---+   +---+   +   +---+   +---+   +   +---+   +
|   |   |       |   |       |   |           |       |
+   +   +---+---+   +   +---+   +---+---+---+   +   +
|                   |       |       |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> cell0 = maze.grid[2,1]; maze.link(cell0, cell0.east)
<Edge object>
```

Next we import the priority queue circuit finder class and get help for method *Status.parse_args*:
```
>>> from mazes.Algorithms.pq_circuit_locator import CircuitFinder
>>> help(CircuitFinder.Status.parse_args)
Help on function parse_args in module mazes.Algorithms.pq_circuit_locator:

parse_args(self, start_cell:Cell=None, shuffle:bool=True,
           pr:(callable>, dict)=dict(), prtype:str ="edge",
           qtype:str="unstable", cached:bool=True, **kwargs)
    parse constructor arguments

    POSITIONAL ARGUMENTS

        maze - handled by __init__ in the base class.

    KEYWORD ARGUMENTS

        start_cell - an optional starting cell

        shuffle - if False, neighbors are processed first come,
            first served.  (Being pushed onto the stack counts
            as being served, so "the first shall be last" and
            "the last shall be first".)  The default is True.

        pr - a priority function or dictionary.

        prtype - one of "vertex", "edge", or "arc". If 'prtype' is
            "arc", then the priorty takes two arguments, namely a
            cell and a passage in that order.  The vertex and edge
            priorities both take one argument, a cell or a passage,
            respectively. (default: edge)

        qtype - one of "stable", "unstable" or "antistable".  This
            determines how equal priorities are handled. (default:
            unstable)

        cached - determines whether priorities are cached or calculated
            anew each time.  If the priority map is complete and free
            of side effects (i.e. a pure function), then caching is
            unnecessary but might improve performance.  If the priority
            map is incomplete or suffers from side effects, caching
            guarantees a pure priority function.  There is a performance
            tradeoff as caching requires additional space roughly
            proportional to the number of distinct keys. (default: True)

        _prng - a random number generator function. (default: rng.random)

        _prng_args - arguments for the random number generator.
            (default: ())

        _prng_kwargs - keyword arguments for the random number generator.
            (default: {})
```
Let's find a circuit and inspect the remains of the priority queue:
```
>>> status = CircuitFinder.on(maze)
>>> print(status)
          Priority Queue Circuit Locator (statistics)
                            visits      144
                     queuing class  PriorityQueue
                           shuffle        1
                  components found        1
               components finished        0
                     cells visited       55
                        start cell  (5, 10)
              maximum queue length       14
                           circuit  ((2, 2), (2, 3))
                     priority type  edge
               unmapped priorities       55
>>> cell0.label = "0"
>>> status.label_pmqueue(label="#"); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                       |           |
+---+   +   +---+   +---+---+   +---+   +   +---+---+
|   |   |   |   |   |   |   |   |   |   |           |
+   +---+---+   +   +   +   +   +   +   +   +---+   +
|   |           |   |               |   | # | # |   |
+   +   +---+   +   +---+   +---+---+---+   +   +   +
|   | #     |       |   |       |               |   |
+   +   +   +   +---+   +   +---+   +   +---+---+---+
|       |   |   |       |   |       |               |
+   +---+---+---+   +---+---+   +   +---+---+   +   +
|     0   #   #                 |       |   |   |   |
+   +---+   +---+   +   +---+   +---+   +   +---+   +
| # |   |     # |   | #     |   |         # |       |
+   +   +---+---+   +   +---+   +---+---+---+   +   +
|     #             |       |     # |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Now let's delete the edge to create a new  perfect maze:
```
>>> cell1, edge, cell2 = status.result
>>> maze.unlink(edge); print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                       |           |
+---+   +   +---+   +---+---+   +---+   +   +---+---+
|   |   |   |   |   |   |   |   |   |   |           |
+   +---+---+   +   +   +   +   +   +   +   +---+   +
|   |           |   |               |   | # | # |   |
+   +   +---+   +   +---+   +---+---+---+   +   +   +
|   | #     |       |   |       |               |   |
+   +   +   +   +---+   +   +---+   +   +---+---+---+
|       |   |   |       |   |       |               |
+   +---+---+---+   +---+---+   +   +---+---+   +   +
|     0   # | #                 |       |   |   |   |
+   +---+   +---+   +   +---+   +---+   +   +---+   +
| # |   |     # |   | #     |   |         # |       |
+   +   +---+---+   +   +---+   +---+---+---+   +   +
|     #             |       |     # |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Section 4. Wallbuilding using a vertex-based priority queue

### Example 4.1  shuffling, random start

We can assign costs to cells instead of passages:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> from mazes.WallBuilders.pq_wallbuilder import PQWallbuilder
>>> print(PQWallbuilder.on(maze, prtype="vertex")); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Priority Queue Circuit Locator
                     finder passes     3040
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |       |                       |
+   +---+   +---+---+---+   +---+   +   +---+---+---+
|       |   |           |       |   |   |           |
+---+   +---+   +---+   +   +---+   +---+---+   +---+
|           |   |       |       |       |           |
+---+---+   +   +---+---+   +---+   +---+   +---+---+
|               |                                   |
+---+---+   +---+   +   +---+---+---+---+---+   +   +
|   |       |   |   |   |   |       |   |   |   |   |
+   +---+   +   +   +---+   +   +---+   +   +   +---+
|       |       |       |       |       |       |   |
+   +   +---+   +---+   +   +---+   +---+---+   +   +
|   |   |                   |                   |   |
+   +   +---+   +   +   +   +---+---+   +   +---+   +
|   |           |   |   |   |           |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 4.2  shuffling, fixed start

```
>>> maze = Maze(OblongGrid(8, 13)); maze.link_all()
>>> print(PQWallbuilder.on(maze, prtype="vertex", shuffle=False, start_cell=maze.grid[4,6])); print(maze)
          maze algorithm (statistics)
                            visits       85
                           locator  Priority Queue Circuit Locator
                        start cell  (4, 6)
                     finder passes     5819
                           unlinks       84
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |                       |           |
+---+   +---+   +---+---+   +   +---+   +   +---+   +
|               |           |   |               |   |
+---+   +---+   +   +---+   +---+---+---+---+   +---+
|           |           |   |               |       |
+   +---+---+---+---+---+---+---+   +---+---+   +---+
|                           |   |           |   |   |
+---+---+   +---+---+   +   +   +   +---+---+   +   +
|   |   |   |           |   |       |       |       |
+   +   +   +---+---+---+   +---+   +   +   +---+   +
|   |       |           |   |           |   |   |   |
+   +---+   +   +---+   +   +   +   +---+   +   +---+
|   |       |   |   |   |       |   |   |   |   |   |
+   +---+   +---+   +   +   +   +   +   +---+   +   +
|           |               |   |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
