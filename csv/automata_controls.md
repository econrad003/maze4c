# Cellular automata maze creation

This is a baseline description of the statistical tests.  This file is based on the output of method *main2()* in the following module.  The output has been rearranged and explanations have been added.

## I. Sampling

```
SAMPLE_SIZE=10, ROWS=10, COLS=10, GENERATIONS=50
```
For each of the sampled algorithms, only 10 samples have been taken.  To get a dramatic speedup, the numbers of rows and columns in the resulting mazes have been reduced to ten cells each.

## II. The CSV

Here are the first few columns of the resulting CSV:
```
      algorithm,generations,stable,all die,     k,      e,     v,largest
         Wilson,       0.00,  1.00,   0.00,  1.00,  99.00,100.00, 100.00
          stdev,       0.00,  0.00,   0.00,  0.00,   0.00,  0.00,   0.00
ETC6:23/3 30% 2,      16.50,  1.00,   0.00, 83.70,  16.50,100.00,   6.60
          stdev,       4.59,  0.00,   0.00,  5.12,   5.52,  0.00,   4.18
ETC8:23/3 30% 2,      50.00,  0.00,   0.00, 78.30,  23.00,100.00,  10.80
          stdev,       0.00,  0.00,   0.00, 10.39,  11.71,  0.00,   6.73
ETC6:23/3 40% 2,      21.70,  1.00,   0.00, 82.30,  17.80,100.00,   6.50
         stdev,        5.97,  0.00,   0.00,  4.31,   4.26,  0.00,   2.06
ETC8:23/3 40% 2,      47.70,  0.10,   0.00, 80.30,  20.50,100.00,   8.50
          stdev,       6.90,  0.30,   0.00, 11.24,  11.58,  0.00,   5.04
ETC6:23/3 30% 3,      15.20,  1.00,   0.00, 85.90,  14.10,100.00,   5.60
          stdev,       5.67,  0.00,   0.00,  5.66,   5.66,  0.00,   1.62
ETC8:23/3 30% 3,      48.30,  0.10,   0.00, 74.00,  26.90,100.00,   9.90
          stdev,       5.10,  0.30,   0.00, 15.02,  15.65,  0.00,   4.81
```

## III. The CSV columns

Here is the full list of columns:
```
  algorithm,generations,stable,all die,k,e,v,largest,
  isolates,dead_ends,turns,northbound,eastbound,degree 3,degree 4
```

### The "algorithm" column

This will contain a string: either the name of the specific algorithm (indicating a row of arithmetic means) or the string "stdev" (indicating a row of standard deviations).

There are three basic algorithms:

* Wilson's algorithm - Wilson's algorithm is being used as a baseline as well as a control for the experiment
* seven-edge neighborhoods - for the automaton, each grid edge has *six* grid edges as neighbors (so each neighborhood consists of seven grid edges).
* nine-edge neighborhoods - for the automaton, each grid edge has *eight* grid edges as neighbors (so each neighborhood consists of eight grid edges).

The names have the form "<algo>:<automaton> <bias> <border>".  The expression <algo> is either "ETC6" for a seven-edge neighborhood automaton or "ETC8" for a nine-edge automaton.  The 6 or 8 denotes the number of neighbors for each grid edge.  The "E" says the cells are grid edges.  The "T" says that the automaton works on a torus, *i.e.* that north of the north boundary is the south boundary, and east of the east boundary is the west boundary.  (A torus is not only *finite* in extent, but also *unbounded*.  As a torus has no boundary walls, there are no special boundary conditions.)  The "C" indicates that the rules for the automaton are being expresses as Conway-type death/birth expressions.  (This type of expression is explained in the next paragraph.)

