# Simple binary tree algorithm

## The classes

Module *mazes.Algorithms.misc.binary\_tree* contains adaptations of the simple binary tree algorithm for various subclasses of *OblongGrid*.  The following classes are defined:

1. class *OneShot* - a stub which is used to build the other classes.  It contains an implementation of the simple binary tree algorithm.

2. class *Cylinder* - an implementation of the simple binary tree algorithm which works correctly on the cylindrical grid.

3. class *Torus1* - a failed implementation of the simple binary tree algorithm on the toroidal grid.  It will sometimes create a disconnected maze.

Examples follow in the numbered sections below.

## The project

This program is an open project.

The goal is to use the simple binary tree logic in *OneShot.Status.visit\_cell* to create binary tree mazes on various grids.  To be successful, I think, a solution should be a class that is derived from class *OneShot* in which:

1. the *on* method for class instances should always produce a spanning binary tree for reasonable inputs,
2. the *visit\_cell* method in *OneShot.Status* must be used and not be overridden, and
3. the underlying algorithm should be feasible, that is, polynomial in time complexity.

Regarding point 2, some preprocessing and postprocessing might be permissible. But ideally, the passages should be chosen by *visit\_cell* in the base class.  Changes can, of course be made to methods like *can\_go\_onward* and *can\_go\_upward*.

Class *Cylinder* qualifies as a success as all four requirements are met.  Class *Torus1* fails on point 1.  Class *OneShot* itself succeeds on the rectangular grid (*i.e.* class *OblongGrid* in *mazes.Grids.oblong).

Regarding point 3, class *OneShot* on a *OblongGrid* and class *Cylinder* both produce spanning binary trees in time complexity which is linear in the number of cells.  Although class *Torus1* fails on point 1, its time complexity is also linear in the number of cells -- erecting the barriers is done in time which is linear (or, since we use sets, perhaps linear times a logarithm) in the greater of the number of rows or the number of columns.  So we might additionally require:

+ for a fully successful solution, the underlying algorithm should be no worse than log linear in time complexity, *i.e.* *O(v log v)* where *v* is the number of cells.

It should be obvious that we aren't interested in solutions that are trivial.  For example, a solution on the cylindrical grid which always blocks passage east in a fixed column would be trivial as this basically cuts the cylinder to form a rectangle.  Such a solution is fine if it occurs randomly, but not if it's preordained.

Another feature of the simple binary tree algorithm is that what happen in a cell is independent of what happens in another cell.  We can imagine a demom in cell who carves the required passage without any information from demons in other cells.  Class *OneShot* on the *OblongGrid*, class *Cylinder*, and class *Torus1* all satisfy this cell-independence.  One barriers have been erected, the only information needed for each visit are which grid connections are available for links.  We only use information local to the cell; we don't use any information from the neighboring cells.

## Section 1 - class *OneShot*

This class is a stub intended as a tool for programmers.  But it can be used to create a simple binary tree maze on a rectangular grid.  Here we go!
```
>>> from mazes.Algorithms.misc.binary_tree import OneShot
>>> from mazes.Grids.oblong import OblongGrid
>>> obj = OneShot(OblongGrid, 8, 13)
```
Notice that the grid class is the first argument.  Subclasses can simply fix the type and pass it along to the *OneShot* constructor.  The remaining arguments are whatever is needed for the grid class constructor.  The grid is wrapped inside a *Maze* object.

To carve the maze we use the object's *on* method.  For *OneShot*, the arguments are the onward direction, the upward direction, and the coin bias (probably of a head or upward call).  All three are require positional arguments.  *OneShot* is a stub, so the two directions are not checked.  Misspelling them or picking directions that are not orthogonal will lead to undesirable results.

