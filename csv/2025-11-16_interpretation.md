# Interpretation of automata results from 2025-11-16

## Table of contents

1. Generations (n)
2. The number (k) of components
3. The number (e) of passages
4. The size (|K|) of the largest component
5. The number of isolated cells
6. The number of dead ends
7. 90-degree turns
8. Straightaways
9. Degree-3 cells
10. Degree-4 cells
11. Cells by degree
12. The good, the bad, and the ugly
13. Turning a maze into a perfect maze

## 1. Generations (n)

### Periodic behavior

The cellular automata proceed one generation at a time.  The state in generation *n+1* is completely determined by the state in generation *n*.  Since the number of possible states is finite (but quite large!), eventually there will be a generation with a state that is the same as that for an earlier generation.  If states of generation *N* and generation *N+T* are equal, then, under the given initial conditions, the automaton is periodic with period *T*, *i.e.*:

* Let *s(n)* denote the sequence of states of a finite cellular automaton with a given starting state *s(0)=s₀*.  Then:
    1. there exists a non-negative integer *N* and a positive integer *T* such that *s(N+T)=s(N)*; and
    2. for all integers *n ≥ N*, *s(n+T) = s(n)*.

What this means is that the automaton must eventually oscillate with a fixed period over a fixed set of states.  In practice, however, determining where the oscillation starts is hard.

### Stability

But there is at least one case that's easy to detect:

* If there is no change of state from generation *N* to generation *N+1*, then for all integers *n ≥ N*, *s(n+1) = s(n) = s(N)*.

If this situation occurs, then the automaton is *stable* for the given initial conditions.  (The initial conditions are the states of the cells in generation 0.)  Although the condition is easy to detect, it is in general hard to predict.  Basically the only general way of finding out is to step through, generation after generation.

### Population crash

If zero is not a member of the birth rule, and if there are no live cells at some generation *N*, then there will never be any live cells.  This is a special case of stability, a population *crash*.

Normally 0 is not a member of the birth rule, so this is normally the end of the story.  But what happens if 0 is a member of the birth rule?  In this case all cells in the next generation come to life.  For an automaton where every cell has the same number of neighbors, there are just two possibilities.

If the number of neighbors is in the death rule, all cells remain alive - a stable situation that is as uninteresting as the all-dead scenario.  If the number of neighbors is not in the death rule, all cells die in the next generation, giving an oscillation of period 2 between all cells dead and all cells alive.

Of course it is possible that not all cells have the same number of neighbors.  This doesn't happen on a toroidal grid, but it does happen on a rectangle.  But all the automata here are built on a torus.  (And none of the birth rules include 0.)

### Stability analysis

Here are the results with 50 generations for all of the tested automata:
```
algorithm                 n        s
ETC6:1234/23 40% 2    50.00     0.00  100% unstable after 50 generations
ETC6:1234/3 40% 2     50.00     0.00  100% unstable after 50 generations
ETC8:123/3 40% 2      50.00     0.00  100% unstable after 50 generations
ETC6:123/3 40% 2      50.00     0.00  100% unstable after 50 generations
ETC8:1234/23 40% 2    49.98     0.20  stable pct 1±10; crashes pct 0±0
ETC8:1234/3 40% 2     43.18    11.95  stable pct 25±43; crashes pct 0±0
ETC6:23/3 40% 2       35.27    10.04  stable pct 71±45; crashes pct 0±0
ETC6:2345/3 40% 2     25.09    10.97  stable pct 89±31; crashes pct 0±0
ETC8:2345/3 40% 2     14.38    11.99  stable pct 90±30; crashes pct 0±0
ETC8:12345/3 40% 2    13.58    14.74  stable pct 86±35; crashes pct 0±0
ETC6:12345/3 40% 2    12.15     2.82  stable pct 100±0; crashes pct 0±0
Wilson                 0.00     0.00  passage carver (BASELINE)
```

Wilson's algorithm is being used as a baseline.  But the notion of a generation is meaningless for Wilson's algorithm.  It runs until all cells have been visited.  We count that as stable but not crashing after the first generation.

In all of our samples, we used a bias of 40% -- approximately 40% of the cells in the automaton were randomly born in the first generation.  None of the automata crashed, but seven had at least one sample the reached a stable state.

