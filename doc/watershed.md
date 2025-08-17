# Watersheds

## Watersheds and recursive division

Watersheds are essentially a means by which recursive division can be generalized to arbitrary connected grids.  Even if we stay with the basic rectangular grid, watersheds allow us to partition it in arbitrary ways.

The general idea is that we start with a connected grid and partition it into a number of reservoirs.  The reservoirs are connected by a maze of floodgates.

Now each reservoir can be viewed as a connected subgrid.  If the reservoir consists of a single cell, no further processing is needed.  Otherwise, we  partition its subgrid into a watershed system of several reservoirs, and then connect the system with some floodgates.

## The *Watershed* class

The *Watershed* class is defined in the module *mazes.watershed*.  The workings are not difficult, but they are not necessarily intuitive.  There is a demonstration module *demos.watershed* which provides some insight.  We will use the demo in two examples, and then provide a third example which goes into the gory details.

## On the examples

Examples 1 and 2 run the watershed demonstration using queues and stacks, respectively.  Example 3 basically shows how the demonstration works.

Example 4 is intended to give some insight into how the watershed model might be used recursively.  In this demo, instead of giving the Watershed object the entire grid, we instead give it a subset of the grid.  We have essentially left the outer boundary and a strip in the middle as a raised land surrounding and inside the watershed.

Example 5 is a basic example using watershed recursive division.  For more details and examples, see the documentation in *watershed\_division.md* in the *doc/Algorithms* folder.

## The watershed demo

Here is the usage docstring:
```
    usage: watershed.py [-h] [-d ROWS COLS] [-n SEEDS] [-s]

    Watershed demonstration

    options:
      -h, --help        show this help message and exit
      -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

    watershed options:
      -n SEEDS, --seeds SEEDS
                        The number of seeds. (Default: 2)
      -s, --stack           Use stacks instead of queues.

    Output is to the console.
```

## Example 1.  A queue-based watershed

We run the demo.  We will create a queue-based watershed with four reservoirs.
```
    maze4c$ python -m demos.watershed -n 4
```

The demo starts by creating a rectangular grid and installing four pumps:
```
    OblongGrid(8, 13)
    Seed cells: [(7, 6), (5, 6), (2, 3), (3, 12)]
```

That's all that is required to create the *Watershed* object:
```
    Watershed(grid, seeds)  # default: QueueType=Queue)
```

Next we need to punp in the water.  This is done using a round-robin process -- each pump in turn pumps in just enough water to fill one more neighboring cell, but only a cell which is not already claimed by one of the reservoirs.  When a reservoir has no available neighboring cells, it stops.
```
    Beginning the round robin...
        completed after 27 passes.
```

The last pass is a failure pass.  With four pumps, 4 x 27 = 108.  There are 8 x 13 = 104 cells.  So apparently some reservoirs are slightly larger than some of the others.  Now we need to connect the reservoirs with a minimal system of floodgates, so that water may move between the reservoirs.  Each reservoir is represented by a single cell in an auxiliary grid.  Inspecting the display below, we see that reservoir 0 is adjacent to each of the other reservoirs.  Reservoir 1 and reservoir 2 are not adjacent.  The auxiliary grid looks like this:
```
                     3
                    /|\
                   / | \
                  /  |  \
                 1---0---2
```
In addition, we run a maze algorithm on the auxiliary grid to help decide the placement of floodgates.  The demo uses Aldous/Broder.  (For a two-reservoir watershed, Aldous/Broder will always terminate quickly.  Termination cannot be guaranteed for 3 or more reservoirs, but the probability of an actual bottleneck is negligible provided the number of reservoirs is small.)
```
    Creating the component maze...
        4 cells, expected 4
        running Aldous/Broder...
            (should be quick, but there are no guarantees)
        3 joins
    Carving the floodgates:
        floodgate: ((1, 6), (1, 5))      # 0 -- 1
        floodgate: ((6, 7), (7, 7))      # 0 -- 3
        floodgate: ((4, 10), (4, 9))     # 0 -- 2
```
Analysis of the floodgates (see hash comments) shows that the auxiliary maze
looked like this:
```
                     3
                     |
                     |
                     |
                 1---0---2
```
The floodgates were chosen at random from the possible edges.  Here is the final reservoir map, including the floodgates.
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 |
+---+---+---+---+---+---+---+   +---+---+---+---+---+
| 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 3 | 3 | 3 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0   2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 2 | 2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1   0 | 0 | 0 | 2 | 2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 2 | 2 | 2 | 2 | 2 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Counting, reservoirs 0, 1, 2, and 3 have 26, 27, 25, and 26 cells, respectively.

