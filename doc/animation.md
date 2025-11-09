# Animating an algorithm

## Contents

* Current state
* Example 1 - Depth-first search (animation)
* Example 2 - Breadth-first search (animation)
* Example 3 - Kruskal's algorithm (animation)
* Example 4 - Depth-first forest, 2 unweighted tasks (animation)
* Example 5 - Simplified Prim (animation)
* Example 6 - Simple binary tree (animation)
* Example 7 - Sidewinder (animation)
* Example 8 - Inwinder (animation)
* Example 9 - Outwinder (animation)
* Example 10 - Eller's algorithm (animation)
* Example 11 - Outward Eller (animation)
* Example 12 - Recursive Division (animation)

Example 1 lays out the basics for producing an animation.  Examples 2 and 3 show the entire session, but give a briefer summary of the mechanics.  The remaining examples only show points where the details of the production session differ.

In each example, following the production session, there is some "discussion" of the results that can be seen in the video.  I suggest viewing the video first before and again as you read the discussion.

## Current state

At present, only linking is fully implemented and tested.  Unlinking and visits might work, but the unlinking has not undergone any testing, and the algorithms themselves do not have the necessary hooks in place to capture visits of cells and joins.

The examples below have been saved in the *movies* folder.

## Example 1 - Depth-first search (animation)

### The outputs

File #1: *movies/capture-DFS.mkv* (shuffled)
File #2: *movies/capture-DFS-ns.mkv* (unshuffled)
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

### The second animation

Session notes:

The session used to produce the second video differed in how depth-first search was called, specifically with the *shuffle* option set to *False*.  Here is the call and the status display:
```
>>> print(DFS.on(spider.maze, shuffle=False))
          Depth-first Search (DFS) (statistics)
                            visits       79
                        start cell  (1, 3)
               maximum stack depth       38
                             cells       40
                          passages       39
```

Note that the maximum stack depth here was 38, so the diameter has a length of 37 passages.  The first session, with shuffling produced a maze with a diameter of 29 passages.  (The maximum diameter for a maze on a 5×8 rectangular grid is 39 passages -- there are a number of ways to produce a labyrinth with this maximum.)

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

### Notes on the videos