Each automaton was sampled 100 times.  Note the following automata:

* ETC8:1234/23 40% 2 - The mean number of generations was 49.98.  Either one sample reached stability after 48 generations or two reached stability after 49 generations.  Since 1% of the samples were stable, it must be the former,
* ETC6:12345/3 40% 2 - all of the samples were stable after an average of 12.15 generations.  In all of the samples for this automaton, the number of generations to reach stability was less than fifty.

### Application to maze generation

An algorithm that reaches stability finalizes its maze...  If it reaches a stable state in just a few generation, there is less work for the program.

Apparently for a bias of 40% and with a 2-cell border, the following automata listed in increasing time efficiency order) are more time-efficient:

* ETC8:1234/3 40% 2
* ETC6:23/3 40% 2
* ETC6:2345/3 40% 2
* ETC8:2345/3 40% 2
* ETC8:12345/3 40% 2
* ETC6:12345/3 40% 2

For maze generation, "ETC6:23/3 40% 2" is probably the worst of all the algorithms for maze generation, but it does seem to share some of the characteristics of Conway's Game of Life, so it might be of interest from another point of view.

For actual maze generation, we need to look at some of the other statistics.

Note that the first one listed was among the four which never reached stability.

## 2. The number (*k*) of components

The number of cells in a 25×25 maze is given by *v=625*.

```
algorithm                 k        s
Wilson                 1.00     0.00  baseline (perfect maze/spanning tree)
ETC6:12345/3 40% 2     5.47     3.00  *k < v/40*  minimal fragmenting
ETC6:1234/23 40% 2     9.55     3.47  *k < v/40*  minimal fragmenting
ETC8:2345/3 40% 2     11.60     3.45  *k < v/40*  minimal fragmenting
ETC6:2345/3 40% 2     12.37     9.83  *k < v/40*  minimal fragmenting
ETC8:12345/3 40% 2    12.39     2.85  *k < v/40*  minimal fragmenting
ETC6:1234/3 40% 2     24.61     4.40  *k < v/20*  modest fragmenting
ETC8:1234/23 40% 2    28.27     4.47  *k < v/20*  modest fragmenting
ETC8:1234/3 40% 2     33.29     4.87  *k < v/10*  moderate fragmenting
ETC6:123/3 40% 2     195.82    20.38  *k < v/2*   severe fragmenting
ETC8:123/3 40% 2     250.32    20.82  *k < v/2*   severe fragmenting
ETC6:23/3 40% 2      522.34    13.53  *k ≥ v/2*   massive fragmenting
```

Here we sorted the results in increasing order by the number of components.  The bottom three had lots of fragments (or components) and are probably unsuitable for use in maze generation.  (*Caveat emptor*!  Suitability is an aesthetic condition -- just as a two people may have very different tastes in painting or music or sculpture; likewise two people may have very different tastes in maze generation.)

## 3. The number ($e$) of passages

The number of cells in a 25×25 maze is given by *v=625*.  The number of components is denoted *k*.  The Euler characteristic χ=*e-v+k is 0 for a tree or forest.  The Euler characteristic is always non-negative.  When positive, it indicates the presence of circuits.

```
algorithm                 e        s        k        χ  *(v-e)/k*
ETC6:23/3 40% 2      103.16    13.70   522.34     0.50     1.00
ETC8:123/3 40% 2     394.48    23.28   250.32    19.80     0.95
ETC6:123/3 40% 2     458.11    24.85   195.82    28.93     0.94
ETC8:1234/3 40% 2    598.25     5.84    33.29     6.54     0.99
ETC8:1234/23 40% 2   606.46     6.49    28.27     9.73     0.98
Wilson               624.00     0.00     1.00     0.00     1.00  baseline
ETC8:12345/3 40% 2   664.58     6.49    12.39    51.97     0.92
ETC8:2345/3 40% 2    669.80     6.47    11.60    56.40     0.92
ETC6:1234/3 40% 2    718.25    12.08    24.61   117.86     0.84
ETC6:1234/23 40% 2   783.38    13.19     9.55   167.93     0.79
ETC6:2345/3 40% 2    842.36    22.40    12.37   229.73     0.73
ETC6:12345/3 40% 2   850.45     9.85     5.47   230.92     0.73
```

