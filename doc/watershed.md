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

Examples 6, 7, and 8 use three different scheduling algorithms (round robin, unweighted tournament, weighted tournament) to build the watershed.

Example 9 shows how the Watershed class might be used with several carving algorithms to carve mazes in each of the basins.  The demonstration module outputs some working Python code along with the results.  It can be thought of as a tutorial on how to program with watersheds.

## The watershed demo

Here is the usage docstring:
```
$ python -m demos.watershed -h
usage: watershed.py [-h] [-d ROWS COLS] [-n SEEDS] [-s] [--tournament]
                    [--weighted]

Watershed demonstration

options:
  -h, --help            show this help message and exit
  -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

watershed options:
  -n SEEDS, --seeds SEEDS
                        The number of seeds. (Default: 2)
  -s, --stack           Use stacks instead of queues.
  --tournament          Use a tournament instead of a round robin.
  --weighted            Use a weighted tournament instead of a round robin.

Output is to the console.
```

## Round robin scheduling

### Example 1.  A queue-based watershed

We run the demo.  We will create a queue-based watershed with four reservoirs.
```
    maze4c$ python -m demos.watershed -n 4
```

The demo starts by creating a rectangular grid and installing four pumps:
```
    maze = Maze(OblongGrid(8, 13))
    Seed cells: [(7, 6), (5, 6), (2, 3), (3, 12)]
        # default: QueueType=Queue)
    from mazes.round_robin import RoundRobin
    Watershed(grid, seeds, tournament=RoundRobin())
```
(By default, the *Watershed* object now uses a *Tournament* object as its scheduler.  As originally written, it used a built-in round robin.  For more details, see the section on *tournament scheduling*.  The demo retains the original round robin default.)

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

### Example 2.  A stack-based watershed

As before, a maze is created, some pumps are installed, and a watershed is created and filled using the round-robin pumping algorithm.
```
    maze4c$ python -m demos.watershed -n 4 -s
```

The demo creates a stack-based watershed
```
    maze = Maze(OblongGrid(8, 13))
    Seed cells: [(1, 5), (1, 10), (5, 4), (3, 9)]
    from mazes.round_robin import RoundRobin
    Watershed(maze, seeds, QueueType=Stack, tournament=RoundRobin())
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

### Example 3.  How to do this programmatically...

First we will need a few imports.  We will need a connected grid for the maze to be partitioned.  We will also need a Watershed object.  The Watershed object will create an empty auxiliary maze.  (By empty, I mean that the grid connections are present, but, none of the reservoirs are linked.  We accordingly need an algorithm to carve the reservoir maze.  The Watershed object suggests floodgate locations, based on the auxiliary maze, but these are
just suggestions.  As we must carve the associated passages, we will also need a Maze object using the original connected grid.

We also need access to a random number generator as our pumps will be located randomly.

```
    maze4c$ python
    Python 3.10.12
    >>> from mazes import rng
    >>> from mazes.Grids.oblong import OblongGrid
    >>> from mazes.maze import Maze
    >>> from mazes.round_robin import RoundRobin
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
    >>> watershed = Watershed(reservoirs, pumps, tournament=RoundRobin())
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

### Example 4.  Land masses in the reservoir system

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

### Example 5. Watershed recursive division

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

## Tournament scheduling

As noted in Example 1, the watershed class was originally written to use round robin scheduling.  The examples above were created accordingly.  The watershed demonstration module (*demos/watershed*) preserves round robin scheduling as the default.

Tournament scheduling is now the default for the *Watershed* class, and the demonstration module can access it using either the tournament or the weighted option.

### Round robins *vs* tournaments

An unweighted tournament differs from round robin scheduling by randomly giving each task a turn.  Consider two knights (Lancelot and Percy) in a sword duel.  In a round robin, the knights take turns:  Lancelot, Percy, Lancelot, Percy, *etc*.

In an unweighted tournament with the two knights, a fair coin is tossed to determine who gets the next strike,  In our example, if, in succession, the coin returns tail, tail, head, tail, head, then the first five strikes are (respectively) Percy, Percy, Lancelot, Percy, Lancelot.

### Example 6 - an unweighted tournament