The expression <automaton> consists of several digits followed by a slash followed by several more digits.  The part before the the slash gives the death rule and the part after: the birth rule.  For example, the rule "12345/23" would have a death rule of {1,2,3,4,5} and a birth rule of {2,3}.  The birth rule says how many living neighbors a dead cell must have in order to be *born* (*i.e.* become alive).  The death rule says how many living neighbors a live cell must have in order *not* to die (*i.e.* to remain alive.  For example, with a birth rule of {2,3}, a dead cell would give birth in a generation with if it has 2 or 3 live neighbors.

The expression <bias> is a percentage (expressed as an integer in the interval (0,100) followed by a percent sign.  The bias tells how the maze was initialized.  A 30% bias says that a grid edge (*i.e.* a cell in the automaton) has a thirty percent chance of being live in first generation.

The expression <border> indicates how many cells have been added to the maze.  A border of two cells on a 10x10 maze indicates that the automaton is working a 12x12 torus.  The maze itself consists of the first ten rows and first ten columns.  (Since the torus is unbounded, the choice of ranges fors the rows and columns doesn't matter.  For example, we could just as easily use rows 1 through 10 instead of rows 0 through 9.  *If we were using a bounded surface*, the choice of a rectangular subset would be very important!)

### The "generations" column

This is the average number of generation in the simulation.  For Wilson's algorithm, this will always be 0 as the completes in the first generation.  For the automata, this will be a value in the interval \[0,50\].  If the value is less than 50 for a given sample (for example *generations=30*), then the automaton ended the simulation in a *stable* state (*e.g.* after 30 generations).  If the simulation had fifty generations, then we assume that the automaton was *unstable* under the given initial conditions.

### The "stable" column

If the simulation is judged as stable, it receives the value 1.  If unstable, it receives the value 0.  If the mean (or average) is 1, then all samples ended in a stable configuration.  If the mean is 0, then all samples ended in an unstable configuration.  A mean between 0 and 1 indicates that some, but not all of the samples were stable.

With ten samples, a mean of 0.4 means that 4 samples ended in a stable configuration and that the remaining 6 samples continued through all fifty generations of the simulation.

### The "all die" column

There is more than one way that a sample can end in a stable configuration.  One possibility is the the simulation *crashed*, *i.e.* all cells in the automaton died.  For a given simulation, a value of 1 indicates that the simulation crashed and a value of 0 indicates that some cells (or grid edges) were alive at the end of the simulation.

With ten samples, a mean of 0.2 means that 2 samples ended in a crash and that the remaining 8 samples did not crash.

Note that when the number of border cells is positive, even if the simulation does not crash, the resulting maze might still end up as empty.

For Wilson's algorithm, this value will always be 1.

### The "k" column

This value denotes the mean of number of connected components in the sample mazes.  The automata typically produce mazes with more than one component.

The automata sampled here all produced mazes with many components -- the means for all the sampled automata were in the double digits, not desirable for a 10x10 maze.  The ideal number of components is 1, *i.e.* the maze is connected.

### The "e" and "v" columns

The value of "e" denotes the mean of number of passages in the sample mazes.  The value of "v" denotes the mean of number of cells (or vertices) in the sample mazes.

For this simulation, the value of "v" will always be 100 since the resulting mazes are 10x10.  For a perfect maze (an *ideal* maze):

* *e = v - k*; and
* *k = 1*.

For a forest with no circuits:

* *e = v - k*.

If *e > v-k*, then the maze has circuits.

The automata sampled here all have low "e" averages because of the large numbers of components.  For nearly ideal mazes, we would want the values of *k* and the ratio *(v-k)/e* to be not much more than 1.  The next column gives one additional condition.

### The "largest" component column

The number of components of a maze cannot be less that the number of cells (or vertices divided by the number of cells in the largest component.  For exaple, if there are 100 cells and the largest component is 25 cells, then *k ≥ 4*.  With a largest component of 24 cells, we jump to a minimum of 5 components.

A small largest component indicates that the maze is seriously fractured, something that happens with all six automata in this sample.

For our "nearly ideal" maze, we would like our resulting maze not to be fractured.  Of course it's difficult to come up with an exact definition here, but we will use the following as a working definition:

* Let *K* be the largest component.  For a "nearly ideal" maze automaton, we require, on average, that *|K|/v* < 0.75.

### The "isolates" and "dead ends" columns

These denote the average numbers of degree 0 (or isolated) and degree 1 (or dead end) cells, respectively.

### The "turns", "northbound", and "eastbound" columns

The total of these three values is the number of degree 2 cells.  A northbound cell is a degree-2 cell with passages north and south.  An eastbound cell is a degree-2 cell with passages east and west.  All other degree-2 cells are turns.

The columns are, of course, averages.

### The "degree 3" and "degree 4" columns

These should be self-explanatory.

## IV. Sample mazes

With the exception of Wilson's algorithm, used here as a baseline and a control, the algorithms chosen here are intended only as illustrations.

Here we give one maze (without further comment!) from each of the sample algorithms.

### Wilson

```
+---+---+---+---+---+---+---+---+---+---+
|                       |       |       |
+   +---+---+---+---+---+---+   +   +   +
|                                   |   |
+---+---+   +---+   +---+   +---+   +   +
|   |   |       |   |       |       |   |
+   +   +---+   +---+---+---+---+---+   +
|       |   |               |   |   |   |
+   +---+   +---+   +   +   +   +   +   +
|                   |   |       |       |
+   +---+---+---+   +   +   +---+   +---+
|           |       |   |       |   |   |
+---+   +---+---+---+---+---+---+   +   +
|       |       |                       |
+   +---+   +---+   +---+---+   +---+---+
|           |           |       |       |
+   +---+---+   +   +   +   +---+   +   +
|   |       |   |   |   |           |   |
+---+   +---+---+   +---+   +   +---+---+
|                   |       |           |
+---+---+---+---+---+---+---+---+---+---+
```


### ETC6:23/3 30% 2

```
+---+---+---+---+---+---+---+---+---+---+
|   |   |           |   |   |   |   |   |
+---+---+---+   +---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+   +   +
|   |   |   |   |   |   |   |       |   |
+---+---+---+---+---+---+---+---+   +   +
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+   +---+---+---+
|   |   |   |   |   |           |   |   |
+---+---+---+---+---+---+   +---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
```

### ETC8:23/3 30% 2

```
+---+---+---+---+---+---+---+---+---+---+
|       |   |   |   |   |   |   |   |   |
+   +   +---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+   +   +---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+   +
|   |   |   |   |   |   |   |   |       |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |       |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |       |   |   |
+---+---+---+---+---+---+---+   +---+---+
|   |   |   |   |   |   |   |       |   |
+---+---+---+---+---+---+---+---+---+---+
|   |       |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
```

### ETC6:23/3 40% 2

```
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+   +---+---+---+---+   +
|   |   |   |           |   |   |       |
+---+---+---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |       |
+---+---+---+---+---+---+---+---+---+   +
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+   +---+---+---+---+---+---+
|   |   |           |   |   |   |   |   |
+---+---+---+   +---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+   +   +---+---+
|   |   |   |   |   |       |       |   |
+---+---+---+---+---+---+   +   +---+---+
|   |   |   |   |   |   |       |   |   |
+---+---+---+---+---+---+---+---+---+---+
```

### ETC8:23/3 40% 2

```
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|       |   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |       |   |   |   |   |   |   |   |
+---+   +   +---+---+---+---+   +---+---+
|   |       |   |   |   |           |   |
+---+---+---+---+---+---+---+   +---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+---+---+---+
|       |   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+---+---+---+
|       |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
```

### ETC6:23/3 30% 3

```
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |           |   |   |   |
+   +---+---+---+---+   +---+---+---+---+
|       |   |   |   |   |   |   |   |   |
+   +---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+   +---+---+
|   |   |   |   |   |   |   |       |   |
+---+---+   +---+---+---+   +   +---+---+
|   |           |   |       |   |   |   |
+---+---+   +---+---+---+   +---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
```

### ETC8:23/3 30% 3

```
+---+---+---+---+---+---+---+---+---+---+
|   |       |       |   |   |   |   |   |
+   +   +---+---+   +---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+   +---+   +   +   +
|   |   |   |   |   |               |   |
+---+   +---+---+---+---+   +---+---+   +
|   |           |   |       |   |       |
+---+---+---+---+---+---+---+---+---+---+
|   |       |   |       |   |   |   |   |
+---+---+---+---+   +   +   +   +   +---+
|   |   |   |   |   |   |       |       |
+---+---+---+   +   +---+   +---+---+   +
|   |   |       |       |           |   |
+---+---+---+---+---+---+---+---+---+---+
```