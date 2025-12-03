# Interpretation of wall builder results from 2025-11-23

## Table of contents

*Introduction*

*Notation*

<ol>
<li>Isolated cells</li>
<li>Dead ends</li>
<li>Degree-2 cells
    <ol type="a">
    <li>Horizontal or E/W passages</li>
    <li>Vertical or N/S passages</li>
    <li>90° turns</li>
    </ol>
</li>
<li>Degree-3 cells</li>
<li>Degree-4 cells</li>
<li>Diameter</li>
</ol>

*Appendices*
<ol type="A">
<li>Efficiency (time)</li>
<li>Euler analysis</li>
</ol>

### Introduction

Wilson's algorithm, the Aldous/Broder random walk algorithm, and the depth-first search passage carver (aka *DFS* or *recursive backtracker*) were used as controls.

The remaining algorithms are wall builders that use a stack, a queue or a priority queue to remove one passage at a time (to break a circuit) starting with a complete maze. For a 21x34 complete maze, this mandates the removal of 660 passages to end with a perfect maze.

### Notation

The wall building algorithms are named as follows:

* WB/DFS - depth-first circuit detection
* WB/BFS - breadth-first circuit detection
* WB/PQ(x) - priority queue circuit detection.  The character in parentheses has the value "e" for edge, "v" for vertex, and "a" for arc.  The arc priorities are based on a (cell, passage) ordered pair where the cell is the passage entrance.  Edge and vertex priorities are based on passages and cells, respectively.

In addition:
* WB/queue shuffle - neighborhoods are shuffled before they are traversed
* WB/queue seq - neighborhoods are not shuffled before they are traversed
* WB/queue seq SW - circuit locator calls start in the southwest corner
* WB/queue seq center - circuit locator calls start in the center of the grid in row 10 column 17.

As will be seen in appendix A, performance degrades significantly when a fixed starting cell is used.  Shuffling generally improves performance, but the passage carvers here nd in previous tests tend to perform considerably better than this particular family of wall builders.

## 1. Isolated cells

An isolated cell (or isolate or island) is a cell with no incident passages, or equivalently, a degree-0 cell.  A connected maze with more than 1 cell will never have any isolated cells.

Since all the sampled algorithm produced connected mazes, no isolated cells were encountered.  This column of results was as expected.

## 2. Dead ends.

A dead end is a cell with exactly one incident passages, or equivalently, a degree-1 cell.  Dead ends tend to be a matter of individual taste.  Some algorithms (like DFS or hunt-and-kill) produce very few.   Some (like Vertex Prim) tend to produce relatively many.   Here are the results for the sampled algorithms.

Each algorithm was sampled 100 times.

```
algorithm                  dead ends    stdev      pct
-------------------------  ---------  -------  -------
WB/DFS seq SW                   2.00     0.00       0%  constant
WB/DFS seq center               3.00     0.00       0%  constant
WB/BFS seq SW                  34.00     0.00       5%  constant
WB/DFS seq                     38.52     6.83       5%
WB/BFS seq center              54.00     0.00       8%  constant
DFS                            74.19     4.95      10%
WB/DFS shuffle                151.77     7.12      21%
WB/PQ(v) seq                  201.12     5.91      28%
WB/PQ(e) seq                  201.80     7.29      28%
WB/PQ(e) shuffle              202.60     6.52      28%
WB/PQ(v) shuffle              203.02     7.77      28%
WB/PQ(e) seq SW               203.67     7.28      29%
WB/PQ(v) seq SW               204.28     7.59      29%
WB/PQ(e) seq center           205.32     7.96      29%
WB/PQ(v) seq center           205.36     6.67      29%
WB/BFS shuffle                207.25     7.51      29%
Wilson                        207.39     7.84      29%  baseline
Aldous/Broder                 207.86     6.46      29%
WB/BFS seq                    208.11     8.29      29%
WB/PQ(a) shuffle              220.33     6.65      31%
WB/PQ(a) seq                  221.75     8.04      31%
WB/PQ(a) seq center           310.14     7.53      43%
WB/PQ(a) seq SW               314.24     6.01      44%
```

