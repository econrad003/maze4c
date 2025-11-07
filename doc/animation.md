# Animating an algorithm

## Contents

* Current state
* Example 1 - Depth-first search (animation)
* Example 2 - Breadth-first search (animation)
* Example 3 - Kruskal's algorithm (animation)
* Example 4 - Depth-first forest, 2 unweighted tasks (animation)

## Current state

At present, only linking is fully implemented and tested.  Unlinking and visits might work, but the unlinking has not undergone any testing, and the algorithms themselves do not have the necessary hooks in place to capture visits of cells and joins.

The examples below have been saved in the *movies* folder.

## Example 1 - Depth-first search (animation)

### The output

File: *movies/capture\_DFS.mkv*

### The capture session

#### Part 1 - preparation

```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.Algorithms.dfs_better import DFS
>>> from mazes.Graphics.animation import Animation
>>> maze = Maze(OblongGrid(5, 8))
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

The empty grid shows up in a window 400 pixels wide and 300 pixels high.  (Your results may differ.  In any case, its too big for a 5 row high by 8 column wide maze.  So we manually reduce the window size.

#### Part 2 - setting up for the capture

(We reduced the size of the animation window, so we need to reconfigure so that the maze fits inside the window.  This may involve some trial and error.  Exactly how you approach this will depend on your video capture and video editing software.)
```
>>> spider.configure()
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

#### Part 3 - carving the maze

At this point, I was ready to:

1. run the maze carving algorithm (DFS);
2. set up the video capture software; and
3. create the animation.

For the first of these steps, I use *spider.maze* instead of *maze* in order to capture the *Maze.link()* operations:
```
>>> print(DFS.on(spider.maze))
          Depth-first Search (DFS) (statistics)
                            visits       79
                        start cell  (0, 0)
               maximum stack depth       30
                             cells       40
                          passages       39
```

#### Part 4 - Capture and animation

Next I set up my video capture software.  When all is ready, I type:
```
>>> spider.animate()
```

When the maze is complete, I close the turtle graphics window.  My animation software automatically closed the video capture.  Afterwards, I cropped the video and removed the sound track.

### Notes on the *spider.maze* object

The *spider.maze* object has type AnimatedMaze, a class derived from class Maze and which uses the class Maze interface to link and unlink passages.  So for all practical purposes, *spider.maze* and *maze* are the same maze even though they are different objects.  Here's what happens if I *print* them:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+
|               |               |
+   +---+---+   +   +   +---+---+
|   |   |       |   |           |
+   +   +   +---+   +---+---+   +
|   |   |   |       |           |
+   +   +   +---+---+   +---+   +
|   |       |           |   |   |
+   +   +---+   +---+---+   +   +
|   |           |               |
+---+---+---+---+---+---+---+---+
>>> print(spider.maze)
+---+---+---+---+---+---+---+---+
|               |               |
+   +---+---+   +   +   +---+---+
|   |   |       |   |           |
+   +   +   +---+   +---+---+   +
|   |   |   |       |           |
+   +   +   +---+---+   +---+   +
|   |       |           |   |   |
+   +   +---+   +---+---+   +   +
|   |           |               |
+---+---+---+---+---+---+---+---+
```
They look exactly the same.  But if I call *maze.link()*, the passage carving is not tracked.

### Notes on the video

Note how, as the maze is created, passages are carved one after another in a long winding chain.  (That's why it is "depth-first".)  When the end of the chain has nowhere to go, the algorithm jumps back to the last place in the chain where it can carve onward.

## Example 2 - Breadth-first search (animation)

### The output

File: *movies/capture\_BFS.mkv*

### The capture session

Session:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.Algorithms.bfs import BFS        # <--- Note!
>>> from mazes.Graphics.animation import Animation
>>> maze = Maze(OblongGrid(5, 8))
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

Here we fiddled with the window:
```
>>> spider.configure()
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

And here we carved the maze
```
>>> print(BFS.on(spider.maze))
          Breadth-first Search (BFS) (statistics)
                            visits       40
                        start cell  (4, 4)
              maximum queue length        9
                             cells       40
                          passages       39
```

Here we fiddled with the video capture software.  And then:
```
>>> spider.animate()
```

### Notes on the video