Here we have a 4-way tournament.  With a reasonably large grid, the difference between an unweighted tournament and a round robin is normally not dramatic.  But the difference is enough to create different biases in algorithms using them.
```
$ python -m demos.watershed --tournament -n 4
OblongGrid(8, 13)
Seed cells: [(7, 7), (4, 9), (1, 11), (4, 5)]
Beginning the round robin...
	completed after 105 passes.
Creating the component maze...
	4 cells, expected 4
	running Aldous/Broder...
		(should be quick, but there are no guarantees)
	3 joins
Carving the floodgates:
	floodgate: ((4, 12), (3, 12))
	floodgate: ((6, 12), (5, 12))
	floodgate: ((5, 2), (5, 1))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 3 | 3 | 0 | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
| 0 | 0   2 | 2 | 2 | 2 | 2 | 0 | 3 | 3 | 3 | 3 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 |
+---+---+---+---+---+---+---+---+---+---+---+---+   +
| 0 | 0 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 1 | 1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 1 | 1 | 1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 0 | 0 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 7 - a weighted tournament

Consider our example of Lancelot and Percy, and suppose instead of a fair coin, we use a fair die with the usual six faces.  If 6 comes up on the die, then Lancelot gets a turn.  If the die returns 1, 2, 3, 4 or 5, then Percy gets a turn.  In this case the tournament is weighted respectively 1 to 5 for Lancelot against Percy.

The weighted option in the demo uses consecutive Fibonacci numbers, starting with 2, as weights.  So with 4 tasks, the consecutive weights are 2:3:5:8.  With 5 tasks, we add the last two (5+8) to get a weight of 13 for the fifth task.

```
$ python -m demos.watershed --weighted -n 5
OblongGrid(8, 13)
Seed cells: [(7, 4), (5, 11), (6, 10), (7, 0), (1, 7)]
Beginning the round robin...
	completed after 105 passes.
Creating the component maze...
	5 cells, expected 5
	running Aldous/Broder...
		(should be quick, but there are no guarantees)
	4 joins
Carving the floodgates:
	floodgate: ((3, 8), (2, 8))
	floodgate: ((5, 5), (6, 5))
	floodgate: ((6, 6), (6, 5))
	floodgate: ((7, 3), (7, 2))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1   0 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 1 | 0 | 0 | 0   3 | 3 | 3 | 3 | 3 | 3 | 4 |
+---+---+---+---+---+   +---+---+---+---+---+---+---+
| 1 | 1 | 4 | 4 | 0 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 1 | 1 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+   +---+---+---+---+
| 4 | 4 | 4 | 4 | 4 | 4 | 2 | 2 | 2 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 4 | 4 | 4 | 2 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4 | 4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here we used five tasks.  The last basin, #4 (weight 13) managed to claim territory covering much of the grid.  Basins 0, 1, 2 and 3 (weights 2, 3, 5 and 8) were trapped before they could gain large footholds.

### Example 8 - tournament with a stack

We can, of course, use a stack instead of a queue:

```
$ python -m demos.watershed --weighted -n 5 --stack
OblongGrid(8, 13)
Seed cells: [(2, 0), (3, 6), (3, 11), (3, 4), (0, 7)]
Beginning the round robin...
	completed after 105 passes.
Creating the component maze...
	5 cells, expected 5
	running Aldous/Broder...
		(should be quick, but there are no guarantees)
	4 joins
Carving the floodgates:
	floodgate: ((1, 6), (1, 5))
	floodgate: ((1, 4), (2, 4))
	floodgate: ((5, 2), (5, 1))
	floodgate: ((3, 1), (2, 1))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2   3 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 |
+---+   +---+---+---+---+---+---+---+---+---+---+---+
| 2 | 0 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 |
+---+---+---+---+   +---+---+---+---+---+---+---+---+
| 2 | 2 | 2 | 1 | 1 | 1   4 | 4 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 4 | 4 | 4 | 4 | 4 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here, basin 3 with weight 8 started roughly in the middle of the grid, offsetting some of the advantage of basin 4 (weight 13).  Basin 2 (weight 5) was somewhat shielded by basins 0 and 1 (weights 2 and 3), and was able to claim a large share of the western region of the maze.

## Programming with watersheds

The demonstration module *demos.basin\_maze* is a tutorial of sorts on Python programming with watersheds.  Here is the help:
```
$ python -m demos.basin_maze -h
usage: basin_maze.py [-h] [-d ROWS COLS] [-n SEEDS] [--round_robin] [-s]
                     [--task_args [WGT ...]]