Four algorithms ended with exactly the same number of dead ends in all the samples.

* Circuit removal using a depth-first search ended in a single chain if the search started in the southwest corner and the neighborhoods were traversed in their dictionary order.
* If a cell near the center was used instead, DFS circuit removal resulted in a long chain with one branch, reminiscent of the letter Y.
* When breadth-first search was used with a fixed starting point and no shuffling of the neighborhood, there was a small amount of branching ending in shorter chains.

When neighborhoods were shuffled, the depth-first circuit remover produced the lowest average number of dead ends, but not nearly as few as its passage carving counterpart.

The breadth-first and priority queue circuit removers had numbers of dead ends that were fairly close to uniform (Aldous/Broder and Wilson) when allowed to start randomly. Breadth-first without shuffling was extremely close.

The DFS circuit removers produced significantly fewer dead ends.  Arc priorities resulted in higher than uniform numbers, significantly higher when a fixed starting cell was used.

## 3. Degree-2 cells.

A degree-2 cell is incident to two passages -- it is linked by passages to two of its neighbors.  Degree-2 cells, in one sense, reflect an absence of choice: if we enter via one of the passages, then we must typically exit via the other.

```
algorithm                   degree 2    stdev      pct
-------------------------  ---------  -------  -------
WB/PQ(a) seq SW               160.38    10.41      22%
WB/PQ(a) seq center           166.91    11.66      23%
WB/PQ(a) seq                  299.79    13.52      42%
WB/PQ(a) shuffle              302.18    11.92      42%
WB/BFS seq                    322.39    14.90      45%
WB/BFS shuffle                323.22    13.01      45%
Aldous/Broder                 323.72    11.35      45%
Wilson                        324.92    13.87      46%  baseline
WB/PQ(e) seq center           327.77    14.53      46%
WB/PQ(v) seq center           328.06    12.59      46%
WB/PQ(v) seq SW               329.17    13.31      46%
WB/PQ(e) seq SW               329.92    12.51      46%
WB/PQ(v) shuffle              331.04    14.13      46%
WB/PQ(e) shuffle              331.81    11.79      46%
WB/PQ(e) seq                  333.35    13.90      47%
WB/PQ(v) seq                  335.50    10.53      47%
WB/DFS shuffle                420.06    13.46      59%
DFS                           568.61     9.71      80%
WB/BFS seq center             618.00     0.00      87% constant
WB/DFS seq                    639.14    13.59      90%
WB/BFS seq SW                 648.00     0.00      91% constant
WB/DFS seq center             710.00     0.00      99% constant
WB/DFS seq SW                 712.00     0.00   † 100% constant

Notes:
(†) Not quite 100%.  There were two dead ends.
```
The algorithms that produced more degree-2 cells on average than DFS also produced very few dead ends.  The mazes in this set are commonly described as labyrinths.

Arc priorities produced greater than uniform numbers of dead ends, so, not unexpectedly, they produced fewer on average numbers of degree-2 cells.

With four directions, there are C(4,2)=6 ways of choosing two directions.  One possibility is east and west.  A second possibility is north and south.  There are four other combinations.  A degree-2 cell with passages east and west might be described as horizontal, while one with north and south passages might be called vertical.  The four remaining combinations are right-angled turns.

### 3a. Horizontal or E/W passages