All of the automata gave rise to some circuits.  The worst of the automata, "ETC6:23/3 40% 2", gave rise to very few, but only because it gave rise to many isolated cells.  As noted, this is easily the worst of the list for maze generation, but (if glider guns are configurable) it may be of interest in computing theory.

## 4. The size (|K|) of the largest component

If the largest component encompasses almost all the maze,then the fragments are not a major concern.  Ideally, the largest component should encompass all of the maze, but our cellular automata are prone to create fragments.  Our working definition of "nearly ideal" includes the stipulation that the largest fragment encompasses 3/4 of the maze.

```
algorithm               |K|        s
ETC6:23/3 40% 2        9.05     2.77  hopelessly fractured 99%
ETC8:123/3 40% 2      51.65    18.27  hopelessly fractured 92%
ETC6:123/3 40% 2     119.06    59.02  hopelessly fractured 81%
ETC8:1234/3 40% 2    230.70    90.60  hopelessly fractured 63%
ETC8:1234/23 40% 2   287.68    96.06  badly fractured 54%
ETC6:1234/3 40% 2    574.72    39.02  very nearly ideal 8%
ETC8:12345/3 40% 2   578.36    28.80  very nearly ideal 7%
ETC8:2345/3 40% 2    591.82    17.78  very nearly ideal 5%
ETC6:1234/23 40% 2   605.72    13.68  very nearly ideal 3%
ETC6:2345/3 40% 2    611.63    11.88  very nearly ideal 2%
ETC6:12345/3 40% 2   619.25     4.09  very nearly ideal 1%
Wilson               625.00     0.00  ideal 0%  (baseline)
```

## 5. The number of isolated cells