Note how, as the maze is created, passages are carved one after another in a long winding chain.  (That's why it is "depth-first".)  When the end of the chain has nowhere to go, the algorithm jumps back to the last place in the chain where it can carve onward.  In the first video, using shuffling, the first chain managed to "paint itself into a corner" fairly early.  In the second video, without shuflling the chain was much longer.

### Note on maximum diameter

It was noted above that an 5×8 rectangular maze has a maximum diameter of 39 passages.  In short, a diameter path spans all 40 cells.  It was also noted that the maximum can be achieved in many ways.  Here are just a few:

```
mainly horizontal                     mainly vertical
+---+---+---+---+---+---+---+---+     +---+---+---+---+---+---+---+---+
|                             T |     |       |       |       |       |
+   +---+---+---+---+---+---+---+     +   +   +   +   +   +   +   +   +
|                               |     |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+   +     +   +   +   +   +   +   +   +   +
|                               |     |   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+---+     +   +   +   +   +   +   +   +   +
|                               |     |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+   +     +   +   +   +   +   +   +   +   +
| S                             |     | S |       |       |       | T |
+---+---+---+---+---+---+---+---+     +---+---+---+---+---+---+---+---+

spiral                                haphazard
+---+---+---+---+---+---+---+---+     +---+---+---+---+---+---+---+---+
|                               |     |       |               |       |
+   +---+---+---+---+---+---+   +     +   +   +   +---+---+   +   +   +
|   |                       |   |     |   |       |       |   |   |   |
+   +   +---+---+---+---+   +   +     +   +---+---+   +   +   +   +   +
|   |   |             T |   |   |     |       |       |   |       |   |
+   +   +   +---+---+---+   +   +     +---+   +   +---+   +---+---+   +
|   |   |                   |   |     |       |   |       |       |   |
+   +   +---+---+---+---+---+   +     +   +---+   +   +---+   +   +   +
| S |                           |     | S | T     |           |       |
+---+---+---+---+---+---+---+---+     +---+---+---+---+---+---+---+---+
```
In each of the four example, the ends of the chains, the terminal cells, are labelled *S* and *T*.  Note that if one starts at either end of the chain, to get to the other end, each step offers exactly one choice.  (Retracing one's steps is not counted as a choice.)  A maze consisting largely of degree 2 cells is typically referred to as a *labyrinth*.

## Example 2 - Breadth-first search (animation)

### The output

File: *movies/capture-BFS.mkv*

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

File: *movies/capture-Kruskal.mkv*

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

File: *movies/capture-DFF.mkv*

### Capture session highlights

*   Import *DFF* as the algorithm:
```
        >>> from mazes.Algorithms.dff import DFF
```

*   After configuring, run *DFF*:
```
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

### Notes on the video

Note the two depth-first searches running in parallel using an unweighted tournament.  The tree on the right happened to get more turns, but that was largely just the result of the proverbial flips of a coin.  Eventually one of the two trees had no place to go, so its task was removed from the scheduler.  After the second tree had exhausted the cells, one last passage was carved to connect the two trees.

Here is the analogy: The two trees were built using a growing tree algorithm.  That final passage connecting them is the mycelial network through which the two trees communicate.

Carrying the analogy further, with three trees, the mycelial network would consist of two passages.

## Example 5 - Simplified Prim (animation)

### The output

File: *movies/capture-sPrim.mkv*

### Capture session highlights

*   Import *NotPrim* (*i.e.* simplified Prim) as the algorithm:
```
        >>> from mazes.Algorithms.simplified_Prim import NotPrim
```

*   Run *NotPrim* on the configured maze:
```
        >>> print(NotPrim.on(spider.maze))
          Simplified "Prim" (statistics)
                            visits       79
                        start cell  (2, 6)
               maximum list length       16
                             cells       40
                          passages       39
```

### Notes on the video

Simplified Prim is a growing tree algorithm which grows the tree by adding a *random* frontier cell to the tree.  On average, the trees will be more like BFS search trees than DFS search trees in that branches leading from the starting cell tend to be short instead on long.

A BFS search tree always produces branches of minimum length -- use of a FIFO queue is enough to guarantee that branch lengths are never more than the grid distance.  A simplified Prim search tree will, on average, produce branches close to minimum length -- randomizing retrieval from its queue allow branches to get longer than the grid distamce.  A DFS search attempts to produce branches of maximum length -- use of a stack (LIFO) makes branches shoot as far a possible, but sometimes a branch manages to "paint itself into a corner".

## Example 6 - Simple binary tree (animation)

### The output

File: *movies/capture-BinTree-r.mkv*

### Capture session highlights

*   Import *Binary* (*i.e.* simple binary tree) as the algorithm:
```
        >>> from mazes.Algorithms.simple_binary_tree import BinaryTree
```

*   Run *BinaryTree* on the configured maze.  The *randomize* option is set in order to highlight the cell-independece of the algorithm:
```
>>> print(BinaryTree.on(spider.maze, randomize=True))
          Simple Binary Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
```

### Notes on the video

Note how passages pop up in with cells in pairs running either west to east or south to north.  The direction (either east or north) is determined by the first cell in the pair (respectively either to the left or below).  Without the *randomize* option (and depending on how dictionaries happen to be implemented in a particular version of *Python*), this behavior might be less apparent.

## Example 7 - Sidewinder (animation)

### The output

File: *movies/capture-sidew.mkv*

### Capture session highlights

*   Import *Sidewinder* as the algorithm:
```
        >>> from mazes.Algorithms.sidewinder import Sidewinder
```

*   Run *Sidewinder* on the configured maze:
```
        >>> print(Sidewinder.on(spider.maze))
          Sidewinder Tree (statistics)
                            visits       41
                             cells       40
                          passages       39
                            onward  east
                            upward  north
                              bias        0.5000
```

### Notes on the video

Sidewinder works independently in rows, but within a given row, cells are dependent.  For this demonstration, rows are processed from south upward, but this is just an artifact of the way the algorithm was implemented.

Within a given row, cells are process from left to right (*i.e.* eastward).  Eastward passages are added for a few cells to create a run, and then a northward passage (*i.e.* a rise) is carved from somewhere in the run.

## Example 8 - Inwinder (animation)

### The output

File: *movies/capture-inw.mkv*

### Capture session highlights

*   Import *Inwinder* as the algorithm:
```
        >>> from mazes.Algorithms.inwinder import Inwinder
```

*   Here we used a larger grid as 5 by 8 isn't really large enough to see what is going on:
```
        >>> maze = Maze(OblongGrid(8, 13))
```

*   Run *Inwinder* on the configured maze:
```
        >>> print(Inwinder.on(spider.maze))
          Inwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       54
                            inward       49
                          backward        0
```

### Notes on the video

Runs in inwinder are in rectangular rings, and rises are perpendicular steps toward the center.  Otherwise the behavior is similar to sidewinder.

## Example 9 - Outwinder (animation)

### The output

File: *movies/capture-outw.mkv*

In the implementation of outwinder, the rings (and thus the *runs*) are processed from the outermost to the innermost.  NOTE, however, that when a run is closed, rises are carved *outward* (not *inward* as in *Inwinder*) to the *previous ring* in the sequence.

The ring order doesn't actually matter -- it is the rise direction that makes a difference.  Outwinder, inwinder, and sidewinder are essentially the same algorithm -- they differ in how rows (where *runs* are placed) and columns (where the *rises* occur).

The ring order is an implementation detail in the algorithm.  It makes no difference in the resulting maze, but it might be confusing when watching the video.

### Capture session highlights

*   Import *Outwinder* as the algorithm:
```
        >>> from mazes.Algorithms.outwinder import Outwinder
```

*   As with *Inwinder* we used a larger grid:
```
        >>> maze = Maze(OblongGrid(8, 13))
```

*   Run *Outwinder* on the configured maze:
```
        >>> print(Outwinder.on(spider.maze))
          Outwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       67
                           outward       36
```

### Notes on the video

Runs in outwinder are in rectangular rings, and rises are perpendicular steps *away from* the center (not *towards* as in inwinder.  The behavior of outwinder, inwinder, and sidewinder is similar -- the main differences is in how rises and runs are defined.

## Example 10 - Eller's algorithm (animation)

### The output

File: *movies/capture-Eller.mkv*

### Capture session highlights

*   Import *Eller* as the algorithm:
```
        >>> from mazes.Algorithms.eller import Eller
```

*   As with *Inwinder* and *Outwinder*, but this time we used portrait mode:
```
        >>> maze = Maze(OblongGrid(13, 8))
```

*   Run *Eller* on the configured maze:
```
        >>> print(Eller.on(spider.maze))
          Martin Eller's Spanning Tree (statistics)
                            visits       13
                             cells      104
                          passages      103
               optional merge left       34
               required merge left        2
             required carve upward       48
             optional carve upward       19
                            onward  east
                            upward  north
```

### Notes on the video

Eller's algorithm proceeds row by row from south to north.  Like Kruskal's algorithm, it creates forests.  When the top row is reached, everything gets resolved.

With a minor change to handling the starting row, we could use Eller's algorithm to extend a perfect rectangular maze upward as far as one desires.  In the creation of forests, it is similar to the simple binary tree algorithm, sidewinder (along with inwinder and outwinder), and Kruskal's algorithm.  In fact, there is a deeper relationship expressed by the following diagram:
```
                Kruskal's algorithm           most general
                         |                         |
                 Eller's algorithm                 |
                         |                         |
                    Sidewinder                     |
                         |                         |
                 Simple Binary Tree         most particular
```
As we go down the diagram, we can think of the algorithms below a particular algorithm as special cases.  To turn Kruskal into Eller, we assigning lower priorities to the edges that we need.  To turn Eller into sidewinder, we never carve more than one rise to any given run.  To turn sidewinder into a binary spanning tree algorithm, we never carve a rise from a cell which already has three neighbors.  To get to the simple binary tree algorithm, we always choose the last cell in a run (every run has one, and it doesn't have an eastward neighbor, so perfectly acceptable).

## Example 11 - Outward Eller's algorithm (animation)

### The output

File: *movies/capture-outEller.mkv*

### Capture session highlights

*   Import *OutwardEller* as the algorithm:
```
        >>> from mazes.Algorithms.outward_eller import Eller
```

*   As with *Inwinder* and *Outwinder*, we use a larger grid.  There is no particular reason to go with portrait mode (as with *Eller*), so we go with landscape:
```
        >>> maze = Maze(OblongGrid(8, 13))
```

*   Run *OutwardEller* on the configured maze:
```
        >>> print(Eller.on(spider.maze))
          Outward Eller (statistics)
                            visits        4
                             cells      104
                          passages      103
               optional merge left       45
               required merge left       14
             required carve upward       30
             optional carve upward       14
                            onward  clockwise
                            upward  outward
```

### Notes on the video

Outward Eller algorithm proceeds in rings (as *runs*), carving outward (for *rises*).  Like Eller's basic algorithm, it creates forests.  Special handling of the outermost ring connects the trees in the forest (like fungal mycelia) to create a single tree.

As with Eller's algorithm, it is possible to extend a perfect rectangular maze using outward Eller, but instead of extending just upward, the extension is outward in rectangular rings.  (This would require some change in the coding.) Also as with Eller's algorithm, there is a hierarchy:
```
                Kruskal's algorithm           most general
                         |                         |
                  Outward Eller's                  |
                         |                         |
                     Outwinder              most particular
```
(There are a few implementation difficulties that need to be resolved, but there is also an outward analogue of the simple binary tree algorithm.

## Example 12 - Recursive division algorithm (animation)

Note that the implementation here is a passage carver.  (Recursive division is more commonly implemented as a wall builder.)

### The output

File: *movies/capture-rdiv.mkv*

### Capture session highlights

*   Import *RecursiveDivision* as the algorithm:
```
        >>> from mazes.Algorithms.recursive_division import RecursiveDivision
```

*   We use a larger square grid for the animation:
```
        >>> maze = Maze(OblongGrid(13, 13))
```

*   Run *RecursiveDivision* on the configured maze:
```
        >>> print(RecursiveDivision.on(spider.maze))
          Recursive Division (statistics)
                            visits      337
                             cells      169
                          passages        0
                             links      168
                           unlinks        0
                             doors      168
                         max stack       10
```

### Notes on the video

In its passage carver implementation, recursive division carves doors.  In our implementation, we have:

1.   divide the room into two parts;
2.   carve a connecting door.
3.   push the first room onto the stack;
4.   push the second room onto the stack.

The algorithm starts by pushing the grid onto the stack.  So the first door carved is the door that divides the entire grid.  The second room in the grid is either north or east of the first room, so the second door carved will be either somewhere roughly north or east of the first door.  In general, the implementation carves its passages from north and east to south and west.

The algorithm creates and joins forests like Kruskal's algorithm, so Kruskal's algorithm can be thought of as a generalization.