```
algorithm                        E/W    stdev      pct
-------------------------  ---------  -------  -------
WB/BFS seq SW                   0.00     0.00       0%  no horizontals
WB/PQ(a) seq SW                41.18     6.45       6%
WB/PQ(a) seq center            42.57     6.63       6%
WB/PQ(a) seq                   62.20     8.33       9%
Wilson                         64.96     8.76       9%  baseline
Aldous/Broder                  65.43     8.70       9%
WB/PQ(e) seq                   67.65     8.80       9%
WB/PQ(v) seq                   68.19     7.37      10%
WB/PQ(a) shuffle               68.56     9.20      10%
WB/PQ(e) shuffle               73.50     8.99      10%
WB/PQ(v) shuffle               75.00     7.60      11%
WB/BFS shuffle                 76.30     9.72      11%
WB/PQ(e) seq center            79.77     9.65      11%
WB/PQ(v) seq center            79.88     9.83      11%
WB/PQ(e) seq SW                88.14    12.34      12%
WB/PQ(v) seq SW                88.79    12.37      12%
WB/DFS shuffle                 89.46    10.67      13%
DFS                           118.54    13.18      17%
WB/BFS seq                    130.48    13.80      18%
WB/BFS seq center             310.00     0.00      43%  constant
WB/DFS seq                    335.45    39.83      47%
WB/DFS seq center             611.00     0.00      86%  constant
WB/DFS seq SW                 672.00     0.00      94%  constant
```

### 3b. Vertical or N/S passages

With *m*=21 rows and *n*=34 columns, there are*v*=714 cells.  Among these cells, *m*(*n*-2)=672 cells have neighbors both east and west, and (*m*-2)*n*=646 have neighbors both north and south.  An unbiased algorithm should have, on average, a ratio of about 1.040 horizontal to vertical.

Wilson's algorithm and Aldous/Broder produced results quite close to this guess.

```
algorithm                         NS    stdev      pct      H/V
-------------------------  ---------  -------  -------  -------
WB/DFS seq SW                   0.00     0.00       0%      inf  no verticals
WB/DFS seq center              19.00     0.00       3%    32.16  constant
WB/DFS seq                     20.81     8.42       3%    16.12
WB/BFS seq                     34.63     7.13       5%     3.77
WB/PQ(a) seq SW                36.05     5.91       5%     1.14
WB/PQ(a) seq center            37.52     5.88       5%     1.13
WB/PQ(v) seq SW                56.86    10.13       8%     1.56
WB/PQ(e) seq SW                58.68    10.13       8%     1.50
Wilson                         60.66     8.76       8%     1.07  baseline
Aldous/Broder                  61.37     7.58       9%     1.07
WB/PQ(a) shuffle               62.31     8.59       9%     1.10
WB/PQ(e) seq center            66.78     9.12       9%     1.19
WB/PQ(v) seq center            66.82     9.65       9%     1.20
WB/PQ(a) seq                   67.28     8.47       9%     0.92
WB/PQ(v) shuffle               67.50     8.79       9%     1.11
WB/PQ(e) shuffle               68.21     9.80      10%     1.08
WB/BFS shuffle                 68.97     8.79      10%     1.11
WB/PQ(e) seq                   76.33     9.35      11%     0.89
WB/PQ(v) seq                   77.01     9.82      11%     0.89
WB/DFS shuffle                 77.82    10.01      11%     1.15
DFS                           106.78    13.31      15%     1.11
WB/BFS seq center             306.00     0.00      43%     1.01  constant
WB/BFS seq SW                 646.00     0.00      90%     0.00  constant
```
Starting in the southwest corner and traversing neighborhoods with out shuffling with the DFS circuit finder resulted in a single chain with no vertical segments.  (Ratio is infinite).  The maze looks something like the following 3x5 maze:
```
    +---+---+---+---+---+
    | T   H   H   H   X |        Legend:
    +   +---+---+---+---+             H - degree-2, horizontal
    | T   H   H   H   T |             T - degree-2, right-angle turn
    +---+---+---+---+   +             X - dead end
    | X   H   H   H   T |
    +---+---+---+---+---+
```
Cells in the first and last column were *turns*, except for the ends of the chain.  The remaining cells were degree-2 horizontal cells.

At the opposite end of the spectrum, with a ratio of 0, the BFS counterpart produced mazes that look something like this:
```
    +---+---+---+---+---+
    | X | X | X | X | X |        Legend:
    +   +   +   +   +   +             V - degree-2, vertical
    | V | V | V | V | V |             T - degree-2, right-angle turn
    +   +   +   +   +   +             X - dead end
    | V | V | V | V | V |             D - degree-3, decision
    +   +   +   +   +   +
    | T | D | D | D | T |
    +---+---+---+---+---+
```
In this case, the bottom corners were turns, the rest of the bottom row were decision cells, the top row were dead ends and cells in other row were degree-2 verticals.