Note that the algorithm sends out feelers in every possible direction, one step at a time.  ("Breadth-first."  Get it?)

## Example 3 - Kruskal's algorithm (animation)

### The output

File: *movies/capture\_Kruskal.mkv*

### The capture session

Session:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.Algorithms.kruskal import Kruskal       # <-- NOTE!
>>> from mazes.Graphics.animation import Animation
>>> maze = Maze(OblongGrid(5, 8))
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
>>> spider.configure()                        # resizing happens here!
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
     # CARVE THE MAZE.
>>> print(Kruskal.on(spider.maze))
          Kruskal (statistics)
                            visits       59
                 components (init)       40
               queue length (init)       67
                             cells       40
                          passages       39
                components (final)        1
              queue length (final)        8
     # SET UP THE VIDEO CAPTURE SOFTWARE...
     # NOW START THE ANIMATION.
>>> spider.animate()
```

### Notes on the video

The growing tree algorithms all start at one points (the "seed") and "grow the tree" from the seed.  The tree is extended one cell at a time, with a passage connecting the added cell to some cell already in the tree.  It is generally easy to show that, if the grid is connected and the growing tree algorithm meets a few simple conditions, then the algorithm terminates with a spanning tree.  The conditions are:

1. each cell in the queue is either already in the tree or is adjacent to a cell already in the tree;
2. whenever a cell not in the tree is visited, it is added to the tree;
3. already visited cells are not added; and
3. every cell is eventually visited.

Growing tree algorithms are characterized by the queuing structure which holds the tree's frontier.  They differ primarily in the organization of the queue -- DFS uses a stack, BFS a queue, Prim's algorithm a priority queue.  In addition, the queuing structure might work with cells, or it might instead work with grid edges.

Some other algorithms, like the first-entrance random walk algorithm (Aldous/Broder), meet some similar conditions, essentially growing a tree one cell at a time.  But they might lack some feature of a growing tree algorithm.  For example, Aldous/Broder doesn't use a queuing structure.  Wilson's algorithm tries to find a path to the growing tree, then adds cells from the reversed path one at a time, so it falls in this category.

Kruskal's algorithm is completely different.  It simply carves passages in grid edges wherever it can (without creating circuits).  By the time it runs out of grid edges (and usually before then), the algorithm has managed to turn a forest with many little trees into a single tree.  Perhaps a more apt analogy for Kruskal's algorithm is the mycelial network that starts as a number of fungal spores.  The growing forest algorithms are a sort of synthesis which takes some of the fungal features of Kruskal's algorithm and weds them with features of a growing tree.

## Example 4 - Depth-first forest, 2 unweighted tasks (animation)

### The output

File: *movies/capture\_DFF.mkv*

### The capture session

Session:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.Algorithms.dff import DFF     # <--- NOTE!
>>> from mazes.Graphics.animation import Animation
>>> maze = Maze(OblongGrid(5, 8))
>>> spider = Animation(maze)
Verbose mode: hints will be displayed...
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
```

After resizing the turtle graphics window:
```
>>> spider.configure()
Spider setup in progress. Please stand by...
Spider setup complete...
Run your algorithm using 'spider.maze'
Then run the animation: spider.animate()
>>> print(DFF.on(spider.maze))
          Depth-first Forest (DFF) (statistics)
                            visits       80
                             tasks        2
                             seeds  [(1, 2), (2, 1)]
                             cells       40
                          passages       39
                      border edges        7
                      accept edges        1
                      reject edges        0
                            task 0  push(25), pop(25), max(19)
                            task 1  push(15), pop(15), max(10)
                     snake lengths  (25, 15)
```

After setting up the video capture software:
```
>>> spider.animate()
```

### Notes on the video

Note the two depth-first searches running in parallel using an unweighted tournament.  The tree on the right happened to get more turns, but that was largely just the result of the proverbial flips of a coin.  Eventually one of the two trees had no place to go, so its task was removed from the scheduler.  After the second tree had exhausted the cells, one last passage was carved to connect the two trees.

Here is the analogy: The two trees were built using a growing tree algorithm.  That final passage connecting them is the mycelial network through which the two trees communicate.

Carrying the analogy further, with three trees, the mycelial network would consist of two passages.