Watershed demonstration with mazes carved in the basins.

options:
  -h, --help            show this help message and exit

watershed options:
  -d ROWS COLS, --dim ROWS COLS
                        the dimensions of the underlying grid.
  -n SEEDS, --seeds SEEDS
                        The number of pumps. (Default: 4)
  --round_robin         use a round robin scheduler.
  -s, --stack           Use stacks instead of queues.
  --task_args [WGT ...]
                        tournament task weights.

Output is to the console. The basin carving algorithms are respectively DFS,
BFS, Wilson, and Kruskal. Kruskal will be used whenever there are four or more
basins.
```

All of the options have defaults.  We will give one example using two of the options:

### Example 9 - programming with watersheds

```
$ python -m demos.basin_maze -d 10 15 -n 5
Namespace(dim=[10, 15], seeds=5, round_robin=False, stack=False, task_args=[])
```

We specified the dimensions of the maze and the number of pumps.  The selected options (including the defaults) are displayed in a namespace.  The demo starts spitting out Python code, with some comments.  In addition to displaying code, the demo performs the operations that are described in the code.  The code includes the imports as they are needed.

The first step is to create a maze object.  Here is the code for a simple rectangular maze with 10 rows and 15 columns:
```
        # create a Maze instance
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
maze = Maze(OblongGrid(10, 15))
grid = maze.grid
```

Next we need to identify five cells to use as pumps:
```
        # get 5 seed cells to use as pumps
from mazes import rng
seeds = rng.sample(list(maze.grid), n)
# --> seeds: [grid[7,7], grid[0,2], grid[0,12], grid[4,12], grid[1,6]]
```
A comment displays the cells that were obtained in the sample operation.

The default scheduler is an unweighted tournament using queues.  Each task is a breadth first search that starts with the indicated pumpinf cell as its starting point or seed.  If we had specified a stack, the searches would be depth-first.  Just one line is needed here:
```
        # create an unweighted tournament watershed
watershed = Watershed(grid, seeds)    # using a queue
```

Next we map the basins.  These are the five breadth-first search tasks:
```
        # map the basins (coding loop)
passes = 1
while watershed.round_robin():
    passes += 1
# --> completed after passes=151.
```
There are 5 pumping cells and a total of 150 cells in the grid.  That leaves 145 cells that need to be claimed.  145 of the 151 passes claim cells.  Five additional failure passes end each of the five pumping tasks.  The remaining pass is a failure pass which detects that there are no more active tasks:
```
     145 + 5 + 1 = 151.
```

At this point, the basins have been identified, but no passages have been carved.  The next step is to carve the floodgate passages that separate the basins.  We first create a simplified map with one component per basin.  We then carve a maze on that map (using Kruskal's algorithm.  Using that maze, we select grid connections as floodgates.  Since there are five basins, we need four floodgates in order to have a perfect maze:
```
        # carve the floodgates separating the basins
cmaze = watershed.initialize_maze()    # simplified basin map
# --> 5 cells in map, expected 5
from mazes.Algorithms.kruskal import Kruskal  # floodgate carver
print(Kruskal.on(cmaze))
          Kruskal (statistics)
                            visits        4
                 components (init)        5
               queue length (init)        7
                             cells        5
                          passages        4
                components (final)        1
              queue length (final)        3
gates = watershed.doors(cmaze)   # now carving
#   connecting the gates (loop)
for gate in gates:
    cell1, cell2 = gate
    maze.link(cell1, cell2)
# --> floodgate indices: {(1,10),(0,10)}, {(3,12),(4,12)},
#                        {(5,9),(6,9)}, {(2,3),(2,4)}
```

For purposes of the demonstration, we label the cells in each basin with the basin number (0 through 4):
```
        # labelling the basins...
