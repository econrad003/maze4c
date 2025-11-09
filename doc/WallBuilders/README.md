# Wall building - an introduction

Passage carvers start with an empty maze, *i.e.* a maze with no passages, and carve new passages to craft the maze.  Wall builders start with a complete maze, *i.e.* a maze in which every pair of neighbors in the underly grid is linked by a passage, and proceed by removing passages (*i.e.* erecting walls) to craft the maze.

A class *AlgorithmWB*, derived from class *Alogorithm*, is designed to act as a base class for wall building algorithms.  What does it do?  Basically it just makes sure that the maze to be crafted is initially complete.

Here is *AlgorithmWB* in action:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.algorithm_wb import AlgorithmWB
>>> maze = Maze(OblongGrid(5, 6))
>>> print(AlgorithmWB.on(maze))
          wall-building maze algorithm (statistics)
                            visits        0
                             links       49
>>> print(maze)
+---+---+---+---+---+---+
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+---+---+---+---+---+---+
```
As you can see, every grid edge corresponds to a link.  The statistics show 0 visits and 49 links.  There were no visits, so no walls were erected.  The maze was created empty, so *AlgorithmWB* carved 49 passages to form a complete maze.

A complete maze isn't very interesting, so we want to remove passages, *i.e.* erect walls.  We use a class derived from AlgorithmWB:
```
>>> from mazes.WallBuilders.simple_binary_tree import BinaryTree
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (Wall Builder) (statistics)
                            visits       31
                             links        0
                             cells       30
                             walls       20
                          passages       29
                            onward  east
                            upward  north
                              bias        0.5000
```
Note that we started with an already complete maze -- the statistic links=0 tells us that no additional passages were carved.  We started with 49 passages, erected 20 walls, leaving a maze with 29 passages. It's a simple binary tree...
```
>>> print(maze)
+---+---+---+---+---+---+
|                       |
+---+---+---+   +   +   +
|               |   |   |
+   +---+---+   +   +   +
|   |           |   |   |
+   +   +   +   +---+   +
|   |   |   |   |       |
+---+---+---+---+---+   +
|                       |
+---+---+---+---+---+---+
```

The *BinaryTree* class in module *mazes.WallBuilders.simple\_binary\_tree* is derived from *AlgorithmWB*, so we can also start with an empty maze:
```
>>> maze = Maze(OblongGrid(5, 6))
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (Wall Builder) (statistics)
                            visits       31
                             links       49
                             cells       30
                             walls       20
                          passages       29
                            onward  east
                            upward  north
                              bias        0.5000
>>> print(maze)
+---+---+---+---+---+---+
|                       |
+---+---+   +---+   +   +
|           |       |   |
+   +   +---+---+---+   +
|   |   |               |
+   +---+---+   +   +   +
|   |           |   |   |
+---+   +   +---+   +   +
|       |   |       |   |
+---+---+---+---+---+---+
```

Starting with a complete maze is helpful in animating a wall builder.  For simple maze crafting, with a wall builder derived from class *AlgorithmWB*, it will depend on how the maze is being used.