## Example 2.  A stack-based watershed

As before, a maze is created, some pumps are installed, and a watershed is created and filled using the round-robin pumping algorithm.
```
    maze4c$ python -m demos.watershed -n 4 -s
    OblongGrid(8, 13)
    Seed cells: [(1, 5), (1, 10), (5, 4), (3, 9)]
    Watershed(grid, seeds, QueueType=Stack)
    Beginning the round robin...
        completed after 28 passes.
```
Since 28 x 4 = 112 is greater than 8 x 13 = 104, the reservoirs are not equal in size.  The complexity of the system is governed by the type of queue, the grid topology, and both the number and the placement of the pumps.

We carve the auxiliary maze and choose the floodgate locations:
```
Creating the component maze...
	4 cells, expected 4
	running Aldous/Broder...
		(should be quick, but there are no guarantees)
	3 joins
Carving the floodgates:
	floodgate: ((2, 10), (2, 9))
	floodgate: ((5, 9), (5, 8))
	floodgate: ((4, 1), (3, 1))
```
From the floodgate information, we can deduce the underlying auxiliary reservoir maze.  The reservoir connections are as follows:

<div align="center">
<table>
  <tr><th>cell location</th><th>edge</th></tr>
  <tr><td>(2,10), (2,9)</td><td>0--3</td></tr>
  <tr><td>(5,9), (5,8)</td><td>0--1</td></tr>
  <tr><td>(4,1), (3,1)</td><td>1--2</td></tr>
</table>
</div>

The auxiliary maze is just a single chain:
```
        3 -- 0 -- 1 -- 2
```
(NOTE: The watershed demo does not display the auxiliary maze.)

The final result as displayed by the demo:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1   0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 0 | 0 |
+---+   +---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3   0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 3.  How to do this programmatically...

