# Cretan Labyrinth-like Mazes

There is a type of unicursal maze variously known as Cretan labyrinth or a Trojan labyrinth.  They are not the mazes being produced here.  Instead, we use the depth-first-forest algorithm to carve a maze which is somewhat reminiscent of this sort of maze, but only vaguely.  The mazes produced here are fairly simple, but they can be twisty and they do have some other possibly undesirable properties.  Let's take a look:

```
    +---+---+---+---+---+---+---+---+---+---+
    |           |               |       |   |
    +---+   +   +   +   +---+   +---+   +   +
    |       |       |       |   |       |   |
    +   +---+---+---+---+   +   +   +---+   +
    |   |                   |   |       |   |
    +   +---+---+---+---+---+   +   +   +   +
    |                       |       |   |   |
    +   +---+---+---+---+   +---+   +   +   +
    |   |       |       | * | *     |   |   |
    +---+   +   +   +   +   +   +---+   +   +
    |   |   |       | *   3 | 2   *         |
    +   +   +---+---+   +---+---+---+---+   +
    |   |   |         *   1 | 0   *         |
    +   +---+   +   +---+   +   +---+---+   +
    |           |   |     * | *             |
    +   +---+---+   +   +---+---+---+---+   +
    |   |   |                           |   |
    +   +   +---+---+---+---+   +---+---+   +
    |       |                               |
    +---+---+---+---+---+---+---+---+---+---+
```
The numbered cells are the cells that form a randomly placed cross.  Each of these cells has two incident edges.  The starred cells are the other endpoints of these passages.  A unit called the *gammadion* consists of the numbered cells and their incident edges.  (The starred cells are not part of the gammadion.)

The algorithm we're calling the Cretan algorithm has four parts:

1. carve the gammadion and hide its cells;
2. run depth-first forest using a round-robin scheduler using the starred cells as seeds;
3. connect the snakes using Kruskal's algorithm; and
4. unmask the hidden gammadion cells.

Steps 2 and 3 are make up a depth-first forest run.  The maze above has ten rows and ten columns.  In step 1, we carve 8 passages.  In step 2, we have 8 tasks, each producing one component of an 8-component maze on 96 cells -- 96-8 is 88, the number of passages carved in step 2.  In step 3, we carve 7 passages to merge the 8 components into a single connected maze.  The total number of passages is:
```
        8 + 88 + 7 = 8 + 95 = 103.
```
The 96-cell maze is a perfect maze, but when we unmask the gammadion, we have 103 passages connecting 100 cells -- the full maze has several circuits.  In the maze above, it isn't hard to see an 8-cell circuit containing cell 0 and its two linked starred neighbors.  It shouldn't be hard to find two paths joining the two starred cells below gammadion cells 0 and 1.  One runs below the gammadion, and another much longer one runs above the gammadion.

Here are the statistics that were returned for this example:
```
          Cretan/DFF algorithm (statistics)
                            visits      192
                         gammadion        4
              passages (gammadion)        8
                             tasks        8
                             seeds  [(3,4), (2,5), (2,6), (3,7),
                                     (4,7), (5,6), (5,5), (4,4)]
                             cells       96
                          passages      103
                     Kruskal edges        7
                 merged components        8
                            task 0  push(12), pop(12), max(10)
                            task 1  push(10), pop(10), max(7)
                            task 2  push(13), pop(13), max(13)
                            task 3  push(9), pop(9), max(9)
                            task 4  push(10), pop(10), max(10)
                            task 5  push(16), pop(16), max(16)
                            task 6  push(17), pop(17), max(15)
                            task 7  push(9), pop(9), max(9)
                     snake lengths  (12, 10, 13, 9, 10, 16, 17, 9)
```

And finally, here is the code that was used to produce this maze:
```python
    from mazes.Grids.oblong import OblongGrid
    from mazes.maze import Maze
    from mazes.Algorithms.crete import Crete

    maze = Maze(OblongGrid(10,10))
    print(status := Crete.on(maze))
    cells = list(status.gammadion)
    for i in range(len(cells)):
        cells[i].label = str(i)
    for cell in status.seed_cells:
        cell.label = "*"
    print(maze)
```
