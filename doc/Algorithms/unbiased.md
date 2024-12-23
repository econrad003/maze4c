# Unbiased Maze Carving Algorithms

## Contents

1. References
2. Aldous/Broder
3. reverse Aldous/Broder
4. Wilson's algorithm
5. Houston's algorithm

## 1 References

1. Jamis Buck. *Mazes for programmers*. 2015 (Pragmatic Bookshelf). Pages 55-60, 249.
2. Lucia Costantini.  *Algorithms for sampling spanning trees uniformly at random* (master's thesis).  Polytechnic University of Catalonia.  Web. Accessed 20 December 2024.
URL: [https://upcommons.upc.edu/bitstream/handle/2117/328169/memoria.pdf](https://upcommons.upc.edu/bitstream/handle/2117/328169/memoria.pdf)
3. Yiping Hu, Russell Lyons and Pengfei Tang.  *A reverse Aldous/Broder
        algorithm.*  Preprint.  Web: arXiv.org.  24 Jul 2019.
URL:[http://arxiv.org/abs/1907.10196v1](http://arxiv.org/abs/1907.10196v1)
4. Jamis Buck. "Maze Generation: Wilson's algorithm" in *the Buckblog*.  Web. Accessed 21 December 2024.
URL: [http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm.html](http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm.html) 
5. Jamis Buck.  "Maze Algorithms".  Web.  Accessed 21 December 2024.
URL: [https://www.jamisbuck.org/mazes/](https://www.jamisbuck.org/mazes/)


## 2 Aldous/Broder (first entrance random walk)

### 2.1 Technical notes

Aldous/Broder is implemented in module *mazes.Algorithms.aldous\_broder* as class *AldousBroder*.  The algorithm (*in theory*) produces a uniformly random spanning tree.  In practice, the uniformity of the spanning tree depends on the implementation of the underlying random number generator.

> [!NOTE]  
> By "*in theory*", I am using *theory* in a purely mathematical sense and not in the sense used in informal speech.  In informal speech, the word *theory* is used where scientists use the word *hypothesis* and where mathematicians use the word *conjecture*.  In science, *a theory* refers to claims which have been rigorously tested.  In mathematics, the requirements are even more rigorous -- the claims must be mathematically proven.  Here the distinction between *in theory* refers to the algorithm and its dependence on a generator which produces uniformly random outcomes.  The practical issue is that the available random outcome generators are not uniformly random.

At best, an implementation of Aldous/Broder can only produce reasonble approximations of uniform spanning trees.

> [!NOTE]  
> Technically there is no such thing as *a* uniform spanning tree or *a* uniformly random spanning tree,  We use this wording to indicate one of many outcomes produced by the algorithm or by an implementation of the algorithm.  It's like a coin toss with a fair coin.  After the coin comes to a stop revealing a head or a tail, the specific result isn't random.  But it is an outcome of a random process,

### 2.2 Algorithm

```
        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell.

        Loop until every cell has been visited:
            choose a random neighbor of the current cell;
            if this neighbor has not been visited:
                (this is a first entrance!)
                carve a passage from the current cell to the neighbor;
            now the neighbor is the current cell
```

When and if the algorithm terminates, the result is a uniformly random spanning tree.  (But see the technical notes.)  Termination is not guaranteed as a possible but unlikely (as in probilility=0) sequence may prevent every cell from being visited.

### 2.3 Example 1

Lines 1, 2 and 3 create an empty maze.  Lines 4 and 5 carve the maze.  Line 6 displays the result:

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.aldous_broder import AldousBroder
    5> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits      844
                             cells      104
                          passages      103
                     starting cell  (0, 7)
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                   |               |               |
    +---+   +---+   +---+   +   +   +---+---+---+   +   +
    |   |       |   |   |   |   |   |           |   |   |
    +   +   +   +   +   +   +---+---+---+---+   +   +---+
    |   |   |   |   |       |                       |   |
    +   +---+---+   +   +---+---+   +---+---+   +---+   +
    |       |       |       |       |                   |
    +   +---+   +---+   +---+   +---+   +   +---+---+   +
    |       |                   |       |   |       |   |
    +---+   +   +---+---+   +   +---+   +   +   +---+---+
    |           |       |   |   |   |   |               |
    +---+   +---+---+   +---+---+   +   +---+   +---+---+
    |       |           |       |           |           |
    +   +   +   +   +---+---+   +   +---+   +---+---+   +
    |   |       |               |       |   |           |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

A visit is one pass through the loop.  As more cells are visited the probability of moving to an already visited cell increases.  The algorithm (and its implementation) tends to visit more unvisited cells per visit in early visits than in later visits.  On average, it took 844/104=8.12 visits per cell to complete the maze.  (Compare this with an algorithm like simple binary tree which makes one simple decision per cell.)

For simple binary tree, the best, worst, and average case run time is roughly proportional to the number of cells in the maze.

For Aldous/Broder, the best case is still roughly proportional to the number of cells.  The worst case (with probability zero) is that the algorithm never terminates.  The expectation or average case will depend on the grid.  According to Lucia Costantini in her master's thesis (Reference 2, page 29), for most connected grids, the average running time will be roughly proportional to n·log(n) where n is the number of cells in the grid.  For certain very nasty grids, the average running time can go as high as O(n³).  Refer to the bibliography in the thesis for more information.

For this particular example (using the natural logarithm):
```
               844
            ----------- = 1.747
            104 ln(104)
```

Of course one run is meaningless.  Here are samples from a few additional runs in my session:

|         | **run** | **visits** | **quotient** |
| ------: | ------: | ---------: | -----------: |
|         |       1 |        844 |        1.747 |
|         |       2 |       1283 |        2.656 |
|         |       3 |       1402 |        2.903 |
|         |       4 |        987 |        2.043 |
|         |       5 |       2326 |        4.816 |
|         |       6 |       1692 |        3.503 |
|         |       7 |       2331 |        4.826 |
|         |       8 |        623 |        1.290 |
|         |       9 |       1041 |        2.155 |
|         |      10 |       1634 |        3.383 |
|    mean |         |       1416 |        2.932 |
| std dev |         |        586 |        1.213 |

**Table 1**. Sample results for first entrance random walk

The quotient in column 4 is the number of visits divided by 104·ln(104).  The last two rows display the mean and sample standard deviation for the first ten rows.  If we look at the mean and standard deviation in column 4, we expect that roughly 2/3 of the values in the sample should be between:
```
        2.932-1.213=1.719 and 2.932+1.213=4.145.
```
Two of the values fell below and two were above. Six of ten were in the interim.  All of the values were within one sample standard deviation.  This is still a very small sample, so we should be wary of making any inferences.

## 3 Reverse Aldous/Broder (last exit random walk)

Instead of carving a passage at the moment a cell is first entered in the random walk, the reverse Aldous/Broder algorithm waits until the walk is complete.  Instead of a passage marking the first entrance into a cell, passages mark the last exit from a cell.

The additional overhead doesn't gain an advantage in carving, but, for reasonably large mazes, doesn't *significantly* increase the time complexity.
The algorithm is included here primarily for completeness, and with the hope that it might be adapted in some way to gain an advantage over a first-entrance analogue.

The resulting spanning tree is a uniformly random spanning (*i.e.* the algorithm is unbiased).  If we take an arbitrary walk of a graph and reverse it, then the first entrances in the reversed walk are the same as the last exits in the original.  Imagine two black boxes that record completed random walks.  One prints the walk in order of traversal.  The other prints the walk in reverse order.  That ALdous/Broder and reverse Aldous/Broder are unbiased implies that there is no statistical analysis of the output which can distinguish the two boxes.

The algorithm is discussed in Reference 3.


### 3.1 Algorithm

```
        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell;
            initialize an asssociative array "tentative exits".

        Loop until every cell has been visited:
            choose a random neighbor of the current cell;
            if this neighbor has not been visited:
                (this is a first entrance!)
                remove the neighbor from the unvisited set
            set the tentative exit from the current cell to the neighbor;
            now the neighbor is the current cell.

        Loop through all cells in the tentative exit list:
            carve a passage from the cell to its neighbor in the list.
```

### 3.2 Example 2

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.reverse_aldous_broder import ReverseAldousBroder
    5> print(ReverseAldousBroder.on(maze))
          Last Exit Random Walk (Reverse Aldous/Broder) (statistics)
                            visits      812
                             cells      104
                          passages      103
                     starting cell  (5, 9)
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |           |                   |   |
    +   +   +   +   +---+   +---+   +   +   +---+   +   +
    |   |   |   |   |   |           |   |   |   |       |
    +---+   +   +   +   +   +---+---+---+   +   +---+   +
    |   |   |   |       |           |       |   |       |
    +   +---+   +---+---+   +---+---+   +   +   +   +   +
    |       |                   |       |   |       |   |
    +   +---+---+---+   +   +---+---+---+   +---+   +   +
    |               |   |   |               |       |   |
    +   +---+   +---+---+   +---+---+---+---+   +---+   +
    |       |               |                       |   |
    +   +---+---+   +---+   +   +   +   +   +---+---+---+
    |   |               |   |   |   |   |       |       |
    +   +---+   +---+---+---+---+   +   +   +---+---+   +
    |   |           |               |   |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## 4 Wilson's algorithm (circuit-eliminated random walk)

Wilson's algorithm takes a different approach to create an unbiased or uniformly random maze.  Instead of a random walk through the entire grid as in Aldous/Broder, we imagine a city that needs to grow surrounded by wilderness.  An explorer and his assistant are charged with carving a path into the wilderness.  The reluctant explorer is inebriated -- "liquid courage"...  The pair are dropped off somewhere in the wilderness (perhaps by helicopter).  The pair sets off in order to find a way back to the city.  The drunken explorer leads while the sober assistant drops markers.  If a marker is encountered on the way, the pair has walked in a circle.  The assistant removes the redundant markers, and the pair then continues onward.  When the pair reaches the city, the resulting marked path is paved (and probably named in honor of the explorer, as in real life: the assistant's contribution largely forgotten), thus extending the city limits.

### 4.1 Algorihm

```
        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;

        Loop until every cell has been visited:
            choose a random cell in the unvisited area as the current cell;
            the walk := [cell]
                    (the random walk)
            while the current cell has not been visited:
                choose one of its neighborsl
                if the neighbor has not been visited:
                    if the neighbor is in the walk:
                                (circuit elimination)
                        remove all cells added since the neighbor was added;
                    otherwise:
                        add the neighbor to the walk
                now the neighbor is the current cell
            add the walk to the maze
```

### 4.2 Example 3

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.wilson import Wilson
    5> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       42
                             cells      104
                          passages      103
                 paths constructed       42
                     cells visited      519
                          circuits      152
                    markers placed      325
                   markers removed      222
                     starting cell  (3, 10)
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |   |       |       |       |           |
    +---+   +---+   +   +---+   +---+   +   +   +---+---+
    |   |               |           |   |               |
    +   +---+   +   +---+---+   +---+   +---+   +---+---+
    |       |   |   |                       |   |       |
    +   +   +---+   +   +   +   +   +---+   +---+   +   +
    |   |   |           |   |   |   |   |       |   |   |
    +   +---+   +---+---+---+---+   +   +   +---+   +---+
    |   |   |   |           |   |       |   |   |       |
    +   +   +   +   +   +   +   +---+   +---+   +   +   +
    |           |   |   |   |       |   |           |   |
    +---+   +---+   +---+   +   +   +   +---+---+   +---+
    |       |   |   |           |           |           |
    +   +---+   +   +---+---+   +---+---+   +---+---+   +
    |   |                   |       |                   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The number of visits (42) is the number of (explorer-assistant) pairs sent on path-paving missions.  Note that this is also the number of paths constructed.

The number of passages (103) is the difference between the number of markers that were placed (325) and the number that were removed (222).  During the run, 152 circuits were encountered.  (A number of these were just (cell1, cell2, cell1), in which only one marker, the marker at cell2, was removed.)

The time complexity of the algorithm is roughly proportional to the sum of the number of markers placed and the number removed:

```
    325 + 222 = 547.
```

In general, as the algorithm progresses (*i.e.* as the city grows), the paths become shorter and circuits become less common.  So, unlike Aldous/Broder, the algorithm tends to start slowly and end quickly.  It can fail to complete, but, once the unvisited area becomes discrete (*i.e.* when each unvisited cell has no unvisited neighbor), an infinite programming loop becomes impossible.

In Reference 2 (Constantini's masters thesis), the stated average time complexity for Wilson's algorithm is O(ζ) where ζ is the average number of steps in a random walk from one random vertex to another.  (This makes Wilson's algorithm, on average for most sufficiently large grids, faster than Aldous/Broder.)  The worst average case is for a barbell graph where the cells are distributed equally between three regions, two dense subgraphs joined by a long path.  For a barbell graph of this type, the average time complexity goes up to O(n³) where n is the number of cells.

## 5 Houston's algorithm (a hybrid)

If we take advantage of the strengths of Aldous/Broder and Wilson's algorithm we get a hybrid which Jamis Buck calls "Houston's algorithm" after Robin Houston who suggested the approach in 2011 in response to a *Buckblog* post on Wilson's algorithm.  The general idea is to extend the city to a certain size using Aldous/Broder and then complete the city using Wilson's algorithm.  At this point it seems to be unclear whether the result is an unbiased spanning tree.

### 5.2 Examples

#### Example 4A

The switch from Aldous/Broder to Wilson is controlled in this implementation by two options:
```
    cutoff_rate = 2/3
    failure_rate = 0.9
```

The cutoff rate (default 2/3) tells the implementation to swith to Wilson's algorithm when the unvisited area falls to less than 2/3 of the grid.  For our example with 104 cells, 2/3 of 104 is about 69.3.  So if we have fewer than 70 unvisited cells, we switch to Wilson's algorithm.  If this is set to any value greater than or equal to 1, then the first visit triggers the switch.  If this is set to 0 or less, then this switch is never activated.

A failure in Aldous/Broder occurs when we visit an already visited cell. If we have too many failures in a row, then this switch is enabled.  The switch depends on the current size of the unvisited area.  If there are 100 remaining unvisited cells, then to activate the switch, we need 90 *consecutive* failures.  To disable this switch, set the failure rate to *float("inf")*.  A value of 0 or less triggers the switch.  For this example, we used the default values.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.houston import Houston
    5> print(Houston.on(maze))
          Hybrid Random Walk (Houson) (statistics)
                            visits      135
                             cells      104
                          passages      103
                 cuttoff threshold       69
                      failure rate        0.9000
                 paths constructed       37
                     cells visited      150
                          circuits       20
                    markers placed       93
                   markers removed       24
                     starting cell  (1, 3)
                           trigger  cutoff threshold
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                           |   |       |           |
    +---+---+---+   +   +---+---+   +   +---+   +---+---+
    |       |       |               |       |           |
    +   +---+---+---+---+   +---+   +---+   +   +---+---+
    |       |       |       |       |   |           |   |
    +---+   +---+   +   +   +   +   +   +---+---+   +   +
    |   |   |       |   |   |   |   |   |   |       |   |
    +   +   +---+   +   +   +---+---+   +   +---+   +   +
    |   |           |   |   |   |   |                   |
    +   +   +   +---+   +---+   +   +---+---+---+---+   +
    |       |       |                                   |
    +   +   +   +   +---+   +---+   +---+---+---+---+   +
    |   |   |   |               |   |       |       |   |
    +   +---+   +---+---+   +   +---+---+   +   +---+   +
    |   |           |       |                   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

In this example, the statistics tell us that the switch was triggered by the cutoff. The first entrance random walk (Aldous/Broder) was used until there were 69 remaining unvisited cells.  (At that point, 34 passages had been carved.) The remaining 69 passages were carved using circuit-eliminated random walks (Wilson's method).

The number of visits (135) is complicated by the fact that a visit in Aldous/Broder carves *at most* one passage while a visit in Wilson carves exactly one path.  Subtract paths constructed from visits:
```
        135 - 37 = 98
```

Aldous/Broder accounted for 34 passages in 98 visits, where one visit involves a single step from one cell to another cell.  34 visits were productive steps into unvisited cells, while 64 were unproductive.
```
        64/34 = 1.88
```

#### Example 4B

To force the algorithm to use the failure rate switch, I set the failure rate to 10% in this example.  (See line 8.  The session continues from the example above.)

```
    7> maze = Maze(OblongGrid(8, 13))
    8> print(Houston.on(maze, failure_rate=0.1))
          Hybrid Random Walk (Houson) (statistics)
                            visits       92
                             cells      104
                          passages      103
                 cuttoff threshold       69
                      failure rate        0.1000
                 paths constructed       40
                     cells visited      193
                          circuits       31
                    markers placed      122
                   markers removed       39
                     starting cell  (3, 5)
                           trigger  failure threshold
    9> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |   |   |   |   |                       |
    +---+---+   +   +   +   +   +---+   +---+---+---+---+
    |                       |                           |
    +   +---+---+---+   +---+   +---+---+---+---+   +---+
    |   |           |           |   |                   |
    +   +   +---+---+---+---+---+   +---+   +---+---+   +
    |           |       |       |           |   |       |
    +   +   +---+---+   +---+   +   +   +---+   +---+---+
    |   |       |           |   |   |   |               |
    +   +---+   +   +   +   +   +---+   +---+   +---+---+
    |       |       |   |   |       |       |           |
    +   +---+   +   +   +   +   +---+---+---+   +---+---+
    |   |       |   |   |                               |
    +---+---+---+   +---+   +---+   +   +   +---+---+   +
    |                   |       |   |   |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

We can determine when the switch was triggered by subtracting markers removed from markers placed:
```
        122 - 39 = 83
```
So 20 passages were carved using Aldous/Broder and the remaining 83 were carved using Wilson's.  There were 83 unvisited cells at the time of the switch.

As before, subtract paths constructed (40) from the number of visits (92):
```
        92 - 40 = 52
```
20 of the 52 visits in Aldous/Broder were steps into unvisited cells.  The remaining 32 steps were unproductive.
```
        32/20 = 1.6
```