watershed.label()
```

We can now carve mazes in the basins.  The demonstration uses DFS, BFS and Wilson's algorithm to carve the first three basins.  Any remaining basins are carved using Kruskal's algorithm (which we have already imported).  We prepare the maze for carving by masking all cells except those in the basin being carved.  We then run the carving algorithm.  Finally, we unmask all the cells.  To access all cells in the grid including the masked cells, we must use the *Grid.\_cells* property:
```
        # carve mazes in the basins (loop)
from mazes.Algorithms.dfs_better import DFS
from mazes.Algorithms.bfs import BFS
from mazes.Algorithms.wilson import Wilson
algorithms = [Wilson, BFS, DFS]
for basin in watershed.basins:
    cells = set(watershed.basins[basin])
    for cell in grid._cells:        # all the cells
        if cell in cells:
            cell.reveal()
        else:
            cell.hide()
    Carver = algorithms.pop() if algorithms else Kruskal
    print(f'{basin=}:', Carver.on(maze))
for cell in grid._cells:        # all the cells
    cell.reveal()
```

Here are the results for each basin:
```
# ------------------------------ CARVING RESULTS ------------------------------
basin=0:           Depth-first Search (DFS) (statistics)
                            visits       69
                        start cell  (3, 7)
               maximum stack depth       22
                             cells       35
                          passages       34
basin=1:           Breadth-first Search (BFS) (statistics)
                            visits       18
                        start cell  (0, 11)
              maximum queue length        5
                             cells       18
                          passages       17
basin=2:           Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       13
                             cells       34
                          passages       33
                 paths constructed       13
                     cells visited      220
                          circuits       69
                    markers placed      138
                   markers removed      105
                     starting cell  (5, 8)
basin=3:           Kruskal (statistics)
                            visits       31
                 components (init)       25
               queue length (init)       37
                             cells      150
                          passages       24
                components (final)        1
              queue length (final)        6
basin=4:           Kruskal (statistics)
                            visits       47
                 components (init)       38
               queue length (init)       60
                             cells      150
                          passages       37
                components (final)        1
              queue length (final)       13
# -----------------------------------------------------------------------------
```

With 150 cells in the grid, we would hope to have 149 passages.  The mission was successful:
```
#    number of cells = 150
# number of passages = 149
```

All that's left is to display the result:
```
#        display the result
print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 4   4 | 4   4 | 2 | 2 | 2   2   2   2   2 | 3   3   3 | 3 |
+---+   +   +---+   +   +   +---+---+---+   +---+   +---+   +
| 4   4   4   4 | 2   2 | 2 | 2 | 2   2   2   2 | 3   3   3 |
+   +---+   +---+---+   +---+   +---+   +   +   +---+   +   +
| 4 | 4   4   4 | 2 | 2 | 2   2   2   2 | 2 | 2 | 3   3 | 3 |
+---+---+---+   +   +   +   +---+---+   +   +---+   +   +---+
| 4 | 4   4   4 | 2   2   2 | 2   2   2 | 2 | 3 | 3 | 3   3 |
+   +---+   +   +---+---+---+   +---+   +---+   +   +   +---+
| 4 | 4   4 | 4 | 0   0 | 2   2   2 | 0 | 3   3   3 | 3   3 |
+   +   +---+---+---+   +---+   +---+   +   +   +---+   +---+
| 4   4   4   4 | 0   0   0 | 2 | 0   0 | 3 | 3 | 3   3   3 |
+---+   +   +---+   +---+   +---+---+   +---+   +   +---+---+
| 4 | 4 | 4 | 0   0   0 | 0 | 0   0   0 | 1 | 3 | 1 | 1 | 1 |
+   +   +   +---+   +   +   +---+---+   +   +---+   +   +   +
| 4 | 4 | 4   4   0 | 0 | 0 | 0   0 | 0 | 1   1 | 1 | 1   1 |
+   +   +   +---+   +   +---+   +   +   +---+   +   +   +---+
| 4   4 | 4 | 0   0 | 0   0   0 | 0 | 0   0 | 1   1   1   1 |
+---+---+   +---+   +---+---+---+   +   +   +   +---+---+---+
| 4   4   4   4 | 0   0   0   0 | 0   0 | 1   1   1   1   1 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```