We will go *onward='east', upward='west'* with a fair coin:
```
>>> print(obj.on('east', 'north', 0.5))
          Simple Binary Tree (stub) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       41
                             tails       43
>>> print(obj.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +---+---+---+   +   +   +   +   +   +   +
|   |   |   |               |   |   |   |   |   |   |
+   +   +   +---+---+---+   +---+   +   +---+   +   +
|   |   |   |               |       |   |       |   |
+---+---+---+   +---+---+---+---+   +   +   +---+   +
|               |                   |   |   |       |
+   +---+   +---+---+---+---+---+---+   +   +   +   +
|   |       |                           |   |   |   |
+---+   +---+   +---+   +---+---+---+---+   +   +   +
|       |       |       |                   |   |   |
+---+   +   +   +---+---+   +---+---+---+   +---+   +
|       |   |   |           |               |       |
+---+---+   +---+   +---+---+   +   +   +   +---+   +
|           |       |           |   |   |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
In 84 of 105 cells, there was a choice of two directions.  In those cells, a head came up 41 times, resulting in a northward passage.  In the remaining 43 cells, a tail resulted in an eastward passage.

Along the top row and along the rightmost column, there were fewer than two choices. Except for the top right cell, there was one available direction, and a passage was carved in that direction.

The maze object is available as *obj.maze* and the status object is available as *obj.status*.

We can can query these two objects for some additional information:
```
>>> obj.status.onward
'east'
>>> obj.status.upward
'north'
>>> obj.status.bias
0.5
>>> type(obj.maze.grid)
<class 'mazes.Grids.oblong.OblongGrid'>
```

## Section 2 - class *Cylinder*

This class is working implementation of the simple binary tree algorithm for the cylindirical grid class.  It avoids circuits by placing one barrier in each row to insure that no row becomes a circuit.

### Example 2.1 - An E/W cylinder maze

We create our maze usiing three Python statements.  First we import class *Cylinder*.  We then create a *Cylinder* object.  Finally, we execute the *Cylinder* object's on method to carve the maze.  For this example, we will display the barriers along with the maze.

The three steps work much like any of our maze carving algorithms with one important difference.  The *on* method here is an object method, and not a class method.

Here we go!
```
maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.misc.binary_tree import Cylinder
>>> obj = Cylinder(8, 13)
>>> print(obj.on())
          Simple Binary Tree (Cylinder) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       47
                             tails       37
                          barriers        8
