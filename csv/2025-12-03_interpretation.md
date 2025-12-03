# Interpretation of spanning binary tree results from 2025-12-03

## Table of contents

* Introduction

* 1. Isolated cells
* 2. Dead ends
* 3. Degree-2 cells
* 3a. Horizontal or E/W passages
* 3b. Vertical or N/S passages
* 3c. 90° turns
* 4. Degree-3 cells
* 5. Degree-4 cells
* 6. Diameter

* Appendix A. Efficiency (time)
* Appendix B. Euler analysis

## Introduction

The data discussed here were from maze carving runs of a number of algorithms.  With four baseline exceptions, the algorithms are all designed to create spanning binary trees.  Each algorithm was run 100 times to carve 40×40 rectangular mazes on Von Neumann rectangular grids.

The baseline algorithms were DFS, BFS, Aldous/Broder and Wilson.  Mazes produced by DFS are "almost" binary, with a tendency to produce very few degree 4 nodes.

The spanning binary tree algorithms were the simple binary tree algorithm, the greedy binary growing tree algorithm, and the fair binary growing tree algorithm, denoted SBT, GBT, and FBT, respectively.  Their implementations are:

* **SBT** - module *mazes.Algorithms.simple\_binary\_tree*, class *BinaryTree*
* **GBT** - module *mazes.Algorithms.binary\_growing\_tree1*, class *BinaryGrowingTree*
* **FBT** - module *mazes.Algorithms.binary\_growing\_tree2*, class *BinaryGrowingTree*

SBT was run with biases of 25%, 50% (fair coin), and 75%.

The two binary growing tree algorithms were run in various configurations using stacks (DFS), queues (BFS), split stacks (SS), split queues (SQ), random queues (RQ), and cached priority queues (PQ).

The binary growing tree algorithms can, in some instances, produce spanning forests which contain isolated vertices.  A preliminary test run did not produce any such forests.  The run here produced exactly one such configuration.  For more information, see the sections on isolated cells and diameters.

```
    1 runs terminated without a spanning tree.
    For these runs, the diameter was taken to be the number of cells.
    These runs will have at least one isolated vertex.
```

## 1. Isolated cells

An isolated cell (or isolate or island) is a cell with no incident passages, or equivalently, a degree-0 cell.  A connected maze with more than 1 cell will never have any isolated cells.

The binary growing tree algorithms can fail in this way.  But failures, though very rare, are not unexpected.

```
algorithm                   isolates    stdev      pct
-------------------------  ---------  -------  -------
GBT/SQ TL=1                     0.01     0.10       0%
```

GBT (the greedy binary growing tree algorithm) using a split queue (SQ) with target length 1 produce one spanning forest with a single isolated cell.  In all other cases, a spanning tree was produced.

A preliminary test run of the script produced no disconnected forests, and, to date, the author has produced no examples (using a standard Von Neumann rectangular grid) in the wild.  These failures are presumed to be very rare in practice.

A simple connected grid in which such a disconnected forest is guaranteed is a five-cell grid known as the 4-star:
```
                +---+
                |   |
            +---+---+---+       Figure 1.  The 4-star
            |   |   |   |           A five-cell grid with no binary spanning
            +---+---+---+           trees.
                |   |
                +---+
```
The 4-star is the smallest example of a grid with no binary spanning trees.

## 2. Dead ends.

A dead end is a cell with exactly one incident passages, or equivalently, a degree-1 cell.  Dead ends tend to be a matter of individual taste.  Some algorithms (like DFS or hunt-and-kill) produce very few.   Some (like Vertex Prim) tend to produce relatively many.   Here are the results for the sampled algorithms.