An isolated cell (or isolate or island) is a cell with no incident passages, or equivalently, a degree-0 cell.  Isolates aren't particularly desirable, but they aren't harmful.  They can be thought of as places where no ink should be used when sketching the maze.  A perfect maze carving algorithm (like Wilson's algorithm) doesn't produce isolated cells.  They are hard to avoid with cellular automata.

```
algorithm           islands        s      pct
Wilson                 0.00     0.00       0%  baseline
ETC6:12345/3 40% 2     3.86     2.88       1%
ETC8:12345/3 40% 2     4.72     2.05       1%
ETC8:2345/3 40% 2      5.15     2.53       1%
ETC6:1234/23 40% 2     5.53     2.65       1%
ETC8:1234/23 40% 2     5.77     2.51       1%
ETC8:1234/3 40% 2      5.95     2.34       1%
ETC6:2345/3 40% 2     10.59     9.36       2%
ETC6:1234/3 40% 2     18.77     3.72       3%
ETC6:123/3 40% 2     148.04    16.64      24%
ETC8:123/3 40% 2     185.66    18.10      30%
ETC6:23/3 40% 2      494.92    16.99      79%
```

## 6. The number of dead ends

A dead end is a cell with exactly one incident passages, or equivalently, a degree-1 cell.  Dead ends tend to be a matter of individual taste.  Some algorithms (like DFS or hunt-and-kill) produce very few.   Some (like Vertex Prim) tend to produce relatively many.   Here we see how our cellular automata fared.

```
algorithm         dead ends        s      pct
ETC6:12345/3 40% 2    17.19     6.07       3%
ETC6:2345/3 40% 2     23.06    10.27       4%
ETC6:1234/23 40% 2    27.80     6.68       4%
ETC6:1234/3 40% 2     32.20     5.53       5%
ETC8:2345/3 40% 2     85.52     8.01      14%
ETC8:12345/3 40% 2    87.89     7.24      14%
ETC6:23/3 40% 2       95.25    12.53      15%
ETC8:1234/23 40% 2    98.85     7.83      16%
ETC8:1234/3 40% 2    115.24     8.36      18%
ETC6:123/3 40% 2     168.98    12.78      27%
Wilson               181.19     7.36      29%  baseline
ETC8:123/3 40% 2     186.80    11.31      30%
```

## 7. 90-degree turns

In a 4-connected rectangular maze, a degree-2 cell can take one of six configurations.  Two of those involve going straight, *i.e*, horizontally from east to west (or *vice versa*) or vertically.  The remaining four are 90-degree turns.  Along the boundary walls, there is one way to go straight and two ways to turn.  In the four corner cells, there is one turn and no ways to go straight.

```
algorithm             turns        s straight degree-2      t/s
ETC6:23/3 40% 2        5.71     3.87     1.19     6.90     4.80
ETC6:2345/3 40% 2     97.81     9.62    46.02   143.83     2.13
ETC6:12345/3 40% 2   109.74    10.35    52.64   162.38     2.08
ETC8:123/3 40% 2     136.01    12.08    34.86   170.87     3.90
ETC6:123/3 40% 2     140.38    14.36    53.63   194.01     2.62
ETC6:1234/23 40% 2   168.01    13.08    81.37   249.38     2.06
Wilson               175.52    12.95   109.92   285.44     1.60  baseline
ETC6:1234/3 40% 2    215.04    13.36   108.40   323.44     1.98
ETC8:2345/3 40% 2    268.57    13.15    86.02   354.59     3.12
ETC8:12345/3 40% 2   277.92    13.40    84.23   362.15     3.30
ETC8:1234/3 40% 2    387.69    15.43    43.10   430.79     9.00
ETC8:1234/23 40% 2   416.23    14.48    33.28   449.51    12.51
```

On the basis of the analysis above, we might expect that the ratio of turns to straightaways in a uniform maze is about 2:1 on average, but our results for Wilson's algorithm, seem to suggest otherwise,  (Of course we have no information about the standard deviation or even whether this is a reasonable estimate for the mean.)

## 8. Straightaways

A degree-2 cell that doesn't turn must go straight.  It could be vertical or horizontal.  For a square maze, there is no reason to believe that an automaton with Conway-type rules would show a preference for horizontal over vertical, or *vice versa*.  Results bear this out.

```
algorithm             N/S    s    E/W    s    V/H
ETC6:23/3 40% 2      0.63±0.88   0.56±0.79   1.12
ETC8:1234/23 40% 2  16.50±4.23  16.78±4.34   0.98
ETC8:123/3 40% 2    17.99±4.44  16.87±4.47   1.07
ETC8:1234/3 40% 2   20.97±4.81  22.13±5.17   0.95
ETC6:2345/3 40% 2   23.00±4.14  23.02±4.87   1.00
ETC6:12345/3 40% 2  26.34±5.35  26.30±5.66   1.00
ETC6:123/3 40% 2    26.58±5.71  27.05±5.89   0.98
ETC6:1234/23 40% 2  40.53±7.56  40.84±8.26   0.99
ETC8:12345/3 40% 2  42.23±5.82  42.00±6.12   1.01
ETC8:2345/3 40% 2   43.38±6.67  42.64±6.51   1.02
ETC6:1234/3 40% 2   54.33±9.53  54.07±9.06   1.00
Wilson              56.05±7.86  53.87±8.78   1.04  baseline
```

## 9. Degree-3 cells

A degree-3 cell is incident to three passages -- it islinked by passages to three of its neighbors.

```
algorithm             deg=3        s      pct
ETC6:23/3 40% 2       14.45     4.80       2%
ETC8:123/3 40% 2      66.26    10.11      11%
ETC8:1234/23 40% 2    68.43     7.45      11%
ETC8:1234/3 40% 2     72.40     7.43      12%
ETC6:123/3 40% 2      96.66    11.79      15%
Wilson               137.55     7.74      22%  baseline
ETC8:12345/3 40% 2   163.99     9.27      26%
ETC8:2345/3 40% 2    174.06    10.23      28%
ETC6:1234/3 40% 2    244.94    18.14      39%
ETC6:1234/23 40% 2   328.96    19.75      53%
ETC6:12345/3 40% 2   407.33    14.20      65%
ETC6:2345/3 40% 2    416.08    20.13      67%
```

## 10. Degree-4 cells

A degree-4 cell is incident to four passages -- it islinked by a passage to each of its four neighbors.

```
algorithm             deg=4        s     pct
ETC8:1234/3 40% 2      0.62     0.78       0%
ETC8:1234/23 40% 2     2.44     1.89       0%
ETC6:1234/3 40% 2      5.65     2.01       1%
ETC8:2345/3 40% 2      5.68     2.15       1%
ETC8:12345/3 40% 2     6.25     2.40       1%
ETC6:1234/23 40% 2    13.33     4.41       2%
ETC6:23/3 40% 2       13.48     3.32       2%
ETC8:123/3 40% 2      15.41     4.21       2%
ETC6:123/3 40% 2      17.31     4.64       3%
Wilson                20.82     3.83       3%  baseline
ETC6:2345/3 40% 2     31.44     6.17       5%
ETC6:12345/3 40% 2    34.24     5.21       5%
```

## 11. Cells by degree

```
algorithm              0      1      2      3      4  total=100%
Wilson                 0%    29%    46%    22%     3%   100%  baseline
ETC6:12345/3 40% 2     1%     3%    26%    65%     5%   100%
ETC6:2345/3 40% 2      2%     4%    23%    67%     5%   101%
ETC6:1234/23 40% 2     1%     4%    40%    53%     2%   100%
ETC8:2345/3 40% 2      1%    14%    57%    28%     1%   101%
ETC8:12345/3 40% 2     1%    14%    58%    26%     1%   100%
ETC6:1234/3 40% 2      3%     5%    52%    39%     1%   100%
ETC8:1234/23 40% 2     1%    16%    72%    11%     0%   100%
ETC8:1234/3 40% 2      1%    18%    69%    12%     0%   100%
ETC6:123/3 40% 2      24%    27%    31%    15%     3%   100%
ETC8:123/3 40% 2      30%    30%    27%    11%     2%   100%
ETC6:23/3 40% 2       79%    15%     1%     2%     2%    99%

                              Rounding affects some of the totals.
```

## 12. The good, the bad, and the ugly

(With apologies to Sergio Leone!)

Listed here are the automata that were tested, along with comments about their suitability for maze generation.  (As noted above, *suitability* is an aesthetic criterion.)  Each automaton was used to create one hundred 25×25 mazes.

The first cut:

* **ETC6:123/3 40% 2** -- hopelessly fractured 81%
* **ETC6:1234/23 40% 2** -- badly fractured 54%
* **ETC6:1234/3 40% 2**
* **ETC6:12345/3 40% 2**
* **ETC6:23/3 40% 2** -- hopelessly fractured 99%
* **ETC6:2345/3 40% 2**
* **ETC8:123/3 40% 2** -- hopelessly fractured 92%
* **ETC8:1234/23 40% 2**
* **ETC8:1234/3 40% 2** - hopelessly fractured 63%
* **ETC8:12345/3 40% 2**
* **ETC8:2345/3 40% 2**

After removing the automata that showed severe fracturing resulting from a small largest component, we are left with:

* **ETC6:1234/3 40% 2** -- *k < v/20*  modest fragmenting
* **ETC6:12345/3 40% 2**
* **ETC6:2345/3 40% 2**
* **ETC8:1234/23 40% 2** -- *k < v/20*  modest fragmenting
* **ETC8:12345/3 40% 2**
* **ETC8:2345/3 40% 2**

Removing the two with modest fragmentation:

* **ETC6:12345/3 40% 2**
* **ETC6:2345/3 40% 2**
* **ETC8:12345/3 40% 2**
* **ETC8:2345/3 40% 2**

Now let's get some examples.  I start by pulling in the script I used to create the CSV.  It has hyphens in the name so I need to use a Python trick:
```
$ python
Python 3.10.12
>>> from importlib import import_module
>>> script = import_module("stats.2025-11-16_automata")
```

A 25×25 maze is too big so I need to reduce the number of columns. I'll also reduce the number of rows:
```
>>> script.ROWS = 8
>>> script.COLS = 13
```

*ROWS* and *COLS* are global variables in the Python script:

* stats/2025-11-16_automata.py

Now I'm ready.  Let's do these in turn:

### Example 1: *ETC6:12345/3 40% 2*

```
>>> stat, maze = script.run_ca1("12345/3", 40, 2, verbose=True)
generation 0: (automaton) 119 alive; (maze) 73 passages.
generation 1: (automaton) 171 alive; (maze) 105 passages.
generation 2: (automaton) 200 alive; (maze) 121 passages.
generation 3: (automaton) 198 alive; (maze) 128 passages.
generation 4: (automaton) 209 alive; (maze) 132 passages.
generation 5: (automaton) 216 alive; (maze) 135 passages.
generation 6: (automaton) 213 alive; (maze) 133 passages.
generation 6: stable configuration
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |       |       |       |       |
+---+   +   +   +   +   +   +   +   +---+   +   +   +
|   |       |               |       |           |   |
+   +   +   +   +---+   +   +   +   +   +---+---+   +
|   |   |       |                   |               |
+   +   +---+   +   +---+---+---+   +   +---+   +   +
|               |                                   |
+---+---+   +   +   +---+   +   +---+---+   +   +---+
|       |       |           |               |       |
+   +   +   +   +   +   +   +   +---+   +---+---+   +
|           |               |       |               |
+   +   +   +   +---+   +   +   +   +   +   +   +   +
|       |               |       |       |           |
+---+   +   +   +   +---+   +   +   +   +   +   +---+
|       |       |           |       |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(stat)
{'name': 'ETC6:12345/3 40% 2', 'generations': 6, 'stable': 1, 'all die': 0, 'k': 2, 'e': 133, 'v': 104, 'largest': 103, 'isolates': 1, 'dead_ends': 4, 'turns': 34, 'northbound': 3, 'eastbound': 4, 'degree 3': 52, 'degree 4': 6}
```

Convergence to a stable state in just six generations... Quick!  Let's analyze that last line:

* name:'ETC6:12345/3 40% 2' -- the algorithm name: birth rule {3}, death rule {1,2,3,4,5}, edge-based on a torus.  The two-cell border tells us that the torus has ten rows and 15 columns.  Our initial conditions set cells as live with 40% probability.
* generations:6 - 6 generations before stability.  Obviously some grid edges did not die.
* k:2 -- 2 components.  (Not bad!)
* e:133 -- 133 passages in the maze.
* v:104 -- 104 cells in the maze.  (8•13=104.)
* largest:103 -- 103 cells in the largest component.  The other component is the isolated cell in the southeast corner.
* isolates:1 -- one island.
* dead_ends:4 -- just four dead ends.
* turns:34, northbound:3, eastbound:4 -- a total of 41 cells of degree 2.
* degree 3:52, degree 4:6
* *e-v+k* = 133 - 104 + 2 = 21.  We would need to remove 21 passages without disconnecting the large component in order to obtain a forest with two components. There are at least twenty-one circuits.  (Clearly there are more as there are obviously some interlocked circuits.)

It's not a difficult maze, but it's definitely more difficult than a labyrinth.  I'd call it a success.

### Example 2: *ETC6:2345/3 40% 2*

```
>>> stat, maze = script.run_ca1("2345/3", 40, 2, verbose=True)
generation 0: (automaton) 117 alive; (maze) 77 passages.
generation 1: (automaton) 137 alive; (maze) 93 passages.
generation 2: (automaton) 143 alive; (maze) 91 passages.
generation 3: (automaton) 156 alive; (maze) 98 passages.
generation 4: (automaton) 160 alive; (maze) 100 passages.
generation 5: (automaton) 167 alive; (maze) 106 passages.
generation 6: (automaton) 174 alive; (maze) 108 passages.
generation 7: (automaton) 179 alive; (maze) 111 passages.
generation 8: (automaton) 176 alive; (maze) 109 passages.
generation 9: (automaton) 180 alive; (maze) 112 passages.
generation 10: (automaton) 186 alive; (maze) 117 passages.
generation 11: (automaton) 193 alive; (maze) 121 passages.
generation 12: (automaton) 194 alive; (maze) 120 passages.
generation 13: (automaton) 199 alive; (maze) 124 passages.
generation 14: (automaton) 206 alive; (maze) 129 passages.
generation 15: (automaton) 207 alive; (maze) 128 passages.
generation 16: (automaton) 212 alive; (maze) 132 passages.
generation 17: (automaton) 213 alive; (maze) 131 passages.
generation 18: (automaton) 213 alive; (maze) 131 passages.
generation 19: (automaton) 214 alive; (maze) 131 passages.
generation 20: (automaton) 217 alive; (maze) 131 passages.
generation 21: (automaton) 219 alive; (maze) 134 passages.
generation 21: stable configuration
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |       |       |               |
+---+   +---+   +   +   +   +   +   +   +   +   +---+
|   |               |   |       |   |               |
+   +   +   +---+---+   +   +   +   +   +   +---+   +
|       |               |           |   |           |
+---+   +   +   +   +   +   +---+   +   +   +   +   +
|               |           |               |       |
+   +---+---+   +   +---+   +   +---+---+   +   +   +
|                           |               |       |
+---+   +   +---+---+   +   +---+   +   +   +   +   +
|       |           |                               |
+   +   +   +   +   +   +   +   +---+---+---+---+   +
|       |       |   |   |                           |
+---+---+   +   +   +   +   +   +   +   +   +   +---+
|           |       |           |       |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(stat)
{'name': 'ETC6:2345/3 40% 2', 'generations': 21, 'stable': 1, 'all die': 0, 'k': 2, 'e': 134, 'v': 104, 'largest': 103, 'isolates': 1, 'dead_ends': 5, 'turns': 28, 'northbound': 5, 'eastbound': 1, 'degree 3': 61, 'degree 4': 3}
```

*e=134*, *v=104*, *k*=2, *e-v+k*=32.

The larger component contains every cell except the southeast corner.  Again, it's not a hard maze, but it isn't shabby.  I'd also rate this one as a success.

### Example 3: *ETC8:12345/3 40% 2*

The same rules as the maze generator in Example 1, but each grid edge now has eight neighboring edges...  Convergence is again very quick...

```
>>> stat, maze = script.run_ca2("12345/3", 40, 2, verbose=True)
generation 0: (automaton) 110 alive; (maze) 74 passages.
generation 1: (automaton) 160 alive; (maze) 113 passages.
generation 2: (automaton) 153 alive; (maze) 100 passages.
generation 3: (automaton) 158 alive; (maze) 105 passages.
generation 4: (automaton) 163 alive; (maze) 103 passages.
generation 5: (automaton) 164 alive; (maze) 104 passages.
generation 6: (automaton) 165 alive; (maze) 103 passages.
generation 7: (automaton) 164 alive; (maze) 103 passages.
generation 7: stable configuration
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               |           |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   |       |       |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |       |       |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |           |   |       |   |       |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D |           |           |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       |       |                       |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |           |       |   |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   |               |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(stat)
{'name': 'ETC8:12345/3 40% 2', 'generations': 7, 'stable': 1, 'all die': 0, 'k': 5, 'e': 103, 'v': 104, 'largest': 92, 'isolates': 2, 'dead_ends': 20, 'turns': 46, 'northbound': 4, 'eastbound': 11, 'degree 3': 20, 'degree 4': 1}
```

*e=103*, *v=104*, *k*=5, *e-v+k*=4.

More nearly perfect, but near perfect came at a cost -- more components.  But the largest component encompasses all but 12 cells.  The four small components in ascending size order respectively contain 1, 1, 2 and 8 cells.  Despite the fragmentation, I'd call this a definite success.

There is one circuit with just four cells, but there are some interesting longer interlocking circuits

### Example 4: *ETC8:2345/3 40% 2*

Another quickly converging automaton...

```
>>> stat, maze = script.run_ca2("2345/3", 40, 2, verbose=True)
generation 0: (automaton) 119 alive; (maze) 76 passages.
generation 1: (automaton) 154 alive; (maze) 101 passages.
generation 2: (automaton) 147 alive; (maze) 93 passages.
generation 3: (automaton) 153 alive; (maze) 96 passages.
generation 4: (automaton) 160 alive; (maze) 99 passages.
generation 5: (automaton) 169 alive; (maze) 104 passages.
generation 6: (automaton) 161 alive; (maze) 100 passages.
generation 7: (automaton) 158 alive; (maze) 97 passages.
generation 8: (automaton) 156 alive; (maze) 96 passages.
generation 9: (automaton) 166 alive; (maze) 105 passages.
generation 10: (automaton) 168 alive; (maze) 107 passages.
generation 11: (automaton) 169 alive; (maze) 106 passages.
generation 11: stable configuration
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |           |       |       |   | A   A |
+---+   +---+   +---+   +---+   +---+   +   +   +---+
|       |       |               |           | A |   |
+   +   +   +---+---+---+   +---+   +---+   +---+   +
|   |   |           |       |               |       |
+   +   +   +   +---+   +   +   +---+---+   +   +   +
|   |       |           |       |       |       |   |
+---+   +---+---+   +---+---+---+   +   +---+   +---+
|           |                       |               |
+   +---+   +   +---+---+   +---+   +---+---+---+   +
|       |   |       |       |       | B   B   B |   |
+   +---+   +---+   +---+---+   +   +   +---+   +---+
|   |           |               |   | B   B | B   B |
+---+   +---+   +---+---+---+   +---+---+   +   +   +
|           |               |   | B   B   B | B   B |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(stat)
{'name': 'ETC8:2345/3 40% 2', 'generations': 11, 'stable': 1, 'all die': 0, 'k': 3, 'e': 106, 'v': 104, 'largest': 89, 'isolates': 0, 'dead_ends': 22, 'turns': 42, 'northbound': 3, 'eastbound': 11, 'degree 3': 26, 'degree 4': 0}
```

*e=106*, *v=104*, *k*=3, *e-v+k*=5.

Alsp nearly perfect, but at a cost -- larger small components.  The largest component encompasses all but 15 cells.  The two small components in ascending size order respectively contain 3 and 12 cells.  I'd rate this as another success.  There are some interesting circuits...

## 13. Turning a maze into a perfect maze

### Example 5: Turning Example 3 into a perfect maze

```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               |           |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   |       |       |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |       |       |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |           |   |       |   |       |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D |           |           |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       |       |                       |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |           |       |   |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   |               |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We start by calculating the Euler characteristic:

* *e=103*, *v=104*, *k*=5, *e-v+k*=4.

To turn this into a forest, we need to remove four passages without increasing the number of components.  Our first step is to find a circuit... None of our circuits are in the three small components. But there is an obvious one in the large component!  Then we break the circuit by removing a passage:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               |           |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   |       |       |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |       |       |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |           |   |       |   | X | X |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D |           |           | X   X |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       |       |                       |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |           |       |   |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   |               |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

* *e=102*, *v=104*, *k*=5, *e-v+k*=3.

And again!
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               |           |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   |       |       |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |       | X | X |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |           | X | X   X |   |   |   |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D |         X |     X     |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       | X   X | X   X   X             |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |         X |       | X |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   | X   X   X   X |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

* *e=101*, *v=104*, *k*=5, *e-v+k*=2.

And again!
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               |           |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   |       |       |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |       |   |   |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |           |   |       |   |   |   |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D | X   X   X |           |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D | X   X | X   X |                       |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       | X   X | X |       |   |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   |               |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

* *e=100*, *v=104*, *k*=5, *e-v+k*=1.

And again!
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               | X   X   X |   |               |
+---+   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   | X   X | X   X |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |     X |   | X |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |     X | X |   | X   X |   |   |   |       |
+---+---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D | X   X   X |     X     |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       | X   X | X   X   X             |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |       | X |       | X |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B |                   | X   X   X   X |   | C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

* *e=99*, *v=104*, *k*=5, *e-v+k*=0.

Phase 1 complete.  Now we just need four passages to connect the five components.  Since all of the small components border the large component, we simply need to break down one wall each between the large component and a smaller component.  We could instead use the boundary between B and D as one of the four passages:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A |               | X   X   X |   |               |
+   +   +---+   +---+   +---+   +   +---+   +---+   +
|       |   |   | X   X | X   X |       |       |   |
+   +---+   +   +   +---+   +---+---+   +---+   +---+
|   |       |     X |   | X |               |       |
+---+   +   +---+   +   +   +---+   +---+   +   +---+
|       |     X | X |   | X   X |   |   |   |       |
+   +---+---+   +---+   +---+   +   +   +   +   +---+
| D | D   D | X   X   X |     X     |       |       |
+   +   +   +   +---+   +---+   +---+---+---+---+   +
| D   D | D |       | X   X | X   X   X             |
+---+   +---+---+   +---+   +---+   +   +---+---+   +
| D   D |       |       | X |       | X |           |
+---+---+   +---+---+   +   +---+---+   +   +---+---+
| B                     | X   X   X   X |     C   C |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

* *e=103*, *v=104*, *k*=1, *e-v+k*=0.

Note that the choice of a passage in a circuit was completely arbitrary in the first phase and the choice of a wall between two components was completely arbitrary in the second phase.

Depth-first search is one algorithm that could be used to find a circuit or to find a connecting wall.