```
The maze object is *obj.maze* and the status object is *obj.status*.  Let's label the barrier cells.  They are are available (as a *frozenset* object) from a property (*obj.status.barriers*) defined in the status object.

```
>>> for cell in obj.status.barriers:
...     cell.label = "B"
...
```
And now the maze:
```
>>> print(obj.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
          B |
+---+---+---+   +   +   +   +   +   +   +   +---+   +
|             B |   |   |   |   |   |   |   |       |
+---+   +---+   +---+---+   +---+---+   +---+   +   +
|       |       |           |         B |       |   |
+---+   +---+---+   +   +---+---+   +   +---+   +---+
        |           | B |           |   |       |
+---+   +---+---+   +   +   +   +---+---+---+   +   +
|     B |           |   |   |   |               |   |
+---+   +   +---+   +   +   +   +   +   +   +   +   +
|       |   |       |   |   |   |   |   | B |   |   |
+---+   +---+   +   +---+   +   +---+---+   +---+---+
        |       |   |       | B |           |
+---+   +   +   +   +---+---+   +   +   +   +   +---+
        | B |   |   |           |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note in each barrier cell, there is no eastward passage,  We can easily find a passage to the barrier cell in the top row.  For example, starting in the lower left, we go one step east, six steps north, two steps east, one step north, and twelve steps east.

The barrier cells guarantee that no row is a circuit.  We used the default coin bias of 50%, so in each cell where there was a choice of carving east or north, there was a 50% chance of carving northward.  For rows other than the top row, the probably of a long eastward corridor is *1/2^12* (12 non-barrier cells) or *1/4096*.  Without the barrier cells, the probablity of a completely free row is 1 for the top row, but *1/8192* (*1/2^13*) for the remaining rows.  If we only put in the barrier at the top, it might take a lot of testing to see that there was still a problem.

### Example 2.2 - A N/S cylinder maze

The initialization method takes the *CylinderGrid* constructor arguments.  These always include the numbers of rows and columns.  To identify the top and bottom sides, we set the *parity* option to *True*:

```
>>> obj = Cylinder(8, 13, parity=True)
```

Now we have hard walls to the east and west of the maze, but fluidity of movement north and south.  In the previous example, the top (northmost) row corresponds to the long corridor in the top row of an E/N or a W/N simple binary tree maze.  The barriers correspond to the long corrider along the east wall of an E/N tree and the cells one step east of the barriers correspond to the long corridor along the west wall for a W/N simple binary tree.  With the cylinder maze, east and west don't really play a role, but we need a way of deciding whether long open corridor is along the north wall or the south wall.

For a N/S cylinder grid, north and south don't matter, but east and west do.  The default is always north and east.  To select west for the N/S cylinder grid (or south for the E/W cylinder grid), we set the *reverse* option to True.

The *bias* option can be changed to make longer (on average) open corridors in the axial direction (*0.5 < bias ≤ 1*) or to make longer (on average) open corridors in the circular direction (*0 ≤ bias < 0.5*).

In this example, we want to guarantee a long open corridor along the west wall, and we will use a low bias to get longer than average open vertical corridors:
```
>>> print(obj.on(bias=0.2, reverse=True))
          Simple Binary Tree (Cylinder) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       15
                             tails       69
                          barriers       13
>>> print(obj.maze)
+   +   +   +---+---+   +   +   +   +---+---+   +   +
|   |   |           |   |   |   |           |   |   |
+   +---+---+   +   +---+   +   +   +   +---+   +   +
|           |   |       |   |   |   |       |   |   |
+   +---+   +---+---+   +   +   +---+   +   +   +---+
|       |           |   |   |       |   |   |       |
+   +   +---+---+   +   +   +   +---+   +   +   +   +
|   |           |   |   |   |       |   |   |   |   |
+   +---+   +   +   +   +---+   +   +   +   +   +---+
|       |   |   |   |       |   |   |   |   |       |
+---+   +   +   +   +   +   +---+   +---+   +   +   +
|   |   |   |   |   |   |       |       |   |   |   |
+   +---+   +   +   +   +   +   +   +---+   +   +   +
|       |   |   |   |   |   |   |       |   |   |   |
+   +---+   +---+---+   +   +   +   +   +   +---+   +
|       |           |   |   |   |   |   |       |   |
+   +   +   +---+---+   +   +   +   +---+---+   +   +
```

Here we have the longest possible vertical open corridor (a vertical path of length 7, all eight cells) along the west wall (in column 0).  In addition, columns 5, 6, 7, and 11 all contaim vertical paths of length 7.

We rolled a head in 15 of 15+69=84 coin flips for an average of about 18% of the rolls.  The coin bias was 0.2 or 20%.

Incidentally, let's verify the type of the grid object (*obj.maze.grid*) :
```
>>> type(obj.maze.grid)
<class 'mazes.Grids.cylinder.CylinderGrid'>
```

## Section 3 - class *Torus1*

A good idea that works in one situation might not work in another.  Here we place one barrier east in each row and one barrier north in each column.  To guarantee a root cell, we make sure that exactly one cell contains both types of barriers.  This generalizes the idea that worked well for a cylindrical maze.  But the torus is more complicated.  The idea will work some of the time and it will fail some of the time.  Below we show both (in Examples 3.1 and 3.2) that the barrier method can fail, and (in Example 3.3). that the barrier method can also succeed.

Since it can fail, I decided to name the class *Torus1* instead of *Torus*.  If, in the future, I am able to find some way of successfully guaranteeing the binary tree using the simple algorithm, that class will be named *Torus*.  It might be derived from class *Torus1* or it might be derived directly from class *OneShot* -- or perhaps someone else might fill in the needed details -- or perhaps prove that the dream is not computationally feasible.

### Example 3.1 - A failure
```
maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.misc.binary_tree import Torus1
>>> obj = Torus1(8, 13)
>>> print(obj.on(bias=0.4))
*** WARNING:  The maze that results might not be connected. ***
          Simple Binary Tree (Torus) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       34
                             tails       50
                      row barriers        8
                   column barriers       13
                     root barriers        1
```
The warning simply tells us that there might be a problem.  It doesn't tell us that there is a problem.  The *Torus1* class does have built-in diagnostics:
```
>>> target = obj.verify()
*** WARNING: the maze is disconnected. ***
```
Now we do know that is is disconnected.  If it were connected, the value of *target* would be *None*.  Since the maze is disconnected, the value of *target* is a cell which is not reachable from the root cell.
```
>>> print(target.index)
(0, 0)
```
Convenient!  Let's label the barriers and look at the maze:
```
>>> obj.label_barriers()
>>> print(obj.maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏━━━┳   ┳━━━┳━━━┳   ┳   ┳━━━┳   ┳━━━┳━━━┳━━━┳━━━┳   ┓
  7 ┃ N     ┃           ┃ E ┃       ┃                   ┃ 7
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━┫
  6     ┃     N           E ┃   ┃   ┃               ┃ N   6
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  5 ┃         E ┃             N                 ┃       ┃ 5
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  4         ┃   ┃ N             ┃     N       E ┃         4
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━┫
  3     ┃ N     ┃                   ┃ E ┃   ┃   ┃         3
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  2 ┃   ┃       ┃   ┃   ┃ N       N     ┃   ┃ E ┃       ┃ 2
    ┣   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  1 ┃ E ┃       ┃   ┃           ┃           ┃ N         ┃ 1
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  0         ┃   ┃     N     ┃           ┃ B ┃     N       0
    ┗━━━┻   ┻━━━┻━━━┻   ┻   ┻━━━┻   ┻━━━┻━━━┻━━━┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
```
The barrier cells are labelled "E" if the barrier blocks passage east, "N" if the barrier blocks passage north, and "B" if both are blocked.  The root cell is labelled "B".  It's easy to see that, in this case, the root cell is unreachable from every other cell.  In most cases, the failure won't be as obvious.

To show the existence of a circuit, we start at the root cell and construct a path with each step eastward or northward.  At some point we will reach a cell already on the path.  It might not be the starting cell, but it this case we did return to start:

```
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏━━━┳   ┳━━━┳━━━┳   ┳ ^ ┳━━━┳   ┳━━━┳━━━┳━━━┳━━━┳ ^ ┓
  7 ┃ N     ┃           ┃ * ┃       ┃             *   * ┃ 7
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━┫
  6     ┃     *   *   *   * ┃   ┃   ┃         *   * ┃ N   6
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  5 ┃         * ┃             N               * ┃       ┃ 5
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  4         ┃ * ┃ N             ┃     *   *   * ┃         4
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━┫
  3     ┃ N   * ┃                   ┃ * ┃   ┃   ┃         3
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ┫
  2 ┃   ┃     * ┃   ┃   ┃ N   *   *   * ┃   ┃ E ┃       ┃ 2
    ┣   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
  1 ┃ E ┃ *   * ┃   ┃     *   * ┃           ┃ N         ┃ 1
    ┣━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  0 > *   * ┃   ┃     N   * ┃           ┃ B ┃     N   * > 0
    ┗━━━┻   ┻━━━┻━━━┻   ┻ ^ ┻━━━┻   ┻━━━┻━━━┻━━━┻━━━┻ ^ ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
```

### Example 3.2 - Another failure

Here the failure might not be as obvious.  I have provided you with the forensics.  It's up to you to analyze the failure by finding a circuit, or by showing in some other manner that the root is not reachable from every cell.
```
>>> obj = Torus1(8, 13)
>>> print(obj.on())
*** WARNING:  The maze that results might not be connected. ***
          Simple Binary Tree (Torus) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       42
                             tails       42
                      row barriers        8
                   column barriers       13
                     root barriers        1
>>> target = obj.verify()
*** WARNING: the maze is disconnected.
>>> obj.label_barriers()
>>> print(obj.maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏   ┳━━━┳   ┳━━━┳   ┳━━━┳   ┳   ┳━━━┳━━━┳━━━┳━━━┳   ┓
  7 ┃ E ┃       ┃       ┃       ┃   ┃ N                 ┃ 7
    ┣   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  6     ┃               ┃ E ┃   ┃ N       N     ┃         6
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  5       N   N         ┃                     E ┃   ┃     5
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  4 ┃       ┃       ┃                   ┃   ┃ N     ┃ E ┃ 4
    ┣   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━┫
  3     ┃       ┃ E ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ N   3
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
  2     ┃   ┃       ┃   ┃   ┃     E ┃       ┃       ┃     2
    ┣━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  1   N     ┃     B ┃   ┃ N   N         ┃           ┃     1
    ┣   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  0 ┃ E ┃   ┃       ┃ N         ┃               ┃ N     ┃ 0
    ┗   ┻━━━┻   ┻━━━┻   ┻━━━┻   ┻   ┻━━━┻━━━┻━━━┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
>>> print(target.index)
(0, 0)
```

### Example 3.3 - A success

I took several tries to get a perfect maze, but I was able to generate one.
Here is the successful attempt:
```
>>> obj = Torus1(8, 13)
>>> print(obj.on())
*** WARNING:  The maze that results might not be connected. ***
          Simple Binary Tree (Torus) (statistics)
                            visits      105
                             cells      104
                          passages      103
                             heads       45
                             tails       39
                      row barriers        8
                   column barriers       13
                     root barriers        1
>>> target = obj.verify()
```
No warning message from method *verify*... So every cell is reachable from the root.
```
>>> obj.label_barriers()
>>> print(obj.maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳━━━┳   ┓
  7 ┃       ┃       ┃           ┃       ┃     B ┃       ┃ 7
    ┣━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  6 ┃       ┃   ┃   ┃   ┃ N                   E ┃       ┃ 6
    ┣   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━┫
  5     ┃ N                 ┃   ┃     E ┃   ┃   ┃   ┃     5
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━┫
  4               N       E ┃       ┃   ┃   ┃   ┃   ┃     4
    ┣   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  3     ┃       ┃   ┃           ┃ E ┃           ┃   ┃ N   3
    ┣   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━┫
  2     ┃     E ┃   ┃       ┃     N     ┃   ┃   ┃   ┃     2
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  1   N       N       N     ┃ N     ┃   ┃ N     ┃ E ┃     1
    ┣   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
  0 ┃   ┃       ┃ E ┃   ┃   ┃   ┃     N         ┃ N     ┃ 0
    ┗━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻━━━┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
```
And here is the value of *target*:
```
>>> print(target)
None
```
All the cells are reachable from the root cell (labelled "B"), so the maze is connected.  Since the number of passages is one less than the number of cells, the maze is minimally connected, and thus forms a tree.  The maze is a perfect maze, or equivalently, using the language of graph theory, it is a spanning tree.