```
algorithm                  dead ends    stdev      pct
-------------------------  ---------  -------  -------
FBT/DFS rand=N SW               2.00     0.00       0%
FBT/DFS rand=N                  2.84     0.37       0%
FBT/DFS rand=N W                3.00     0.00       0%
FBT/DFS rand=N C                3.00     0.00       0%
GBT/BFS rand=N SW              41.00     0.00       3%
FBT/BFS rand=N SW              41.00     0.00       3%
FBT/BFS rand=N                 76.74    15.91       5%
GBT/BFS rand=N                 78.31    14.70       5%
GBT/BFS rand=N C               80.00     0.00       5%
FBT/BFS rand=N C               80.00     0.00       5%
GBT/BFS rand=N W               82.00     0.00       5%
FBT/BFS rand=N W               82.00     0.00       5%
GBT/BFS                       107.40    17.73       7%
FBT/SQ TL=10                  108.69    19.81       7%
GBT/SQ TL=1                   109.05    22.45       7%
FBT/BFS                       109.52    20.86       7%
FBT/SQ TL=1                   109.81    21.93       7%
GBT/SQ TL=10                  120.36    19.22       8%
DFS                           170.50     7.29      11%  control
BFS                           171.20     6.99      11%  control
FBT/DFS                       171.99     7.07      11%
SBT E/N p=0.75                325.14    12.07      20%
SBT E/N p=0.25                325.67    11.44      20%
SBT E/N p=0.5                 419.82    10.12      26%
Aldous/Broder                 489.50    10.41      31%  baseline
Wilson                        490.88    12.72      31%  baseline
FBT/RQ                        520.36     9.10      33%
GBT/SS TL=10                  639.76    25.72      40%
FBT/SS TL=10                  645.79    24.81      40%
FBT/PQ cache                  656.03     7.68      41%
GBT/PQ cache                  673.37     6.65      42%
GBT/SS TL=1                   690.05     7.78      43%
GBT/DFS                       701.59     5.38      44%
FBT/SS TL=1                   702.58     6.48      44%
GBT/DFS rand=N C              730.00     0.00      46%
GBT/DFS rand=N                762.39    35.38      48%
GBT/DFS rand=N W              783.00     0.00      49%
GBT/DFS rand=N SW             801.00     0.00      50%
```
The extreme examples are all cases where the cell neighborhoods were traversed in dictionary order (*rand=N*).

## 3. Degree-2 cells.

A degree-2 cell is incident to two passages -- it is linked by passages to two of its neighbors.  Degree-2 cells, in one sense, reflect an absence of choice: if we enter via one of the passages, then we must typically exit via the other.

```
algorithm                   degree 2    stdev      pct
-------------------------  ---------  -------  -------
GBT/DFS rand=N SW              81.00     0.00       5%
GBT/DFS rand=N W              117.00     0.00       7%
GBT/DFS rand=N                158.22    70.75      10%
GBT/DFS rand=N C              223.00     0.00      14%
FBT/SS TL=1                   277.84    12.96      17%
GBT/DFS                       279.82    10.75      17%
GBT/SS TL=1                   302.90    15.56      19%
GBT/PQ cache                  336.26    13.30      21%
FBT/PQ cache                  370.94    15.36      23%
FBT/SS TL=10                  391.42    49.62      24%
GBT/SS TL=10                  403.48    51.43      25%
FBT/RQ                        642.28    18.21      40%
Wilson                        758.65    22.14      47%  baseline
Aldous/Broder                 760.74    18.11      48%  baseline
SBT E/N p=0.5                 843.36    20.23      53%
SBT E/N p=0.25               1031.66    22.87      64%
SBT E/N p=0.75               1032.72    24.14      65%
FBT/DFS                      1339.02    14.14      84%
BFS                          1343.24    14.08      84%  control
DFS                          1344.59    14.29      84%  control
GBT/SQ TL=10                 1442.28    38.44      90%
FBT/SQ TL=1                  1463.38    43.86      91%
FBT/BFS                      1463.96    41.72      91%
GBT/SQ TL=1                  1464.89    44.92      92%
FBT/SQ TL=10                 1465.62    39.63      92%
GBT/BFS                      1468.20    35.47      92%
GBT/BFS rand=N W             1519.00     0.00      95%
FBT/BFS rand=N W             1519.00     0.00      95%
GBT/BFS rand=N C             1523.00     0.00      95%
FBT/BFS rand=N C             1523.00     0.00      95%
GBT/BFS rand=N               1526.38    29.40      95%
FBT/BFS rand=N               1529.52    31.83      96%
GBT/BFS rand=N SW            1601.00     0.00     100%
FBT/BFS rand=N SW            1601.00     0.00     100%
FBT/DFS rand=N W             1677.00     0.00     105%
FBT/DFS rand=N C             1677.00     0.00     105%
FBT/DFS rand=N               1677.32     0.73     105%
FBT/DFS rand=N SW            1679.00     0.00     105%
```
The extreme examples are all cases where the cell neighborhoods were traversed in dictionary order (*rand=N*).