For the DFS circuit remover starting in the center, the following run gives rough idea of the result:
```
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
>>> maze = Maze(OblongGrid(5, 8)); maze.link_all()
>>> print(BasicWallbuilder.on(maze, start_cell=maze.grid[2,4], shuffle=False))
          maze algorithm (statistics)
                            visits       29
                           locator  Circuit Locator
                        start cell  (2, 4)
                     finder passes     1357
                           unlinks       28
>>> print(maze)
+---+---+---+---+---+---+---+---+
| X                       Y   X |
+---+---+---+---+---+---+   +---+
|                       |       |    Legend:
+   +---+---+---+---+   +---+   +       #  start cell (dead end)
|               | # |   |       |       X  dead ends
+---+---+---+   +   +   +   +---+       Y  decision (degree 3)
|               |   |   |       |       blank  degree 2
+   +---+---+---+   +   +---+   +
|                   |           |
+---+---+---+---+---+---+---+---+
```

Here is a run showing the BFS counterpart starting in the center:
```
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.WallBuilders.bfs_wallbuilder import BFSWallbuilder
>>> maze = Maze(OblongGrid(5, 8)); maze.link_all()
>>> print(BFSWallbuilder.on(maze, start_cell=maze.grid[2,4], shuffle=False))
          maze algorithm (statistics)
                            visits       29
                           locator  BFS Circuit Locator
                        start cell  (2, 4)
                     finder passes     1770
                           unlinks       28
>>> print(maze)
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |    Legend:
+   +   +   +   +   +   +   +   +       #  start cell (degree 4)
|     Y   Y   Y   #   Y   Y     |       4  degree 4
+---+---+---+---+   +---+---+---+       Y  degree 3
|                 4             |
+---+---+---+---+   +---+---+---+
|                 Y             |
+---+---+---+---+---+---+---+---+
```

### 3c. 90° turns

```
algorithm                       turn    stdev      pct
-------------------------  ---------  -------  -------
WB/BFS seq SW                   2.00     0.00       0%  constant
WB/BFS seq center               2.00     0.00       0%  constant
WB/DFS seq SW                  40.00     0.00       6%  constant
WB/DFS seq center              80.00     0.00      11%
WB/PQ(a) seq SW                83.15     8.46      12%
WB/PQ(a) seq center            86.82     9.24      12%
WB/BFS seq                    157.28    13.09      22%
WB/PQ(a) seq                  170.31    11.24      24%
WB/PQ(a) shuffle              171.31    11.63      24%
WB/BFS shuffle                177.95    11.02      25%
WB/PQ(e) seq center           181.22    11.61      25%
WB/PQ(v) seq center           181.36    11.03      25%
WB/PQ(e) seq SW               183.10    11.03      26%
WB/PQ(v) seq SW               183.52    11.94      26%
WB/PQ(v) shuffle              188.54    13.10      26%
WB/PQ(e) seq                  189.37    11.09      27%
WB/PQ(e) shuffle              190.10    11.49      27%
WB/PQ(v) seq                  190.30    10.63      27%
Aldous/Broder                 196.92    11.09      28%
Wilson                        199.30    11.17      28%  baseline
WB/DFS shuffle                252.78    13.24      35%
WB/DFS seq                    282.88    27.96      40%
DFS                           343.29    12.47      48%
```

## 4. Degree-3 cells.

A degree-3 cell is incident to three passages -- it islinked by passages to three of its neighbors.  Given an entrance, a degree-3 cell represents a choice of two separate exits.