First we will need a few imports.  We will need a connected grid for the maze to be partitioned.  We will also need a Watershed object.  The Watershed object will create an empty auxiliary maze.  (By empty, I mean that the grid connections are present, but, none of the reservoirs are linked.  We accordingly need an algorithm to carve the reservoir maze.  The Watershed object suggests floodgate locations, based on the auxiliary maze, but these are
just suggestions.  As we must carve the associated passages, we will also need a Maze object using the original connected grid.

We also need access to a random number generator as our pumps will be located randomly.

```
    maze4c$ python
    Python 3.10.12
    >>> from mazes import rng
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
    >>> from mazes.watershed import Watershed
    >>> from mazes.Algorithms.aldous_broder import AldousBroder
    >>>
```

Our reservoir system (or watershed) will be built on a rectangular grid (class *OblongGrid*), but any connected grid could be used.  (If the grid is not connected, an exception will be raised at some point in the process.)  We will be using Aldous/Broder to carve the auxiliary reservoir maze.  As our watershed won't have many reservoirs, the choice of algorithm doesn't matter, except to the extent that the algorithm must work on arbitrary grids.  (For example, the simple binary tree algorithm would not work as our auxiliary grid is not rectangular.)

First we create the reservoir system and install the pumps:
```
    >>> reservoirs = Maze(OblongGrid(8, 13))
    >>> pumps = rng.choices(list(reservoirs.grid), k=4)
    >>>
```

Let's see where the pumps were installed:
```
    >>> labels = "ABCD"
    >>> for i in range(4):
    ...     pumps[i].label = labels[i]
    ...
     >>> print(reservoirs)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   | A |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   | B |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   | C |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | D |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    >>>
```

We can now begin to fill the system:
```
    >>> watershed.round_robin()
    True
    >>> watershed.label()
    >>> print(reservoirs)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   | 3 | 3 |   | 0 |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   | 0 |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   | 2 | 2 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 1 | 1 |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    >>>
```

The method *watershed.label()* labels each cell with its reservoir number.  When the watershed was created, each pump filled its associated cell.  The method *watershed.round_robin()* attempts to fill one neighboring cell from each pump.  The returned value, *True*, indicates that at least one reservoir claimed an additional cell.

To complete the system of reservoirs, we must run *watershed.round_robin()* until it returns false.  Each time, including the last constitutes a single pass through the pumps.  (NOTE: When counting passes, don't forget the pass that returns *False*.)  We have already used one pass, and a *while* loop will exit before counting...

```
    >>> passes = 2
    >>> while watershed.round_robin():
    ...     passes += 1
    ...
    >>> print(f"passes: {passes}")
    passes: 29
    >>> watershed.label()
    >>>
```
The watershed algrorithm completed after 29 passes of the round robin.  This includes the failure pass.  Note that the pump cells were added at the start, so the minimum number of passes (including the failure pass) is the number of cells divided by the number of pumps, *i.e.* (8×13)/4 = 26.  So the reservoirs are not equal in size, but they are fairly close to equal.

We have labelled the cells in each reservoir with the reservoir number.  The only thing left is to connect the reservoirs with a system of floodgates.  First we carve an auxiliary maze:

```
    >>> aux_maze = watershed.initialize_maze()
    >>> type(aux_maze)
    <class 'mazes.maze.Maze'>
    >>> print(AldousBroder.on(aux_maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits        4
                             cells        4
                          passages        3
                     starting cell        2
    >>>
```

We create a grid four cells, each representing a single reservoir.  Note that the method returned a Maze object containing the desired grid.  We pass this maze object into our carving algorithm (Aldous/Broder).  The algorithm carves three passages.  We will use this auxiliary maze to carve our floodgates:

```
    >>> floodgates = watershed.doors(aux_maze)
    >>> floodgates
    [{SquareCell object, SquareCell object}, {SquareCell object,
       SquareCell object}, {SquareCell object, SquareCell object}]
    >>>
```
The watershed object returned three sets, each consisting of two square cells.  Sets were returned because the carving algorithm (AldousBroder) produces undirected links.  The *doors()* method is smart enough to handle directed links by replacing them with tuples instead of sets.  NOTE: At this point, these floodgates are just suggestions.  We could run the *doors()* method again to get another list of suggestions.

To display the cell coordinates, we need to do a little busy work:
```
    >>> for gate in floodgates:
    ...     cell1, cell2 = gate
    ...     foo.append({cell1.index, cell2.index})
    ...
    >>> foo
    [{(6, 10), (6, 11)}, {(4, 4), (4, 5)}, {(1, 6), (0, 6)}]
    >>>
```

Now let us carve the floodgates:
```
    >>> for gate in floodgates:
    ...     reservoirs.link(*tuple(gate))
    ...
    >>>
```

NOTE: The syntax `*tuple(gate)` is Python sugar which just converts the set of cells into an argument list.  I could have written this out instead as:
```
    >>>     # TRANSLATING THE PYTHON SUGAR
    >>> for gate in floodgates:
    ...     cell1, cell2 = gate
    ...     reservoirs.link(cell1, cell2)
    ...
    >>>    # END OF TRANSLATION
```

Now that the reservoir maze has been carved, let's look at the final result:
```
    >>> print(reservoirs)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0   2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 1 | 1 | 3 | 3 | 3   0 | 0 | 0 | 0 | 2 | 2 | 2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 1 | 1 | 1 | 1 | 3 | 0 | 0 | 0 | 2 | 2 | 2 | 2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 2 | 2 | 2 | 2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 2 | 2 | 2 | 2 | 2 |
    +---+---+---+---+---+---+   +---+---+---+---+---+---+
    | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    >>> # END OF DEMO
```

## Example 4.  Land masses in the reservoir system

We run a modified version of the demo which fixes the grid at 8 by 13 and removes the outer cells and a strip in the center from the reservoir system.  A list of the remaining cells (*i.e.* the labelled cells below) are what was supplied in lieu of a Grid object.
```
    maze4c$ python -m demos.watershed_partial -n 4
    OblongGrid(8, 13)
    Seed cells: [(3, 3), (5, 1), (1, 8), (6, 1)]
    Watershed(grid, seeds)  # default: QueueType=Queue)
    Beginning the round robin...
        completed after 20 passes.
    Creating the component maze...
        4 cells, expected 4
        running Aldous/Broder...
            (should be quick, but there are no guarantees)
        3 joins
    Carving the floodgates:
        floodgate: ((6, 2), (5, 2))
        floodgate: ((1, 4), (1, 5))
        floodgate: ((1, 6), (1, 5))
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |   |
    +---+---+   +---+---+---+---+---+---+---+---+---+---+
    |   | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 2 | 2 | 3 | 3 |   |   |   | 1 | 1 | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 2 | 3 | 3 | 3 |   |   |   | 1 | 1 | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 2 | 3 | 3 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | 2 | 2 | 2 | 2   3   1 | 1 | 1 | 1 | 1 | 1 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The underlying idea in recursive division using watersheds is that the recurrence involves treating a reservoir as a watershed system.

## Example 5. Watershed recursive division

Recursive division using watersheds is implemented in Python module *watershed\_division.py* found in the *mazes/algorithms* folder.  There are many options -- for those, we defer to the module *docstring* and to the *watershed\_division* documentation in the *doc/algorithms* folder.  Here we give just one example.

As always, we need to import a few classes:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.watershed_division import WatershedDivision
```

Then we construct a grid and embed it in a maze object.  Any grid type will do, but, for documentation purposes, we stick with a rectangular grid.  Our watershed recursive division is a passage carver, so the cells in the grid are not linked at this stage:
```
>>> maze = Maze(OblongGrid(10,15))
```

Next we run the algorithm, here taking all the available defaults.  In addition to the empty maze above, we need to specify a minimum size and the number of pumps to use in each subdivision.  We will go with 2 cells and 2 pumps.  A minimum size of two insures that the maze will be a perfect maze.  Two pumps means that, at each visit, if our current basin has at least two cells, then we will subdivide it into two basins and carve a door between them:
```
>>> print(WatershedDivision.on(maze, 2, 2))
          Watershed Recursive Division (statistics)
                            visits      368
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        8
```
Our grid has 150 cells, and we have 149 passages.  The number of cells is one more than the number of passages -- a necessary (but not a sufficient) condition for a perfect maze.

Let's do some analysis...

The largest stack length was 8 -- corresponding to a recursion depth of 8 levels.  The number of visits, 368, is the number of times basins were passed to the partitioning routine.  This includes the "failures" -- single cell basins that were too small to subdivide.  Clearly this number must be larger than 150.  In the best case, we would subdivide as equally as possible:

| basin sizes     | visits | too small |
| --------------- | -----: | --------: |
| 150             | 1      |           |
| 75 + 75         | 2      |           |
| (37 + 38)*2     | 4      |           |
| (18 + 19*3)*2   | 8      |           |
| (9*5 + 10*3)*2  | 16     |           |
| (4*5 + 5*11)*2  | 32     |           |
| (2*21 + 3*11)*2 | 64     |           |
| (1*53 + 2*11)*2 | 128    | 106       |
| 1*44            | 44     | 44        |
| TOTALS          | 299    | 150       |

So the best we can do is 299 visits.  (Note that powers of two show up in the visit column until basins of size 1 start to drop out.  That is not an accident.  The "too small" column adds up to 150 cells because there are 150 cells in the maze, again not an accident.)  Note also that there are 9 lines in the table.  This is 1 more than the maximum stack size above. Although the number of visits was not optimal, the algorithm did as well as the best case in terms of maximum recursion depth.

And here is the maze...
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |                                   |   |
+---+---+   +   +   +   +---+---+---+---+   +---+   +---+   +
|           |   |   |   |       |       |       |           |
+---+   +---+   +---+   +   +   +---+   +---+---+---+---+   +
|   |                   |   |       |       |           |   |
+   +   +---+---+---+---+---+   +   +   +   +   +---+   +   +
|       |           |       |   |       |       |   |       |
+   +---+   +   +---+   +---+   +   +   +   +---+   +---+---+
|   |   |   |   |           |   |   |   |                   |
+   +   +---+   +   +---+   +   +---+   +---+   +---+---+   +
|   |           |   |               |       |   |   |   |   |
+   +---+   +   +---+---+   +---+   +   +   +---+   +   +   +
|           |   |           |       |   |   |       |       |
+   +---+---+   +---+   +---+   +   +---+---+---+   +   +   +
|   |   |           |   |       |   |       |   |       |   |
+   +   +---+   +   +   +---+   +---+   +   +   +---+---+---+
|       |   |   |   |       |   |   |   |   |   |           |
+   +---+   +---+   +   +---+   +   +   +   +   +   +---+   +
|               |   |   |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```