With four directions, there are C(4,2)=6 ways of choosing two directions.  One possibility is east and west.  A second possibility is north and south.  There are four other combinations.  A degree-2 cell with passages east and west might be described as horizontal, while one with north and south passages might be called vertical.  The four remaining combinations are right-angled turns.

### 3a. Horizontal or E/W passages

```
algorithm                        E/W    stdev      pct
-------------------------  ---------  -------  -------
GBT/BFS rand=N SW               0.00     0.00       0%
GBT/BFS rand=N W                0.00     0.00       0%
FBT/BFS rand=N SW               0.00     0.00       0%
FBT/BFS rand=N W                0.00     0.00       0%
GBT/DFS rand=N SW              20.00     0.00       1%
GBT/DFS rand=N W               21.00     0.00       1%
GBT/DFS rand=N                 22.48     3.75       1%
GBT/DFS rand=N C               25.00     0.00       2%
SBT E/N p=0.75                 36.69     6.83       2%
FBT/SS TL=1                    53.58     6.19       3%
GBT/DFS                        54.86     5.80       3%
GBT/SS TL=1                    71.85    10.28       4%
GBT/PQ cache                   73.52     8.83       5%
FBT/PQ cache                   74.87     7.67       5%
FBT/SS TL=10                  117.70    37.03       7%
GBT/SS TL=10                  128.28    41.62       8%
Aldous/Broder                 147.08    13.54       9%  baseline
Wilson                        147.46    13.40       9%  baseline
FBT/RQ                        157.65    20.07      10%
SBT E/N p=0.5                 218.62    17.51      14%
DFS                           261.05    21.82      16%  control
BFS                           261.05    20.09      16%  control
FBT/DFS                       262.29    20.26      16%
FBT/BFS rand=N                290.20   327.77      18%
GBT/BFS rand=N C              361.00     0.00      23%
FBT/BFS rand=N C              361.00     0.00      23%
GBT/BFS rand=N                417.84   372.40      26%
SBT E/N p=0.25                692.74    33.14      43%
GBT/BFS                       717.48   187.16      45%
GBT/SQ TL=10                  718.21   215.20      45%
FBT/SQ TL=10                  718.74   205.60      45%
FBT/SQ TL=1                   729.99   194.84      46%
GBT/SQ TL=1                   731.90   205.37      46%
FBT/BFS                       743.58   207.15      46%
FBT/DFS rand=N SW            1560.00     0.00      98%
FBT/DFS rand=N               1565.66    17.77      98%
FBT/DFS rand=N C             1577.00     0.00      99%
FBT/DFS rand=N W             1580.00     0.00      99%
```

### 3b. Vertical or N/S passages

With *m*=40 rows and *n*=40 columns, there are*v*=1600 cells.  Among these cells, *m*(*n*-2)=1520 cells have neighbors both east and west, and (*m*-2)*n*=1520 have neighbors both north and south.  An unbiased algorithm should have, on average, a ratio of about 1.000 horizontal to vertical.