```
algorithm                   degree 3        s      pct
WB/DFS seq SW                   0.00     0.00       0%  constant (zero)
WB/DFS seq center               1.00     0.00       0%  constant
WB/BFS seq SW                  32.00     0.00       4%  constant
WB/BFS seq center              32.00     0.00       4%  constant
WB/DFS seq                     36.16     6.74       5%
DFS                            70.21     4.92      10%
WB/DFS shuffle                134.57     7.09      19%
WB/PQ(v) seq                  155.64     7.63      22%
WB/PQ(v) seq center           157.80     8.00      22%
WB/PQ(e) seq                  157.90     9.46      22%
Wilson                        157.99     7.17      22%  baseline
WB/PQ(e) seq center           158.50     8.57      22%
WB/PQ(e) shuffle              158.58     7.86      22%
WB/PQ(v) seq SW               158.82     7.73      22%
WB/PQ(v) shuffle              158.86     8.48      22%
Aldous/Broder                 158.98     7.87      22%
WB/PQ(e) seq SW               159.15     7.71      22%
WB/BFS seq                    160.89     8.84      23%
WB/BFS shuffle                161.81     7.96      23%
WB/PQ(a) shuffle              164.65     7.91      23%
WB/PQ(a) seq                  165.17     8.32      23%
WB/PQ(a) seq center           165.76     8.33      23%
WB/PQ(a) seq SW               166.52    10.18      23%
```

## 5. Degree-4 cells.

A degree-4 cell is incident to four passages -- it islinked by a passage to each of its four neighbors.  Given an entrance, a degree-4 cell represents a choice of three separate exits.

```
algorithm                   degree 4        s     pct
WB/DFS seq SW                   0.00     0.00       0%  constant
WB/DFS seq center               0.00     0.00       0%  constant
WB/BFS seq SW                   0.00     0.00       0%  constant
WB/DFS seq                      0.18     0.43       0%
DFS                             0.99     1.06       0%
WB/DFS shuffle                  7.60     2.66       1%
WB/BFS seq center              10.00     0.00       1%  constant
WB/PQ(e) seq                   20.95     4.30       3%
WB/PQ(e) shuffle               21.01     4.10       3%
WB/PQ(v) shuffle               21.08     4.23       3%
WB/PQ(e) seq SW                21.26     4.55       3%
WB/BFS shuffle                 21.72     4.59       3%
WB/PQ(v) seq SW                21.73     4.30       3%
WB/PQ(v) seq                   21.74     4.16       3%
WB/PQ(e) seq center            22.41     4.17       3%
WB/BFS seq                     22.61     4.55       3%
WB/PQ(v) seq center            22.78     3.59       3%
Aldous/Broder                  23.44     4.42       3%
Wilson                         23.70     3.80       3%  baseline
WB/PQ(a) shuffle               26.84     4.21       4%
WB/PQ(a) seq                   27.29     5.18       4%
WB/PQ(a) seq center            71.19     5.87      10%
WB/PQ(a) seq SW                72.86     5.88      10%
```

## 6. Diameter.

The diameter of a maze is the length of a longest path.  (The cells in a (simple) path must be unique.  Repeated cells are permitted in a trail (no repeated passages), or a walk, or a circuit (but only first and last) or a cycle (a walk that starts and ends in the same place).  Terminology does vary, so beware.)

```
algorithm                   diameter        s
WB/BFS seq center              54.00     0.00  constant
WB/BFS seq SW                  73.00     0.00  constant
WB/PQ(a) seq SW               105.19    15.07
WB/PQ(a) seq center           107.66    17.31
Aldous/Broder                 132.87    18.89
Wilson                        137.08    21.34  baseline
WB/PQ(a) seq                  137.60    20.48
WB/BFS shuffle                138.69    19.95
WB/PQ(a) shuffle              138.72    21.08
WB/BFS seq                    140.30    18.43
WB/PQ(e) shuffle              145.66    18.82
WB/PQ(e) seq                  146.27    22.98
WB/PQ(v) seq                  148.15    21.44
WB/PQ(v) shuffle              148.43    21.64
WB/PQ(e) seq SW               153.35    22.20
WB/PQ(v) seq center           154.49    21.94
WB/PQ(e) seq center           155.84    22.85
WB/PQ(v) seq SW               157.38    20.41
WB/DFS shuffle                187.57    30.30
WB/DFS seq                    327.18    60.06
DFS                           381.75    38.10
WB/DFS seq center             707.00     0.00  constant
WB/DFS seq SW                 713.00     0.00  constant
```

