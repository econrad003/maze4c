# Simple Binary Tree as a wall builder

For an introduction to wall building, refer to the file *README.md* in this folder.

## Contents

1. Craft a simple binary tree by erecting walls
2. Options
3. Animation

## Craft a simple binary tree by erecting walls

We start with some imports:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.WallBuilders.simple_binary_tree import BinaryTree
```

Next we create a maze object:
```
>>> maze = Maze(OblongGrid(5, 8))
```

Depending on our application, we might want to start with an empty maze or a complete maze.  If we want the latter, we can use the *link\_all* method in class maze:
```python
         maze.link_all()
```
Since we're simply crafting a simple binary tree, we'll let the class *BinaryTree* handle the details:
```
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (Wall Builder) (statistics)
                            visits       41
                             links       67
                             cells       40
                             walls       28
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
```
The options are as for the passage carving version in the *mazes.Algorithms* folder.  But, as we are erecting walls instead of carving passages, the bias option has a different effect.

The links statistic (links=67) tells us that 67 passages were carved to create a complete maze.  Since we started with an empty maze, that's one for each edge in the grid. 28 walls were erected, or in other words, 28 passages were removed leaving 39 passages in the crafted maze.

Here is the result:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+
|                               |
+   +   +---+   +---+   +---+   +
|   |   |       |       |       |
+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |
+---+---+---+   +---+---+   +   +
|               |           |   |
+---+   +   +   +   +   +---+   +
|       |   |   |   |   |       |
+---+---+---+---+---+---+---+---+
```

## Options

Here are the principle options -- results of the *help* text were edited for brevity:
```
>>> help(BinaryTree.Status.parse_args)
Help on function parse_args in module mazes.WallBuilders.simple_binary_tree:

    parse constructor arguments

    POSITIONAL ARGUMENTS

        maze - handled by __init__ in the base class.

    KEYWORD ARGUMENTS

        onward - the onward direction (tail). The default is "east".

        upward - the upward direction (head). The default is "north".

        bias - the probability of a head.  The default is 0.5 in
            'cointoss'.  This argument is passed to flip, if present.

        randomize (default False) - if True, the grid is shuffled
            to get a new iteration order. (This option is primarily
            for demonstation purposes.)
```
Since the coin toss determines placement of a wall instead of a passage, the effect of the bias argument is inverted from its passage carving counterpart.  Here we use a bias of 10%, so roughly 10% of the coin tosses are heads:
```
>>> maze = Maze(OblongGrid(5, 8))
>>> print(BinaryTree.on(maze, bias=0.1))
          Simple Binary Tree (Wall Builder) (statistics)
                            visits       41
                             links       67
                             cells       40
                             walls       28
                          passages       39
                            onward  east
                            upward  north
                              bias        0.1000
>>> print(maze)
+---+---+---+---+---+---+---+---+
|                               |
+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |
+   +   +   +   +---+   +   +   +
|   |   |   |   |       |   |   |
+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```
We erect a wall to the north on a head and a wall to the east on a tail.  There are far fewer heads, so most of the passages run north as east was more likely to be blocked.

Here is how the passage carver handles the same bias:
```
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree as PassageCarver
>>> maze = Maze(OblongGrid(5, 8))
>>> print(PassageCarver.on(maze, bias=0.1))
          Simple Binary Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.1000
>>> print(maze)
+---+---+---+---+---+---+---+---+
|                               |
+---+---+---+---+---+---+---+   +
|                               |
+---+---+---+---+---+---+   +   +
|                           |   |
+---+---+---+---+---+   +---+   +
|                       |       |
+---+---+---+---+---+---+---+   +
|                               |
+---+---+---+---+---+---+---+---+
```
In the passage carver, we carve a passage to the north on a head and a passage to the east on a tail.  There are far fewer heads, so most of the passages run east.

## Animation

### The output

File: *movies/capture-BinTree-r-wb.mkv*  (wall builder)

### The video capture session

We start by creating a complete maze on a grid:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> maze = Maze(OblongGrid(5, 8))
>>> maze.link_all()     # complete maze on the grid
```
The main reason we want a complete maze is that we only want to see unlinks in the animation.  So we link the grid ahead of the animation.

Next we prepare the animation:
```
>>> from mazes.Graphics.animation import Animation
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```
Cells (small squares) and the passages (line segments) that connect them are painted in black.  (This takes some time.)

We manually resize the drawing canvas to make the maze smaller -- that requires reconfiguration:
```
>>> spider.configure()
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

Next we run the wall builder on the *AnimatedMaze* object (*spider.maze*).  Since the algorithm doesn't actually depend on the order in which cells are traversed, we shuffle the grid using the *randomize* option:
```
>>> from mazes.WallBuilders.simple_binary_tree import BinaryTree
>>> print(BinaryTree.on(spider.maze, randomize=True))
          Simple Binary Tree (Wall Builder) (statistics)
                            visits       41
                             links        0
                             cells       40
                             walls       28
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
>>> print(maze)
+---+---+---+---+---+---+---+---+
|                               |
+   +---+   +---+---+---+   +   +
|   |       |               |   |
+---+   +   +---+---+---+---+   +
|       |   |                   |
+---+   +   +---+   +   +---+   +
|       |   |       |   |       |
+   +   +---+---+---+---+---+   +
|   |   |                       |
+---+---+---+---+---+---+---+---+
```
No links tells us that we started with a complete maze.  28 passages were removed, and 39 passages remain.

At this point we set up the video capture software.  When ready, we type:
```
>>> spider.animate()
```

### Notes on the video

As passages are removed, the endpoint cells turn blue and the connecting line segment is erased.  (Removing a passage is erecting a wall.)  When the 28 walls have been erected, the maze above is left on the screen.  Most, not all, of the cells have turned blue, and some passages (black line segments) remain onscreen.