```
algorithm                         NS    stdev      pct      H/V
-------------------------  ---------  -------  -------  -------
FBT/DFS rand=N W               19.00     0.00       1%    83.16
FBT/DFS rand=N C               19.00     0.00       1%    83.00
FBT/DFS rand=N                 19.31    10.38       1%    81.08
GBT/DFS rand=N                 28.53     9.18       2%     0.79
GBT/DFS rand=N C               33.00     0.00       2%     0.76
SBT E/N p=0.25                 36.82     6.51       2%    18.81
GBT/DFS rand=N SW              39.00     0.00       2%     0.51
GBT/DFS rand=N W               39.00     0.00       2%     0.54
FBT/DFS rand=N SW              39.00     0.00       2%    40.00
FBT/SS TL=1                    52.33     6.72       3%     1.02
GBT/DFS                        53.82     6.15       3%     1.02
GBT/SS TL=1                    68.45     9.28       4%     1.05
GBT/PQ cache                   74.32     8.69       5%     0.99
FBT/PQ cache                   75.53     8.77       5%     0.99
FBT/SS TL=10                  115.77    39.53       7%     1.02
GBT/SS TL=10                  116.84    33.81       7%     1.10
Wilson                        145.73    13.67       9%     1.01  baseline
Aldous/Broder                 147.17    11.94       9%     1.00  baseline
FBT/RQ                        161.90    21.87      10%     0.97
SBT E/N p=0.5                 220.46    18.06      14%     0.99
FBT/DFS                       259.30    18.15      16%     1.01
BFS                           262.27    19.94      16%     1.00  control
DFS                           263.51    18.30      16%     0.99  control
SBT E/N p=0.75                691.74    34.02      43%     0.05
FBT/BFS                       711.08   199.51      44%     1.05
GBT/SQ TL=10                  713.79   212.69      45%     1.01
GBT/SQ TL=1                   723.56   207.15      45%     1.01
FBT/SQ TL=1                   723.81   199.56      45%     1.01
FBT/SQ TL=10                  732.88   208.12      46%     0.98
GBT/BFS                       741.35   190.48      46%     0.97
GBT/BFS rand=N               1103.74   374.56      69%     0.38
GBT/BFS rand=N C             1157.00     0.00      72%     0.31
FBT/BFS rand=N C             1157.00     0.00      72%     0.31
FBT/BFS rand=N               1234.59   333.27      77%     0.24
GBT/BFS rand=N W             1517.00     0.00      95%     0.00
FBT/BFS rand=N W             1517.00     0.00      95%     0.00
GBT/BFS rand=N SW            1599.00     0.00     100%     0.00
FBT/BFS rand=N SW            1599.00     0.00     100%     0.00
```

### 3c. 90° turns

```
algorithm                       turn    stdev      pct
-------------------------  ---------  -------  -------
GBT/BFS rand=N SW               2.00     0.00       0%
GBT/BFS rand=N W                2.00     0.00       0%
FBT/BFS rand=N SW               2.00     0.00       0%
FBT/BFS rand=N W                2.00     0.00       0%
FBT/BFS rand=N                  4.73     0.70       0%
GBT/BFS rand=N                  4.80     0.57       0%
GBT/BFS rand=N C                5.00     0.00       0%
FBT/BFS rand=N C                5.00     0.00       0%
FBT/BFS                         9.30     2.96       1%
GBT/BFS                         9.37     2.80       1%
GBT/SQ TL=1                     9.43     2.92       1%
FBT/SQ TL=1                     9.58     2.95       1%
GBT/SQ TL=10                   10.28     3.12       1%
FBT/SQ TL=10                   14.00     3.29       1%
GBT/DFS rand=N SW              22.00     0.00       1%
GBT/DFS rand=N W               57.00     0.00       4%
FBT/DFS rand=N W               78.00     0.00       5%
FBT/DFS rand=N SW              80.00     0.00       5%
FBT/DFS rand=N C               81.00     0.00       5%
FBT/DFS rand=N                 92.35    17.52       6%
GBT/DFS rand=N                107.21    76.89       7%
FBT/SS TL=10                  157.95    10.64      10%
GBT/SS TL=10                  158.36    11.70      10%
GBT/SS TL=1                   162.60    10.30      10%
GBT/DFS rand=N C              165.00     0.00      10%
GBT/DFS                       171.14    10.61      11%
FBT/SS TL=1                   171.93    10.18      11%
GBT/PQ cache                  188.42    10.95      12%
FBT/PQ cache                  220.54    14.14      14%
SBT E/N p=0.25                302.10    16.20      19%
SBT E/N p=0.75                304.29    15.93      19%
FBT/RQ                        322.73    14.65      20%
SBT E/N p=0.5                 404.28    17.55      25%
Wilson                        465.46    19.17      29%  baseline
Aldous/Broder                 466.49    17.03      29%  baseline
FBT/DFS                       817.43    19.64      51%
BFS                           819.92    20.33      51%  control
DFS                           820.03    19.97      51%  control
```

## 4. Degree-3 cells.

