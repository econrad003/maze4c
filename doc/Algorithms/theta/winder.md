# The Polar Winder Algorithms

The polar analogues of sidewinder are inwinder and outwinder.  They are built using the same foundation as the polar analogue of the simple binary binary tree.

## The algorithm

As with sidewinder, we keep track of runs in the onward direction (clockwise or counterclockwise).  Privileged cells and lateral flow are as in the polar version of simple binary tree.

*  Closing the run:  if the run is not empty, we choose one of the cells and carve a passage in the rise direction (inward for inwinder, or outward for outwinder).  We then empty the run.

When we visit a cell, we first extend the run by adding (cell, neighbor) pairs for each neighbor in the rise direction.

The decision tree is roughly the same as that for a simple binary tree:

*  In a privileged cell, we close the run.
*  For other cells when the run is not empty, we toss a coin: (head) close out the run, or (tail) carve a passage onward.
*  For non-privileged cells when the run is empty, we simply carve a passage onward.

## Example 1 - Outwinder

As usual we first create a grid and incorporate in into a maze object:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.polar import ThetaGrid
    2> from mazes.maze import Maze
    3> maze = Maze(ThetaGrid(5))
```

Next we run the maze carving algorithm:
```
    4> import mazes.Algorithms.polar.winder as wnd
    5> print(wnd.Outwinder.on(maze))
          Polar Outwinder (statistics)
                            visits      119
                             cells      114
                          passages      113
                    rise direction  outward
                              bias        0.5000
```

We create a sketch of the maze...
```
    6> from mazes.Graphics.polar1 import Pholcidae
    7> spider = Pholcidae(maze)
    8> spider.setup()
    9> spider.title("Outwinder")
    10> spider.draw_maze()
    11> spider.show()
```
A copy of the sketch for the run above is found in the gallery as:

*   *gallery/theta/outwinder\_1A.png*

Note the long open corridor in the outermost ring.  This is a standard feature of outwinder.  In outwinder, if the outermost ring has more than one cell, then it will have exactly one wall.

And we also create a linewise sketch...
```
    12> from mazes.Graphics.polar2 import SpiderWeb
    13> spider = SpiderWeb(maze)
    14> spider.setup()
    15> spider.title("Outwinder")
    16> spider.draw_maze()
    17> spider.show()
```
A copy of the sketch for the run above is found in the gallery as:

*   *gallery/theta/outwinder\_1B.png*

In this figure, note the four line segments that meet in a single point in roughly the 9 o'clock position.  The point is a cell in ring 2 with four neighbors -- this maze is a tree but not not a binary tree.

## Example 2 - Inwinder

We continue the session with inwinder.  (The imports won't be repeated.)  First we prepare a grid and carver the maze:

```
    18> maze = Maze(ThetaGrid(5))
    19> print(wnd.Inwinder.on(maze))
          Polar Inwinder (statistics)
                            visits      119
                             cells      114
                          passages      113
                    rise direction  inward
                              bias        0.5000
```

Next we sketch the maze.  The figure has been saved as:

*   *gallery/theta/inwinder\_2A.png*

Note here that the outermost ring houses a number of walls, but there is just one wall in the innermost ring. With polar inwinder, the innermost ring is always a path but but not a circuit.  If there is more than one cell, the innermost ring will have exactly one wall.

```
    20> spider = Pholcidae(maze)
    21> spider.setup()
    22> spider.title("Inwinder")
    23> spider.draw_maze()
    24> spider.show()
```

Finally we sketch the linewise representation.  The figure has been saved as:

*   *gallery/theta/inwinder\_2B.png*

```
    25> spider = SpiderWeb(maze)
    26> spider.setup()
    27> spider.title("Inwinder")
    28> spider.draw_maze()
    29> spider.show()
```

There are several degree 4 cells in this particular maze.

## Food for thought

1.  What can you say about the locations of cells of degree 4 or more in the winder algorithms?  For example, can inwinder have cells of degree 4 in the innermost ring? in the outermost ring?  What about outwinder?  What happens when there is a single pole cell?
2.  Why is the outermost ring always a path and never a circuit in outwinder?
3.  Why is the innermost ring always a path and never a circuit in inwinder?
4.  How would you use the implementation (class *ThetaGrid*) to generate a polar grid with 5 rings and just one cell in the outermost ring?  *(Yes, it can be done!)*

(**Spoiler**) For one answer to Question 4, see:

*   *gallery/theta/spoiler1.png*
