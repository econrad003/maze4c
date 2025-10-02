# DFF - Depth-first forest (DFS with multiple seeds)

## Description

Suppose we have several simultaneous depth-first searches in progress on the same grid.  As each cell is visited, it is claimed by its respective task (or *snake* or *tree*).  The only rule here is that a cell may only be claimed by one task.  At the end of this process, we have a forest of search trees (or a *nest of snakes*).  To turn this forest into a tree, we need to add some additional edges.

That, in a nutshell, is the depth-first forest algorithm, the first in a family of growing forest algorithms.

### Background

Although the algorithm is not described in his book, maze guru Jamis Buck has an example on the following web page:

* "Maze Algorithms."  URL: [https://www.jamisbuck.org/mazes/](https://www.jamisbuck.org/mazes/)  (Accessed 29 September 2025)

Look for the display entitled "Recursive Backtracking (Parallel Seeds)".

The DFF algorithm is my implementation of this maze carver.

## Example 1 - a small example with a lot of analysis

We start in the Python interactive shell with some imports:
```
$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.dff import DFF
```
"DFF" stands for depth-first forest.

We create a *Maze* object and carve the maze:
```
>>> maze = Maze(OblongGrid(5, 5))
>>> print(DFF.on(maze, 3, label=True))
          Depth-first Forest (DFF) (statistics)
                            visits       50
                             tasks        3
                             seeds  [(0, 0), (2, 2), (2, 3)]
                             cells       25
                          passages       24
                      border edges       10
                      accept edges        2
                      reject edges        0
                            task 0  push(7), pop(7), max(5)
                            task 1  push(10), pop(10), max(8)
                            task 2  push(8), pop(8), max(8)
                     snake lengths  (7, 10, 8)
```
When calling *DFF.on*, we supplied the empty maze.  We also specified that we wanted three tasks, and we wanted *snakes* to be labelled.  (The label option is intended primarily for debugging, but it can be useful for documentation.)

Before analyzing the statistics, let's look at the output:
```
>>> print(maze)
+---+---+---+---+---+
| 1   1   1   1   1 |
+   +---+   +---+---+
| 1 | 1   1 | 2   2 |
+   +   +---+---+   +
| 0 | 1   1 | 2 | 2 |
+   +---+---+   +   +
| 0   0   0   2 | 2 |
+---+   +   +   +   +
| 0   0 | 0 | 2   2 |
+---+---+---+---+---+
```
From the statistics, we had 50 *visits* with 25 cells and we created 24 passages.  (Some of the visits were unproductive.)

The cells claimed by our three tasks are labelled 0, 1 and 2 in the display.  Task 0 started with the cell in the lower left.  Task 1 started with the cell in the center (coordinates (2,2)).  Task 3 started to the immediate right in cell (2,3).

For a spanning forest with 3 trees, a 25-cell maze would have 25-3=22 passages.  Notice that the total number of passages is 24, so two passages were added to connect the trees.  (The two added passages show up in the statistics as "accept edges".)

After the snake tasks have completed, we have ten border edges, as labelled below from a through j:
```
+---+---+---+---+---+
|                   |
+   +---+   +-a-+-b-+
|   |       d       |
+ c +   +---+---+   +
|   e       h   |   |
+   +-f-+-g-+   +   +
|           i   |   |
+---+   +   +   +   +
|       |   j       |
+---+---+---+---+---+
```
Passages were carved in two of these edges, namely c (connecting snakes 0 and 1) and i (connecting snakes 0 and 2).  Kruskal's algorithm was used to select these two edges.  These two edges were the first two edges in the sequence (as no edges were rejected).  Once the maze became connected, there was no reason to try any more edges.

The task statistics tell us a bit more.  In each visit, we inspect the top cell in the task's stack.  One of three things can happen:

* the task's stack is empty, in which case we remove the task from the scheduler;
* we spot an unvisited neighbor, in which case we push that neighbor onto the task's stack, and we claim the cell for the task's snake;
* we fail to find any visited neighbors, in which case we remove the cell from the task's stack.

The process is started by pushing the first cell in each snake onto the stack in the corresponding task.

The number of pushes for a task is the number cell in the corresponding snake.  If the grid is connected, the total number of pushes is equal to the number of cells.

Each cell that is pushed is eventually popped, so pushes = pops.  The "max" statistic tells us the size of the queue,  This is the length of the longest path from the seed. The current contents of the stack are the current path from the seed -- this is true only because the stack is a LIFO structure,

## Example 2 - a larger example (with less analysis)

In this example, we create a 3-seed DFF maze with weights.  The weights are a max-priority system -- a task with weight 5 has, on average, 5 times the probability of having the next turn as a task with weight 1.

```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(DFF.on(maze, 3, weights=[5, 3, 1]))
          Depth-first Forest (DFF) (statistics)
                            visits      208
                             tasks        3
                             seeds  [(5, 8), (2, 10), (7, 4)]
                             cells      104
                          passages      103
                      border edges       24
                      accept edges        2
                      reject edges        4
                            task 0  push(67), pop(67), max(45)
                            task 1  push(31), pop(31), max(28)
                            task 2  push(6), pop(6), max(5)
                     snake lengths  (67, 31, 6)
```
Task 0 with weight 5 claimed the majority of the cells.  Task 1 with weight 3 claimed more cells than task 2 with weight 1.

Task 0 had 5/9 or about 55% of the total task weight and claimed 67/104 or 
about 64% of the cells.

Here is the maze.
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       |                   |       |
+---+---+---+---+   +---+---+---+---+   +   +   +---+
|                           |           |   |       |
+---+   +---+---+---+---+   +   +---+---+   +---+   +
|       |       |       |       |       |           |
+   +---+   +   +   +   +---+   +---+   +---+---+   +
|   |       |       |               |       |   |   |
+   +   +---+---+---+---+---+---+---+---+   +   +   +
|   |   |       |                   |       |       |
+   +---+   +   +   +---+---+---+   +   +---+---+   +
|           |       |           |               |   |
+---+---+---+---+---+   +---+   +---+---+---+   +---+
|   |               |   |           |       |       |
+   +   +---+   +---+   +   +---+---+   +   +---+   +
|           |           |               |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 3 - defaults

If we just supply the maze, the implementation supplies two equally weighted tasks with random seeds.
```
>>> maze = Maze(OblongGrid(5, 8))
>>> print(DFF.on(maze)); print(maze)
          Depth-first Forest (DFF) (statistics)
                            visits       80
                             tasks        2
                             seeds  [(0, 3), (2, 5)]
                             cells       40
                          passages       39
                      border edges       14
                      accept edges        1
                      reject edges        0
                            task 0  push(15), pop(15), max(11)
                            task 1  push(25), pop(25), max(15)
                     snake lengths  (15, 25)
+---+---+---+---+---+---+---+---+
|   |                           |
+   +   +---+---+   +---+---+   +
|       |       |       |       |
+   +---+   +---+---+   +   +---+
|   |               |   |       |
+   +   +---+   +---+---+---+   +
|   |   |   |           |   |   |
+   +   +   +---+   +---+   +   +
|   |       |                   |
+---+---+---+---+---+---+---+---+
```

## Example 4 - seeds

We can specify seeds for one or more tasks.  These are supplied as a list.
```
>>> maze = Maze(OblongGrid(5, 8))
>>> seed1=maze.grid[0,0]
>>> seed1.label="1"
>>> seed2=maze.grid[4,7]
>>> seed2.label="2"
>>> print(DFF.on(maze, 3, seeds=[seed1,seed2])); print(maze)
          Depth-first Forest (DFF) (statistics)
                            visits       80
                             tasks        3
                             seeds  [(0, 0), (4, 7), (1, 6)]
                             cells       40
                          passages       39
                      border edges       19
                      accept edges        2
                      reject edges        0
                            task 0  push(8), pop(8), max(7)
                            task 1  push(17), pop(17), max(17)
                            task 2  push(15), pop(15), max(12)
                     snake lengths  (8, 17, 15)
+---+---+---+---+---+---+---+---+
|                           | 2 |
+---+---+---+   +   +---+---+   +
|           |   |           |   |
+---+   +   +---+   +---+   +   +
|       |   |       |       |   |
+   +---+   +   +   +   +---+   +
|   |           |   |       |   |
+   +   +---+---+   +---+---+   +
| 1 |           |               |
+---+---+---+---+---+---+---+---+
```
Since we specified three tasks, a seed was randomly generated for the third task.

## Example 5 - BFF (breadth-first forest and other queuing structures)

I hinted in the introduction that DFF is just one of a large number of a growing forest family of algorithms.  If we replace stacks by queues in DFF,
we have a new algorithm, namely BFF - *breadth-first forest*.

(And, no, BFF is not my best friend forever...  Sorry, but I couldn't let that horrid pun slide.)

In any case, everything is in place to turn DFF into BFF.  We first need two more imports:
```
>>> from mazes.Algorithms.dff import Task
>>> from mazes.Queues.queue import Queue
```

We need to create our tasks beforehand so that they use queues instead of stacks:
```
>>> task0 = Task(0, QueueType=Queue)
>>> task1 = Task(1, QueueType=Queue)
>>> task2 = Task(2, QueueType=Queue)
```

Now for our maze:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(DFF.on(maze, task0, task1, task2))
          Depth-first Forest (DFF) (statistics)
                            visits      208
                             tasks        3
                             seeds  [(2, 2), (2, 1), (3, 7)]
                             cells      104
                          passages      103
                      border edges       22
                      accept edges        2
                      reject edges        0
                            task 0  push(21), pop(21), max(8)
                            task 1  push(23), pop(23), max(6)
                            task 2  push(60), pop(60), max(13)
                     snake lengths  (21, 23, 60)
```

The seeds were randomly chosen.  Tasks 0 and 1 have seeds that are addjacent, so we can expect that their snakes (or BFS search trees) will quickly collide.  Task 2 starts away from the other two, so its search tree has more room to grow unimpeded.  Let's see what actually unfolds -- I've labelled the seeds for reference:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                           |   |                   |
+---+   +---+---+   +---+---+   +   +---+---+---+---+
|           |   |       |   |                       |
+---+   +---+   +---+   +   +   +---+---+---+---+---+
|       |   |       |   |   |                       |
+---+   +   +   +---+   +   +   +---+---+---+---+---+
|       |   |       |   |   |                       |
+---+   +   +   +---+   +   +   +---+---+---+---+---+
|       |           |         2                     |
+---+   +   +---+---+---+   +   +   +   +---+---+---+
|     1 | 0         |       |   |   |               |
+   +   +   +   +---+---+   +   +   +   +   +---+---+
|   |       |           |   |   |   |   |           |
+   +   +   +   +   +   +   +   +   +   +   +---+---+
|   |   |   |   |   |   |   |   |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Indeed, task 2 claimed all of the east half of the maze for itself.  The three tasks fought fiercely to stake their claims in the right half.

## Example 6 - BFS vs DFS, a tale of four battles

Study the four examples that follow and make some conjectures.  Then test your conjectures with more experiments.

### Example 6a - BFS vs DFS, all things being equal

Breadth-first search tends to work in a small area, close to home, while depth-first search likes to wander near and far.  What happens if we start them close to each other and set them loose?

We'll start from scratch.  First we run the Python interpreter and import some classes:
```
$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.dff import DFF, Task
>>> from mazes.Queues.queue import Queue
>>> from mazes.Queues.stack import Stack
```

Any grid can be used but we'll use the usual Von Neumann (N/S/E/W) neigborhood.  So *OblongGrid* is our grid class.  From the *dff* module we'll need both the *DFF* class for the algorithm and the *Task* class since we need to prepare our classes in advance.  Breadth-first search and depth-first search use a queue and a stack, respectively, so we need the *Queue* class and the *Stack* class.

Let's prepare our two contestants:
```
>>> task0 = Task(0, QueueType=Queue)
>>> task1 = Task(1, QueueType=Stack)
```

The arguments are a task ID and a queue type.  The task ID doesn't actually matter except that it's a required argument.  The implementation renumbers the tasks to meet it's own requirements.  Next we create the grid and designate the seeds.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> seed0 = maze.grid[3, 6]; seed0.label="B"
>>> seed1 = maze.grid[4, 6]; seed1.label="D"
```

Let the games begin!  We call the *DFF.on* method with the maze and the two tasks.  The keyword argument *seeds* specifies the seeds.  In addition, we would like to see the territory claimed by each task, so we use the *label* keyword argument:
```
>>> print(DFF.on(maze, task0, task1, seeds=[seed0, seed1], label=True))
          Depth-first Forest (DFF) (statistics)
                            visits      300
                             tasks        2
                             seeds  [(4, 6), (5, 8)]
                             cells      150
                          passages      149
                      border edges       26
                      accept edges        1
                      reject edges        0
                            task 0  push(147), pop(147), max(12)
                            task 1  push(211), pop(211), max(69)
                     snake lengths  (50, 100)
```
Depth-first search is a clear winner, seizing twice as much territory as its shy stay-close rival.

Let's label the seeds for emphasis and print the maze:
```
>>> seed0.label, seed1.label = "B", "D"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1   1   1 | 1   1   1   1   1   1   1 | 1   1   1 | 1   1 |
+   +---+   +---+---+---+   +---+---+   +---+   +---+   +   +
| 1 | 1   1   1   1   1   1 | 1   1 | 1   1 | 1 | 1   1 | 1 |
+   +---+   +---+---+---+---+   +   +---+   +   +   +---+   +
| 1   1 | 1 | 1   1   1   1   1 | 1   1 | 1 | 1   1 | 1   1 |
+   +   +---+   +---+---+---+   +---+   +   +---+   +   +---+
| 1 | 1 | 1   1 | 0   0   0 | 1   1 | 1 | 1   1 | 1 | 1   1 |
+   +   +   +---+---+---+   +---+---+   +---+   +---+---+   +
| 1 | 1   1 | 0   0   0   0   0   D | 1   1 | 1   1   1 | 1 |
+   +---+---+---+---+---+   +---+   +---+   +---+---+   +   +
| 1   1 | 1 | 0   0   0   B   0 | 1   1 | 1   1 | 1 | 1 | 1 |
+---+   +   +---+---+---+   +---+---+   +---+   +   +   +   +
| 1 | 1   1 | 0   0   0   0   0   0 | 1   1   1 | 1   1 | 1 |
+   +---+   +---+---+---+   +---+---+---+---+---+---+   +   +
| 1   1 | 1 | 0   0   0   0   0   0   0   0   0   0 | 1   1 |
+   +---+   +---+---+   +   +---+---+---+---+---+---+---+---+
| 1   1   1 | 1 | 0   0 | 0   0   0   0   0   0   0   0   0 |
+   +---+---+   +---+   +   +---+---+---+---+---+---+---+---+
| 1   1   1   1   1 | 0 | 0   0   0   0   0   0   0   0   0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Apparently DFS blocked its rival to the east, north, west and southwest, leaving BFS land-locked in the south and the southeast.  (But be careful! This is a single example!)

We could mitigate this effect, or exaggerate it, by supplying task weights.

### Example 6b - BFS vs DFS, with a handicap

We can reuse the task objects, since both their queues are now empty.  We just need a new maze object:
```
>>> maze = Maze(OblongGrid(10, 15))
>>> seed0, seed1 = maze.grid[4, 6], maze.grid[5,8]
```
The seeds need to be on the correct grid, so we need to reassign them as well.

For the handicap, we will average 2 calls to BFS (task0) to each call to DFS.  So our weights will be 2 and 1:
```
>>> print(DFF.on(maze, task0, task1, seeds=[seed0, seed1],
...       label=True, weights=[2,1]))
          Depth-first Forest (DFF) (statistics)
                            visits      300
                             tasks        2
                             seeds  [(4, 6), (5, 8)]
                             cells      150
                          passages      149
                      border edges       39
                      accept edges        1
                      reject edges        0
                            task 0  push(252), pop(252), max(18)
                            task 1  push(256), pop(256), max(69)
                     snake lengths  (105, 45)
```
With the handicap, BFS now dominates the board...

Let's display the maze:
```
>>> seed0.label, seed1.label = "B", "D"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1   1   1   1 | 1   1   1   1   1 | 1   1   1   1   1   1 |
+---+   +   +---+   +   +---+   +   +   +---+---+   +---+---+
| 1   1 | 1 | 1   1 | 0 | 0 | 1 | 1   1 | 0 | 0 | 1   1   1 |
+   +   +---+   +---+   +   +---+---+---+   +   +---+---+   +
| 1 | 1 | 1   1 | 0 | 0 | 0   0   0   0   0   0   0   0 | 1 |
+   +---+   +---+   +   +   +---+---+---+---+---+   +---+   +
| 1   1   1 | 0   0   0   0   0   0   0 | 1   1 | 0   0 | 1 |
+   +---+---+---+---+---+   +---+---+---+   +   +---+---+   +
| 1 | 0   0   0   0   0   0   0 | D   1   1 | 1   1   1   1 |
+---+---+---+---+---+---+   +---+---+---+---+---+---+---+---+
| 0   0   0   0   0   0   B   0   0   0   0   0   0   0   0 |
+---+---+---+---+   +   +   +   +---+---+---+---+---+---+---+
| 0   0   0   0   0 | 0 | 0 | 0   0   0   0   0   0   0   0 |
+---+---+---+   +   +   +   +   +   +   +---+---+---+---+---+
| 0   0   0   0 | 0 | 0 | 0 | 0 | 0 | 0   0   0   0   0   0 |
+---+---+   +   +   +   +   +   +   +   +---+---+---+---+---+
| 0   0   0 | 0 | 0 | 0 | 0 | 0 | 0 | 0   0   0   0   0   0 |
+---+---+   +   +   +   +   +   +   +   +---+---+---+---+---+
| 0   0   0 | 0 | 0 | 0 | 0 | 0 | 0 | 0   0   0   0   0   0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 6c - BFS vs DFS, with a lessened handicap

Let's reduce the handicap.  Let's try a 4:3 handicap. Make your bets!  The betting is now closed!  We proceed:
```
>>> maze = Maze(OblongGrid(10, 15))
>>> seed0, seed1 = maze.grid[4, 6], maze.grid[5,8]
>>> print(DFF.on(maze, task0, task1, seeds=[seed0, seed1],
...       label=True, weights=[4,3]))
          Depth-first Forest (DFF) (statistics)
                            visits      300
                             tasks        2
                             seeds  [(4, 6), (5, 8)]
                             cells      150
                          passages      149
                      border edges       19
                      accept edges        1
                      reject edges        0
                            task 0  push(333), pop(333), max(18)
                            task 1  push(325), pop(325), max(69)
                     snake lengths  (81, 69)
```
Make a conjecture...

And the results:
```
>>> seed0.label, seed1.label = "B", "D"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0   0   0   0   0 | 0 | 0 | 0 | 1   1   1   1   1   1   1 |
+---+---+---+---+   +   +   +   +---+---+   +   +---+---+   +
| 0   0   0   0   0   0 | 0 | 0 | 0 | 1   1 | 1 | 1   1 | 1 |
+---+---+---+---+---+   +   +   +   +   +---+---+   +   +---+
| 0   0   0   0   0   0 | 0 | 0 | 0 | 1   1   1   1 | 1   1 |
+---+---+---+---+---+   +   +   +   +---+---+   +---+---+   +
| 0   0   0   0   0   0 | 0   0   0   0   0 | 1 | 1   1 | 1 |
+---+---+---+---+---+   +   +---+---+   +   +   +   +---+   +
| 0   0   0   0   0   0 | 0 | 1   D | 0 | 0 | 1 | 1 | 1   1 |
+---+---+---+---+---+   +   +   +---+---+   +   +   +   +---+
| 0   0   0   0   0   0   B | 1   1   1   1 | 1   1 | 1   1 |
+---+---+---+---+   +   +   +---+---+---+   +---+   +---+   +
| 0   0   0   0   0 | 0 | 0 | 1   1   1 | 1 | 1   1 | 1 | 1 |
+---+   +   +   +   +   +   +   +---+---+   +   +---+   +   +
| 0   0 | 0 | 0 | 0 | 0 | 0 | 1   1   1   1 | 1   1   1 | 1 |
+   +   +   +   +   +   +   +   +---+---+---+---+---+---+   +
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1   1 | 1   1 | 1   1   1 |
+   +   +   +   +   +   +   +   +   +   +   +   +   +---+   +
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1   1 | 1   1 | 1   1 | 1   1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
DFS just wasn't able to get a foothold in the western half of the board.  But, with a larger board, perhaps the outcome would change.  Or perhaps we need more tests...

### Example 6d - BFS vs DFS on steroids

We could, of course, boost the weight for DFS.  We know what to expect, but we'll run the experiment anyway.  We'll give DFS four moves (on average) to every three for BFS.  So our weights are now 3:4:
```
>>> maze = Maze(OblongGrid(10, 15))
>>> seed0, seed1 = maze.grid[4, 6], maze.grid[5,8]
>>> print(DFF.on(maze, task0, task1, seeds=[seed0, seed1], label=True, weights=[3,4]))
          Depth-first Forest (DFF) (statistics)
                            visits      300
                             tasks        2
                             seeds  [(4, 6), (5, 8)]
                             cells      150
                          passages      149
                      border edges       23
                      accept edges        1
                      reject edges        0
                            task 0  push(417), pop(417), max(18)
                            task 1  push(391), pop(391), max(69)
                     snake lengths  (84, 66)
```
Is this what you expected?

```
>>> seed0.label, seed1.label = "B", "D"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0   0   0   0 | 0 | 0 | 1   1   1   1 | 1   1   1   1   1 |
+---+---+---+   +   +   +   +---+---+   +   +---+---+---+   +
| 0   0   0   0   0 | 0   1   1   1 | 1 | 1 | 1 | 1   1   1 |
+---+---+---+---+   +   +---+---+   +   +   +   +   +---+---+
| 0   0   0   0   0 | 0 | 0 | 0 | 1 | 1 | 1 | 1   1 | 1   1 |
+---+---+---+---+   +   +   +   +   +   +   +   +---+---+   +
| 0   0   0   0   0   0 | 0 | 0 | 1 | 1   1 | 1 | 1   1   1 |
+---+---+---+---+---+   +   +   +   +---+---+   +---+   +   +
| 0   0   0   0   0   0 | 0   0 | D | 0 | 0 | 1   1   1 | 1 |
+---+---+---+---+---+   +   +---+---+   +   +---+---+---+   +
| 0   0   0   0   0   0   B   0   0   0   0   0 | 1   1   1 |
+---+---+---+---+---+   +   +---+---+---+---+---+   +---+---+
| 0   0   0   0   0   0 | 0   0   0   0 | 1 | 1   1 | 1   1 |
+---+---+---+---+   +   +   +---+---+---+   +   +---+---+   +
| 0   0   0   0   0 | 0 | 0   0   0 | 1   1 | 1 | 1   1 | 1 |
+---+---+   +   +   +   +   +   +---+   +---+   +   +   +   +
| 0   0   0 | 0 | 0 | 0 | 0 | 0 | 1   1   1 | 1 | 1 | 1   1 |
+---+---+   +   +   +   +   +---+   +---+   +   +   +---+   +
| 0   0   0 | 0 | 0 | 0 | 0 | 1   1   1 | 1   1   1 | 1   1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

FYI: It's not what I expected.  But I do like surprises.

## Example 7 - BFS vs DFS on Moore grid

Let's rerun Example 6a on a Moore grid.

We need one additional import:
```
>>> from mazes.Grids.oblong8 import MooreGrid
```

We need to wrap a *MooreGrid* object inside a *Maze* object.  Otherwise it's as before:
```
>>> maze = Maze(MooreGrid(10, 15))
>>> seed0, seed1 = maze.grid[4, 6], maze.grid[5,8]
>>> print(DFF.on(maze, task0, task1, seeds=[seed0, seed1], label=True))
          Depth-first Forest (DFF) (statistics)
                            visits      300
                             tasks        2
                             seeds  [(4, 6), (5, 8)]
                             cells      150
                          passages      149
                      border edges      136
                      accept edges        1
                      reject edges        0
                            task 0  push(465), pop(465), max(18)
                            task 1  push(493), pop(493), max(92)
                     snake lengths  (48, 102)
```
DFS won the tournament.  Here is the result.
```
>>> seed0.label, seed1.label = "B", "D"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 1   1   1 | 1 | 1   1 | 1   1   1 | 1   1   1   1 |
+---\   +---\---+---X---\---\---\---\---+   +---+   +---/---+
| 0   0 | 1 | 1 | 1   1 | 1   1 | 1   1 | 1 | 1   1 | 1 | 1 |
+---+---X---\   +---+---+---+---+---+---+   +   +---+---X---+
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
+---X---/---\---+---\---\   /---+   /---+   /---/   +---X---+
| 1 | 0 | 0   0 | 0 | 0 | 0 | 1 | 0   0 | 1 | 1 | 1 | 1 | 1 |
+   +---+---/---\---\   /---/---X---\---+---+   +---X---+   +
| 1   1 | 0 | 0   0   0 | 1 | 0 | D | 0   0 | 1   1 | 1   1 |
+---+   +---+---/---/---\---X---+---+---\---\---+---+---+   +
| 0 | 1 | 0   0 | 0 | 0   B | 1   1 | 1 | 0 | 0 | 1 | 1 | 1 |
+---\---X   +---/---/---/   \---+   /---\---+---/---X---+   +
| 0   0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1   1 | 1 | 1 | 1 | 1 |
+---+---/---/---+---+   +---/   \---+---\---+---\---\---\   +
| 1   1 | 0 | 1 | 1 | 0 | 0 | 0 | 0   0 | 1 | 1   1 | 1 | 1 |
+---\---+---/   +   \---+---+---+---+---+---\---\---+---\---+
| 1   1 | 1 | 1 | 1 | 1 | 1   1 | 1   1   1   1 | 1   1 | 1 |
+---X---X---+---X---+---\---X---+   +---+---+---+---+---X   +
| 1 | 1 | 1 | 1   1   1 | 1 | 1   1 | 1   1   1   1   1 | 1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now the exercise is to trave from B to D.  You'll need to find that one border edge that was accepted.

Another is to explain why in all four mazes in Example 6 as well as this one, there were no rejected border edges.  (In other words, the first border edge in the list was the accepted edge.)  The explanation is actually quite simple, but it does depend on the number of tasks.  (Example 2 has a rejected edge.)