A degree-3 cell is incident to three passages -- it islinked by passages to three of its neighbors.  Given an entrance, a degree-3 cell represents a choice of two separate exits.

```
algorithm                   degree 3        s      pct
FBT/DFS rand=N SW               0.00     0.00       0%
FBT/DFS rand=N                  0.84     0.37       0%
FBT/DFS rand=N W                1.00     0.00       0%
FBT/DFS rand=N C                1.00     0.00       0%
GBT/BFS rand=N SW              39.00     0.00       2%
FBT/BFS rand=N SW              39.00     0.00       2%
FBT/BFS rand=N                 74.74    15.91       5%
GBT/BFS rand=N                 76.31    14.70       5%
GBT/BFS rand=N C               78.00     0.00       5%
FBT/BFS rand=N C               78.00     0.00       5%
GBT/BFS rand=N W               80.00     0.00       5%
FBT/BFS rand=N W               80.00     0.00       5%
GBT/BFS                       105.40    17.73       7%
FBT/SQ TL=10                  106.69    19.81       7%
GBT/SQ TL=1                   107.05    22.45       7%
FBT/BFS                       107.52    20.86       7%
FBT/SQ TL=1                   107.81    21.93       7%
GBT/SQ TL=10                  118.36    19.22       7%
DFS                           163.32     7.22      10%  control
BFS                           163.92     7.66      10%  control
FBT/DFS                       169.99     7.07      11%
SBT E/N p=0.75                323.14    12.07      20%
SBT E/N p=0.25                323.67    11.44      20%
Aldous/Broder                 374.02    10.94      23%  baseline
Wilson                        374.06    11.75      23%  baseline
SBT E/N p=0.5                 417.82    10.12      26%
FBT/RQ                        518.36     9.10      32%
GBT/SS TL=10                  637.76    25.72      40%
FBT/SS TL=10                  643.79    24.81      40%
FBT/PQ cache                  654.03     7.68      41%
GBT/PQ cache                  671.37     6.65      42%
GBT/SS TL=1                   688.05     7.78      43%
GBT/DFS                       699.59     5.38      44%
FBT/SS TL=1                   700.58     6.48      44%
GBT/DFS rand=N C              728.00     0.00      46%
GBT/DFS rand=N                760.39    35.38      48%
GBT/DFS rand=N W              781.00     0.00      49%
GBT/DFS rand=N SW             799.00     0.00      50%
```
The extreme examples are all cases where the cell neighborhoods were traversed in dictionary order (*rand=N*).

## 5. Degree-4 cells.

A degree-4 cell is incident to four passages -- it islinked by a passage to each of its four neighbors.  Given an entrance, a degree-4 cell represents a choice of three separate exits.

Cells in binary trees have at most degree 3 (one parent, two children).

```
algorithm                   degree 4        s     pct
Wilson                         57.41     6.67       4%  baseline
Aldous/Broder                  56.74     6.24       4%  baseline
BFS                             2.64     1.51       0%  control
DFS                             2.59     1.58       0%  control
FBT/PQ cache                    0.00     0.00       0%
FBT/RQ                          0.00     0.00       0%
FBT/SQ TL=10                    0.00     0.00       0%
FBT/SQ TL=1                     0.00     0.00       0%
FBT/SS TL=10                    0.00     0.00       0%
FBT/SS TL=1                     0.00     0.00       0%
FBT/BFS rand=N C                0.00     0.00       0%
FBT/BFS rand=N W                0.00     0.00       0%
FBT/BFS rand=N SW               0.00     0.00       0%
FBT/BFS rand=N                  0.00     0.00       0%
FBT/BFS                         0.00     0.00       0%
FBT/DFS rand=N C                0.00     0.00       0%
FBT/DFS rand=N W                0.00     0.00       0%
FBT/DFS rand=N SW               0.00     0.00       0%
FBT/DFS rand=N                  0.00     0.00       0%
FBT/DFS                         0.00     0.00       0%
GBT/PQ cache                    0.00     0.00       0%
GBT/SQ TL=10                    0.00     0.00       0%
GBT/SQ TL=1                     0.00     0.00       0%
GBT/SS TL=10                    0.00     0.00       0%
GBT/SS TL=1                     0.00     0.00       0%
GBT/BFS rand=N C                0.00     0.00       0%
GBT/BFS rand=N W                0.00     0.00       0%
GBT/BFS rand=N SW               0.00     0.00       0%
GBT/BFS rand=N                  0.00     0.00       0%
GBT/BFS                         0.00     0.00       0%
GBT/DFS rand=N C                0.00     0.00       0%
GBT/DFS rand=N W                0.00     0.00       0%
GBT/DFS rand=N SW               0.00     0.00       0%
GBT/DFS rand=N                  0.00     0.00       0%
GBT/DFS                         0.00     0.00       0%
SBT E/N p=0.75                  0.00     0.00       0%
SBT E/N p=0.5                   0.00     0.00       0%
SBT E/N p=0.25                  0.00     0.00       0%
```
Except for the baseline and control algorithms, no algorithms produced cells of degree 4.  (As required!)