# APPENDICES

## Appendix A. Efficiency (time)

Real time was not measured.  What was measured was a count of the inner loops.

From a performance standpoint, passage carving DFS took the least time, a constant at that.  Wilson's algorithm was slower, but not painfully slow.  Even Aldous/Broder wasn't terrible.

The wall building algorithms all did worse.  Shuffling the neighborhoods improved the performance.  Fixing the starting point degraded it, though this was only tested without shuffling.

The constant algorithms were nearly the worst of the lot -- a lot of effort to produce a very simple maze.

The performance results shouldn't be surprising.  A lot of work goes into finding a circuit.  This work is done over and over, essentially starting from scratch each time.

I have two questions, one purely aesthetic, and one more substantial:

1. (aesthetics) Are the mazes produced by any of the algorithms "interesting" in their own right?
2. (performance) Are there ways to avoid starting from scratch with each circuit finder?  For example, instead of starting the finder each time at random or from a fixed point, how would performance be affected by starting the next finder from one end of the edge that was just removed?

```
algorithm                         time       stddev
-------------------------  -----------  -----------

WB/PQ(a) seq SW              742263.86     22728.95            WORST
WB/BFS seq SW                720651.00         0.00  constant
WB/BFS seq center            699784.00         0.00  constant
WB/PQ(a) seq center          662712.14     79421.52
WB/DFS seq                   415171.63     25792.44
WB/DFS seq center            400672.00         0.00  constant
WB/DFS seq SW                384941.00         0.00  constant
WB/PQ(v) seq SW              336150.32     40212.85
WB/PQ(e) seq SW              335532.49     37384.54
                                                      <-- MEAN "TIME"
WB/PQ(v) seq center          200287.15     32832.31
WB/PQ(e) seq center          199549.82     32042.86
WB/PQ(a) seq                  82608.22      8553.01   <-- MEDIAN "TIME"
WB/PQ(a) shuffle              79233.16      7635.61
WB/BFS seq                    49432.39      5554.02
WB/BFS shuffle                49143.24      6097.47
WB/PQ(e) seq                  44141.05      4332.13
WB/PQ(v) seq                  43890.52      3793.43
WB/PQ(e) shuffle              40985.53      2969.06
WB/PQ(v) shuffle              40911.55      3175.82
WB/DFS shuffle                34587.55      2880.49
Aldous/Broder                 17908.44      5435.30
Wilson                         5196.92      2633.03  baseline
DFS                            1427.00         0.00  constant   BEST
-------------------------  -----------  -----------
                     mean    242920.91
```

For comparison, here is a table of some functions evaluated at the numbers of grid edges (e) and cells (v):
```
        linear            e =     1 373         v =     714
        log linear  e ln(e) =     9 920   v ln(v) =   4 692
        3/2 power      e √e =    50 875      v √v =  19 077
        square           e² = 1 885 129        v² = 509 796
```
They might be of some use in forming conjectures.

## Appendix B. Euler analysis.

The mazes in our samples all have *v*=714=21•34 cells.  For a perfect maze, we must have *e*=*v-1*=713 edges.  The sum of the degrees of the cells in any undirected maze is twice the number of passages: 2e=1426.

  (This relationship between the number of passages (or edges) and the sum of the degrees of the cells (or vertices) is a lemma due to Leonhard Euler (1807-1883) and published in 1736 in his analysis of the Königsberg bridges problem posed by Christian Goldbach,)

We can also use Euler's Lemma to work out the number of undirected grid edges in our mazes.  The sum of the degrees is straightforward: (i) there are four corner cells, each with degree 2; (ii) the remaining cells along the perimeter all have degree 3; and (iii) the cells in the interior all have degree 4.
```
     (corners)    4                  degree 2       8
     (perimeter)  2(19+32)=102       degree 3     306
     (interior)   19•32=608          degree 4    2432
                                                 -----
            Sum of degrees                       2746
                                                 -----
            Divide by two:                       1373 passages
```
Thus, a wall builder must remove 660 edges. (1373 - 713)