## 6. Diameter.

The diameter of a maze is the length of a longest path.  (The cells in a (simple) path must be unique.  Repeated cells are permitted in a trail (no repeated passages), or a walk, or a circuit (but only first and last) or a cycle (a walk that starts and ends in the same place).  Terminology does vary, so beware.)

To avoid infinite distances, when isolated vertices are present, the number of cells is used in lieu of the diameter.  Results in this instance may be skewed.

```
algorithm                   diameter        s
GBT/BFS rand=N C               84.00     0.00
FBT/BFS rand=N C               84.00     0.00
FBT/SQ TL=1                   104.88    10.18
FBT/BFS                       105.29    10.03
GBT/SQ TL=10                  106.47     9.32
GBT/BFS                       106.70     8.86
FBT/SQ TL=10                  106.92     9.10
GBT/BFS rand=N                111.21    12.24
FBT/BFS rand=N                112.79    12.57
GBT/BFS rand=N SW             120.00     0.00
GBT/BFS rand=N W              120.00     0.00
FBT/BFS rand=N SW             120.00     0.00
FBT/BFS rand=N W              120.00     0.00
FBT/RQ                        120.64    15.74
GBT/SQ TL=1                   121.01   157.14  *
SBT E/N p=0.75                135.37     3.64
SBT E/N p=0.25                135.75     3.35
SBT E/N p=0.5                 154.07     3.82
GBT/SS TL=10                  180.26    12.71
GBT/PQ cache                  182.88    26.83
FBT/SS TL=10                  190.41    15.09
FBT/PQ cache                  194.26    29.76
Aldous/Broder                 233.91    31.07
Wilson                        234.82    34.77  baseline
GBT/SS TL=1                   352.95    41.38  baseline
FBT/SS TL=1                   511.67    58.85
GBT/DFS                       522.37    63.70
BFS                           788.05    86.53  control
DFS                           795.94    86.47  control
FBT/DFS                       797.39    82.21
GBT/DFS rand=N                855.33    39.43
GBT/DFS rand=N C              867.00     0.00
GBT/DFS rand=N SW             881.00     0.00
GBT/DFS rand=N W              899.00     0.00
FBT/DFS rand=N W             1640.00     0.00
FBT/DFS rand=N C             1660.00     0.00
FBT/DFS rand=N               1666.24    12.59
FBT/DFS rand=N SW            1680.00     0.00
```
Notes:
* GBT/SQ TL=1 produced a single isolated vertex in its sample of 100 runs.

# APPENDICES

## Appendix A. Efficiency (time)

With the exceptions of Aldous/Broder and Wilson's algorithms, the time complexity of the algorithms is asymptotically linear in the number of grid edges.  For rectangular Von Neumann grids, with at least five rows and five columns the number of grid edges is between 3 and 4 times the number of cells.  The asymptotic time complexity is roughly proportional to the number of cells.

## Appendix B. Euler analysis.

The mazes in our samples all have *v*=1600=40•40 cells.  For a perfect maze, we must have *e*=*v-1*=1599 edges.  The sum of the degrees of the cells in any undirected maze is twice the number of passages: 2e=3198.

  (This relationship between the number of passages (or edges) and the sum of the degrees of the cells (or vertices) is a lemma due to Leonhard Euler (1807-1883) and published in 1736 in his analysis of the Königsberg bridges problem posed by Christian Goldbach,)

