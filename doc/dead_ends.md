# Dead end tools

## Contents

1. The basics
2. The dead end toolbox
3. Hiding dead ends
4. Exposing circuits (and *bridges*)
5. Sampling
6. Removing dead ends by linking
7. Removing dead ends in pairs
8. Removing in pairs, then linking

## 1. The basics

You can skip these if you already know what's meant by the *degree* of a cell and what's meant by a *dead end* cell.  But at least glance at *Euler's Lemma* before moving on.

Consider the following 2×2 binary spanning tree maze:
```
     +---+---+
     | 4   3 |
     +---+   +
     | 1   2 |
     +---+---+
```
Cells 1 and 4 are each incident to one passage, respectively the passage between cells 1 and 2, and the passage between 3 and 4.  Cells 2 and 3 are each incident to two passages, the first: respectively, the passages mentioned above, and the second: the passage between 2 and 3.

### 1.1. The degree of a cell

If a maze doesn't have any directed passages, then, with one important exception, the *degree* of a cell is the number of passages incident to that cell.

If the maze has directed passages, then we distinguish the *in-degree* and the *out-degree*:  The *in-degree* is the number of inbound passages and the *out-degree* is the number of outbound passages.  Undirected (or bidirectional) passages are counted as both inbound and outbound.

There is a special type of passage which complicates this picture.  A *loop* is a passage between a cell and itself.  Technically speaking, a loop is, by nature, undirected.  A loop is both inbound and outbound, so there are legitimate questions as to how to count loops in the degree.  The usual convention is to count each of a cell's loops twice in the degree.  If we follow that convention in counting, then we have *Euler's Lemma*:

* **Euler's Lemma**: In an undirected maze (or graph), the sum of the degrees of the cells (or vertices) is twice the number of passages (or edges).

We generally don't admit loops in mazes, so counting passages presents no problems.  Of course Euler's Lemma doesn't apply to mazes with directed passages (or to digraphs, or to networks).

The maze above has 3 passages.  The degree of cell 1, 2, 3, or 4 is, respectively, 1, 2, 2, or 1.  So the sum of the degrees is 6, or twice the number of passages.

<ul>
<li><b>Problem 1</b>:
In a typical m×n rectangular grid (with north, south, east and west neighbors), how many grid edges are there?</li>
<li><b>Solution</b>:
<blockquote>
First consider two trivial cases: (a) if m=1, then there are n-1 edges; and (b) if n=1, then there are m-1 edges.
<p>Suppose that both m and n are both greater than 1.  Then we have:
<ol type="a">
<li>four corner cells, each of degree 2;</li>
<li>2(m-2) + 2(n-2) premaining erimeter cells, each of degree 3; and</li>
<li>(m-2)(n-2) interior cells, each of degree 4.</li>
</ol>
Multiplying:
<blockquote>
4•2 = 8<br>
(2(m-2) + 2(n-2))•3 = 6*m + 6*n - 24<br>
(m-2)(n-2)•4 = 4mn - 8m - 8n +16
</blockquote>
Add these up to get the sum of the degrees:
<blockquote>
4mn - 2m - 2n
</blockquote>
Divide by two to get the number of edges in the grid:
<blockquote>
2mn - m - n
</blockquote></li>
<li><b>Sanity Check</b>: A 2×2 rectangular grid has two north-south edges and two east-west edges for a total of 4.  Putting m=n=2 into the result, we have:
<blockquote>
2•2•2 - 2 - 2 = 4 (as expected).
</blockquote></li>
</ul>

### 1.2. Dead ends

A dead end cell is a cell with exactly one incident passage, and that passage must be undirected.  So for a dead end cell, the degree, the in-degree, and the out-degree are all 1.  For a dead end cell, the way in is the same as the way out.

Our 2×2 example has exactly two dead ends, namely, cells 1 and 4:
```
     +---+---+
     | 4   3 |
     +---+   +
     | 1   2 |
     +---+---+
```

## 2. The dead end toolbox

The dead end toolbox provides tools for locating and managing dead ends. Let's create a maze and locate the dead ends.  First we need a maze:
```
$ python
Python 3.10.12
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(OblongGrid(5, 8))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       16
                             cells       40
                          passages       39
                 paths constructed       16
                     cells visited       97
                          circuits       20
                    markers placed       61
                   markers removed       22
                     starting cell  (3, 4)
>>> print(maze)
+---+---+---+---+---+---+---+---+
|   |               |           |
+   +   +   +---+   +   +---+   +
|       |   |   |           |   |
+---+   +---+   +---+   +---+   +
|   |               |   |   |   |
+   +---+---+---+   +---+   +   +
|   |       |   |   |       |   |
+   +   +---+   +   +   +---+   +
|                       |       |
+---+---+---+---+---+---+---+---+
```
Next we will use the dead end toolbox:
```
>>> from mazes.tools.dead_ends import DeadEnds
>>> dead = DeadEnds(maze)
```

How many dead ends?
```
>>> len(dead)
10
```

And where are they?
```
>>> for cell in dead:
...     cell.label = "D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+
| D |               |           |
+   +   +   +---+   +   +---+   +
|       | D | D |         D |   |
+---+   +---+   +---+   +---+   +
| D |               | D | D |   |
+   +---+---+---+   +---+   +   +
|   |     D | D |   |       |   |
+   +   +---+   +   +   +---+   +
|                       | D     |
+---+---+---+---+---+---+---+---+
```

The dead ends are marked with the label "D".  (And, yes, there are ten of them.)  For each of these cells, there is exactly one passage into the cell, and the one and only exit is the same passage.

## 3 Hiding dead ends

If we don't like dead ends, then one solution is to hide them.
```
...     cell.hide()
...
>>> print(maze)
+---+---+---+---+---+---+---+---+
|█D█|               |           |
+   +   +   +---+   +   +---+   +
|       |█D█|█D█|        █D█|   |
+---+   +---+   +---+   +---+   +
|█D█|               |█D█|█D█|   |
+   +---+---+---+   +---+   +   +
|   |    █D█|█D█|   |       |   |
+   +   +---+   +   +   +---+   +
|                       |█D█    |
+---+---+---+---+---+---+---+---+
```
The block character "█" marks the hidden cells.  Hiding a cell does not disrupt the actual passages, so they are still displayed in this representation of the maze.  But using the usual interfaces to look for passages does hide the hidden cells.  For example, consider the cell just south of the northwest corner cell:
```
>>> cell = maze.grid[3, 0]
```
The cell to the north (*i.e.* the northwest corner) and the cell to the south (middle row, first cell) are both hidden.  The neighbor to the east (row 3, column 1) is not hidden.
```
>>> for nbr in cell.neighbors:
...     print(nbr.index)
...
(3, 1)
>>> len(list(cell.neighbors))
1
```
Although the two hidden cells were hidden from the *Cell.neighbors()* generator, they are still there -- and the passage north still exists:
```
>>> cell.north.index, cell.south.index
((4, 0), (2, 0))
>>> cell.is_linked(cell.north), cell.is_linked(cell.south)
(True, False)
```
And all the neighbors, even the hidden ones, can be accessed through a special generator (*Cell._neighbors):
```
>>> list(nbr.index for nbr in cell._neighbors)
[(3, 1), (4, 0), (2, 0)]
```

Continuing with the example, that the cell above has just one unmasked neighbor.  Let's look at dead ends in the unmasked portion of the maze -- there are five of them:
```
>>> less_dead = DeadEnds(maze)
>>> len(less_dead)
5
```

Let's label them:
```
>>> for cell in less_dead:
...     cell.label = "L"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+
|█D█|               |           |
+   +   +   +---+   +   +---+   +
| L     |█D█|█D█|        █D█|   |
+---+   +---+   +---+   +---+   +
|█D█|               |█D█|█D█|   |
+   +---+---+---+   +---+   +   +
| L | L  █D█|█D█|   |     L |   |
+   +   +---+   +   +   +---+   +
|                       |█D█  L |
+---+---+---+---+---+---+---+---+
```

If we start with any perfect maze and mask the dead ends, the unmasked part of the maze is still a perfect maze.  And if we repeat the process, we will eventually be left with a perfect maze consisting of a single cell:
```
>>> while True:
...    more_deaths = DeadEnds(maze)
...    if len(more_deaths) < 1: break
...    for cell in more_deaths: cell.hide()
... 
>>> print(maze)
+---+---+---+---+---+---+---+---+
|█D█|    ███ ███ ███|███ ███ ███|
+   +   +   +---+   +   +---+   +
|█L█ ███|█D█|█D█|███ ███ █D█|███|
+---+   +---+   +---+   +---+   +
|█D█|███ ███ ███ ███|█D█|█D█|███|
+   +---+---+---+   +---+   +   +
|█L█|█L█ █D█|█D█|███|███ █L█|███|
+   +   +---+   +   +   +---+   +
|███ ███ ███ ███ ███ ███|█D█ █L█|
+---+---+---+---+---+---+---+---+
```
The sole survivor: the second cell in the top row.

**Masking Lemma 1**: Given a perfect maze (*i.e.* a tree), repeatedly removing dead ends leaves a perfect maze (or tree) consisting of a single cell.

On the other hand, if our maze has a circuit, we will end up exposing the cells contained in circuits.

## 4. Exposing circuits (and *bridges*)

### 4.1. Introducing circuits into a maze

Let's create a maze with some circuits.  We start with a perfect maze.  To create a single circuit, we need to add one passage.  Adding more passages introduces more circuits.  First our perfect maze:
```
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       21
                             cells       40
                          passages       39
                 paths constructed       21
                     cells visited      132
                          circuits       32
                    markers placed       79
                   markers removed       40
                     starting cell  (1, 4)
>>> print(maze)
+---+---+---+---+---+---+---+---+
|   |               |       |   |
+   +   +---+---+   +   +   +   +
|       |   |       |   |   |   |
+---+---+   +---+   +   +   +   +
|                   |   |   |   |
+---+   +---+   +---+   +---+   +
|   |   |           |           |
+   +   +---+---+   +---+   +   +
|       |                   |   |
+---+---+---+---+---+---+---+---+
```

Now we will add two passages:
```
>>> cell1 = maze.grid[0,1]; cell1.label = "1"
>>> cell1.is_linked(cell1.east)
False
>>> maze.link(cell1, cell1.east)
>>> cell2 = maze.grid[1,1]; cell2.label = "2"
>>> cell2.is_linked(cell2.east)
False
>>> maze.link(cell2, cell2.east)
>>> print(maze)
+---+---+---+---+---+---+---+---+
|   |               |       |   |
+   +   +---+---+   +   +   +   +
|       |   |       |   |   |   |
+---+---+   +---+   +   +   +   +
|                   |   |   |   |
+---+   +---+   +---+   +---+   +
|   | 2             |           |
+   +   +---+---+   +---+   +   +
|     1                     |   |
+---+---+---+---+---+---+---+---+
```
One obvious circuit starts at cell 1, proceeds east 3 steps, north 1 step, west 3 steps (to cell 2), and south 1 step back to cell 1.  Another circuit starts at cell 2, proceeds east 2 steps, north 1 step, west 2 steps, and south 1 step back to cell 2.  A third circuit is more complicated.  Starting at cell 1,go east 3, north 1, west 1, north 1, west 2, and south 2, returning to cell 1.

These are simple circuits: none of the cells except the terminals are repeats.  If we treat circuits as sets instead of as sequences, these three circuits are all the circuits in the maze.

(Adding one passage to a perfect maze creates a single circuit.  Adding two passages can create two disjoint circuits, or it can create three circuits that share some cells.)

### 4.2. Removing dead ends from a maze with circuits

Now let us repeatedly mask dead ends:
```
>>> while True:
...    more_deaths = DeadEnds(maze)
...    if len(more_deaths) < 1: break
...    for cell in more_deaths: cell.hide()
... 
>>> print(maze)
+---+---+---+---+---+---+---+---+
|███|███ ███ ███ ███|███ ███|███|
+   +   +---+---+   +   +   +   +
|███ ███|███|███ ███|███|███|███|
+---+---+   +---+   +   +   +   +
|███             ███|███|███|███|
+---+   +---+   +---+   +---+   +
|███| 2             |███ ███ ███|
+   +   +---+---+   +---+   +   +
|███  1              ███ ███|███|
+---+---+---+---+---+---+---+---+
```
Our three circuits have been preserved.

**Masking Lemma 2**: Given a connected maze with circuits, repeatedly removing dead ends leaves a connected maze containing all the cells which are contains all the circuits.  (It may also contain *bridge* cells.)

### 4.3. Uh! Where did those *bridges* come from?!?!?

Consider the following barbell maze -- the masked cells are not part of the maze:
```
+---+---+---+       +---+---+---+
| 1   1   1 |       | 2   2   2 |
+   +---+   +---+---+   +---+   +
| 1 |███| 1   B   B   2 |███| 2 |
+   +---+   +---+---+   +---+   +
| 1   1   1 |       | 2   2   2 |
+---+---+---+       +---+---+---+
```
It consists of two disjoint circuits (with cells labelled '1' or '2') and two *bridge* cells (labelled 'B').  There are no dead ends that can be removed.

Removing a bridge cell disconnects the maze.  Removing a cell from either of the circuits breaks the circuit, but does not disconnect either the maze or the rest of the circuit.

We could obtain this barbell maze in one step by removing the dead ends (labelled 'd') from the following maze:
```
+---+---+---+---+---+---+---+---+
| 1   1   1   d | d   2   2   2 |
+   +---+   +---+---+   +---+   +
| 1   d | 1   B   B   2   d | 2 |
+   +---+   +   +   +   +---+   +
| 1   1   1 | d | d | 2   2   2 |
+---+---+---+---+---+---+---+---+
```

So, yes, we needed to mention those *bridges* in **Masking Lemma 2**.

## 5. Sampling

There are times when we want to work with a subset of the dead ends.  There are two built-in ways that we can create a subset or sample.

Let's start with a maze:
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       27
                             cells       65
                          passages       64
                 paths constructed       27
                     cells visited      407
                          circuits      128
                    markers placed      252
                   markers removed      188
                     starting cell  (1, 5)
>>> dead = DeadEnds(maze)
>>> len(dead)
20
```

### 5.1. Specifying the size of the subset

One way of generating a sample is specifying the size of the sample.  We have twenty dead ends in our maze.  Let's say we want to randomly choose exactly five dead ends.  (In statistics, this is sampling *without replacement*.  In other words, we don't choose a cell more than once.)

```
>>> dead.sample(5)
method DeadEnds.sample: 15 cells removed,
        5 cells remain in the sample
>>> list(cell.index for cell in dead)
[(4, 2), (0, 10), (0, 12), (4, 0), (0, 4)]
```

### 5.2. Recovering the full set

We can recover the full set using the *DeadEnds.configure()* method:
```
>>> dead.configure()
>>> len(dead)
20
```

### 5.3. Another way to sample

Imagine we have 20 people.  We tried choosing five.  But those five complained that they weren't picked at random.  So we decide to use two flips of a fair coin -- if both tosses are tails (1 in 4 probability!), then that person is chosen.  On average, we get five people, but depending on the outcome of all forty flips, we could have a sample of anywhere from zero to twenty people.  Zero is of course not very likely, and twenty is even more remote.

So let's use the same idea to select a sample of *approximately* five dead end cells.  We'll use an unfair coin with a 75% probability of heads:
```
>>> dead.discard_on_head(bias=0.75)
method DeadEnds.discard_on_head: 15 cells removed,
        5 cells remain in the sample
>>> list(cell.index for cell in dead)
[(0, 11), (4, 8), (4, 4), (4, 0), (1, 4)]
```
(Dead on! If you'll forgive the pun.)

Of course, repeating the process might not give us exactly five cells:
```
>>> dead.configure()
>>> dead.discard_on_head(bias=0.75)
method DeadEnds.discard_on_head: 16 cells removed,
        4 cells remain in the sample
>>> list(cell.index for cell in dead)
[(3, 11), (4, 11), (4, 9), (0, 10)]
```

## 6. Removing dead ends by linking

On a rectangular grid, if every cell is unmasked, then every cell has at least two neighbors.  One way we can get rid of dead ends is by masking them.  Another way is by adding a second way out (and creating a circuit in the process).

Let's look at the options in method *DeadEnds.remove\_by\_linking()*:
```
>>> help(dead.remove_by_linking)
remove_by_linking(action:str='all', q:int=0, bias:float=0.5,
                  quiet:bool=False)
    remove dead ends

    Remove some or all of the dead ends by linking them with a random
    neighbor.

    OPTIONAL ARGUMENTS

        action (default: all) - which dead ends will be removed?

            Possible values are:

                all - all the dead ends in the maze (except any with
                    just one grid connection)

                flip, toss - extract a sample using a series of coin
                   tosses (option: bias)

                sample - extract a fixed size sample (option: n)

                use_me - use whatever cells happen to be in the
                    set 'dead_end'

            Only the first letter ('a', 'f', 't', 's', or 'u') is
            significant.

        q - (default: half the sample) number to sample.

        bias - proportion of heads (discards).

        quiet (default: False) if False, displays status messages.
```

### 6.1. Removing all by linking

The first possibility is removing all the dead ends.  Let's continue with the maze from the last section.  We'll label the cells:
```
>>> dead.configure()     # restore the sample to all
>>> len(dead)
20
>>> for cell in dead: cell.label="D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D | D | D       D |           | D | D       D | D |
+   +   +---+   +---+   +---+   +   +---+   +---+   +
|   |                   |       |           | D |   |
+   +---+   +---+---+---+   +   +   +---+   +   +   +
|           |           | D |       | D             |
+---+   +---+   +---+   +---+   +---+---+   +---+   +
|         D |     D |             D | D         |   |
+   +---+---+---+---+---+---+   +---+---+---+   +   +
|                 D | D                   D | D | D |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The default action is "all" (or just "a").  So we don't need any options.  The "all" action does a *configure()* to restore all the dead ends -- just in case you are just playing with sampling...
```
>>> dead.remove_by_linking()
method DeadEnds.configure: 20 dead ends
method DeadEnds.remove_by_linking
        before: 20 samples, new passages: 15, after: 0 samples
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D   D   D       D             | D   D       D   D |
+   +   +   +   +---+   +---+   +   +---+   +---+   +
|   |                   |       |             D |   |
+   +---+   +---+---+---+   +   +   +---+   +   +   +
|           |           | D |       | D             |
+---+   +   +   +---+   +   +   +   +   +   +---+   +
|         D |     D |             D | D         |   |
+   +---+---+---+   +   +---+   +---+---+---+   +   +
|                 D | D                   D   D   D |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
After adding fifteen passages to give 15 dead ends an additional way out, each of the twenty original dead ends had a second exit.

### 6.2. Removing a sample by linking

We need a fresh maze...
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       31
                             cells       65
                          passages       64
                 paths constructed       31
                     cells visited      275
                          circuits       69
                    markers placed      175
                   markers removed      111
                     starting cell  (4, 9)
>>> dead = DeadEnds(maze)
>>> len(dead)
22
>>> for cell in dead: cell.label="D"
... 
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|         D | D |     D | D | D     |     D | D | D |
+   +---+---+   +   +---+   +---+   +   +---+   +   +
|       | D     |             D |         D |       |
+---+   +---+   +---+   +---+---+---+   +---+   +   +
| D                 |   | D | D     |       |   |   |
+---+   +   +---+   +   +   +---+   +---+   +   +   +
| D     | D | D |                   | D         |   |
+---+   +---+   +---+   +---+   +   +---+---+   +   +
| D             | D     | D     |               | D |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The default for *action="sample"* is *q=11* (half of the dead ends).  (If the number of dead ends is odd, rounding is to the nearest *even* integer.  Half of both 19 and 21, rounded, is 10.)  We can, of course supply a value for *q*, but we'll use the default:
```
>>> dead.remove_by_linking(action="s")
method DeadEnds.sample: 11 cells removed, 11 cells remain in the sample
method DeadEnds.remove_by_linking before: 11 samples,
        new passages: 9, after: 0 samples
```
Nine passages were added to provide eleven dead ends with an additional exit.

What about the remaining dead ends?
```
>>> dead.configure()
>>> len(dead)
9
```
Two of the remaining dead ends were linked to dead ends in the eleven-cell sample.  So just nine remain.
```
>>> for cell in dead: cell.label="X"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|         D   D |     D   D   D     |     X | D   D |
+   +---+---+   +   +---+   +---+   +   +---+   +   +
|       | X     |             X |         D         |
+---+   +---+   +---+   +---+---+---+   +---+   +   +
| X                 |   | X | D     |       |   |   |
+---+   +   +---+   +   +   +   +   +---+   +   +   +
| D     | D | X |                   | X         |   |
+   +   +   +   +---+   +---+   +   +---+---+   +   +
| D             | X       D     |               | X |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 6.3 Removing a coin-flip sample by linking

Again let's start fresh:
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       23
                             cells       65
                          passages       64
                 paths constructed       23
                     cells visited      349
                          circuits      102
                    markers placed      224
                   markers removed      160
                     starting cell  (4, 7)
>>> dead = DeadEnds(maze)
>>> len(dead)
16
>>> for cell in dead: cell.label="D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     D |                     D |                 D |
+   +---+   +---+---+   +---+---+   +---+---+---+---+
|           |       |               | D | D     | D |
+   +---+   +   +   +---+   +---+---+   +---+   +   +
|       |       |   | D     | D | D |   |           |
+---+   +---+   +   +---+---+   +   +   +   +---+---+
| D | D | D     |                   |       |     D |
+   +---+---+   +---+   +---+   +---+   +---+   +---+
|                 D |     D |                     D |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

For *action="flip"* (or *"toss"* or just *"f"* or *"t"*), the default is a fair coin.  Heads discard a cell, so let's discard approximately 75%:
```
>>> dead.remove_by_linking(action="t", bias=0.75)
method DeadEnds.discard_on_head: 13 cells removed,
        3 cells remain in the sample
method DeadEnds.remove_by_linking before: 3 samples,
       new passages: 3, after: 0 samples
```
75% of 16 is 12, the expected number to remove.  The actual number removed was 13.  The three remaining dead ends were given an additional exit using three passages.
```
>>> dead.configure()
>>> len(dead)
11
```
Two of the three dead added passages joined a dead end in the sample with one outside the sample.  Eleven dead ends remain (labelled "X"):
```
>>> for cell in dead: cell.label="X"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     X |                     X |                 D |
+   +---+   +---+---+   +---+---+   +---+---+---+   +
|           |       |               | D   D     | D |
+   +---+   +   +   +---+   +---+---+   +---+   +   +
|       |       |   | X     | X | X |   |           |
+   +   +---+   +   +---+---+   +   +   +   +---+---+
| D | X | X     |                   |       |     X |
+   +---+---+   +---+   +---+   +---+   +---+   +---+
|                 X |     X |                     X |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 6.4 Removing a custom sample by linking

One additional possibility remains -- a custom sample. The action *"use\_me* or *custom* makes this possible... Again we start with a fresh maze:
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       30
                             cells       65
                          passages       64
                 paths constructed       30
                     cells visited      228
                          circuits       58
                    markers placed      140
                   markers removed       76
                     starting cell  (4, 2)
>>> dead = DeadEnds(maze)
>>> len(dead)
18
>>> for cell in dead: cell.label="D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D         |             D | D |                 D |
+---+---+   +   +---+---+---+   +   +   +   +---+---+
| D | D |   |       | D         |   |   | D | D | D |
+   +   +   +---+   +---+   +   +   +   +---+   +   +
|       |           | D     |       |               |
+   +---+---+   +   +---+   +---+   +---+   +---+   +
|   | D         |             D |   | D     | D |   |
+   +---+   +---+---+---+---+---+   +---+---+   +   +
|                             D | D | D             |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Let's create a custom sample.  Those four dead ends in the northeast corner look interesting.  We'll take those, along with the northwest corner cell.  And just for fun, we'll throw in a cell which is not a dead end.  (User error is a factor to consider.)
```
>>> grid = maze.grid
1>> custom = [grid[4,0], grid[3,12], grid[3,11], grid[3,10], grid[4,12]]
2>> fubar = grid[2,2]; fubar.label = 'f'; len(list(fubar.passages))
2
3>> custom.append(fubar)
4>> list(cell.char for cell in custom)
['D', 'D', 'D', 'D', 'D', 'f']
```
In line 1, we add the five chosen dead ends.  In line 2, we label a cell which is not a dead end, verify afterwards that the cell isn't a dead end.  (Its degree is 2.)  In line 3, we add the cell from line 2 to our custom list.  Finally , in line 4, we check that the cells in our custom list are the ones that we intended to choose.

Now let's run the custom...  First, we set the dead ends sample to the custom list of six cells:
```
>>> dead.dead_ends = custom    # property setter
>>> type(dead.dead_ends)
<class 'set'>
>>> len(dead)
6
```
(Our custom *list* of six cells has been *copied* into a *set* of six cells.  And here we go:
```
>>> dead.remove_by_linking(action="c")
User sample: 6 cells
ERROR: Cell[(2, 2)] is not a dead end. (ignored)
```
Aha!  It found our little surprise!

```
method DeadEnds.remove_by_linking before: 6 samples, new passages: 3,
    after: 1 samples
>>> for cell in dead: print(cell.index)
...
(2, 2)
```
And our surprise cell was left unprocessed...  What's left?
```
>>> dead.configure()
>>> for cell in dead: cell.label = "X"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D         |             X | X |                 D |
+   +---+   +   +---+---+---+   +   +   +   +---+   +
| D | X |   |       | X         |   |   | D   D | D |
+   +   +   +---+   +---+   +   +   +   +---+   +   +
|       | f         | X     |       |               |
+   +---+---+   +   +---+   +---+   +---+   +---+   +
|   | X         |             X |   | X     | X |   |
+   +---+   +---+---+---+---+---+   +---+---+   +   +
|                             X | X | X             |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Our five legitimate dead ends were given additional exits by adding three passages.  In the upper right, two of those three passages joined the dead ends in pairs, while the third passage joined our candidate in the northwest corned to its neighbor to the south -- which happened to be a dead end.  The illegitimate cell was untouched.  The dead ends that remain are labelled 'X'.

## 7. Removing dead ends in pairs

In our custom example in the previous section (Subsection 6.4), the dead ends were all accidentally linked to other dead ends.  We can make this a requirement using the *DeadEnds.link\_pairs()* method.  The *action* option is the same as for removing dead ends by linking (Section 6), so we will just use the *action="all"* option.

We start with a fresh maze:
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       29
                             cells       65
                          passages       64
                 paths constructed       29
                     cells visited      337
                          circuits       91
                    markers placed      217
                   markers removed      153
                     starting cell  (3, 1)
>>> dead = DeadEnds(maze); len(dead)
18
>>> for cell in dead: cell.label="D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D                             | D       D | D     |
+---+---+---+   +   +---+---+   +---+   +---+---+   +
|         D |   |     D | D |                       |
+   +   +---+   +   +---+   +---+---+---+---+   +---+
|   |       | D |           |       |     D |   | D |
+   +---+   +---+   +   +---+   +   +   +---+   +   +
| D | D     | D |   |           | D |           |   |
+---+---+   +   +   +---+---+   +---+---+---+   +   +
| D                       D |     D | D             |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Note that several dead ends, including the dead end in the center of the bottom row, are not adjacent to other dead ends, so they won't be paired.  The dead end in the first cell of row 1 (just north the southwest cell) is adjacent to two dead ends, so one of its two neighbors will be left untouched.  The two dead ends near the northeast corner will be joined by a passage.  We proceed:
```
>>> dead.link_pairs()
method DeadEnds.configure: 18 dead ends
method DeadEnds.link_pairs before: 18 samples, new passages: 5, after: 8 samples
>>> for cell in dead: cell.label="X"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| X                             | X       D   D     |
+---+---+---+   +   +---+---+   +---+   +---+---+   +
|         X |   |     D   D |                       |
+   +   +---+   +   +---+   +---+---+---+---+   +---+
|   |       | D |           |       |     X |   | X |
+   +---+   +   +   +   +---+   +   +   +---+   +   +
| D   D     | D |   |           | D |           |   |
+---+---+   +   +   +---+---+   +   +---+---+   +   +
| X                       X |     D | X             |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Five dead ends were paired, eliminating ten dead ends total.  Eight dead ends could not be paired.

## 8. Removing in pairs, then linking

We can use the two methods in sequence, first pairing dead ends, then linking.  If we use a sample, we need to use the *action="custom"* option when linking if we wish to stick with the sample.

We start with a maze:
```
>>> maze = Maze(OblongGrid(5, 13))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       24
                             cells       65
                          passages       64
                 paths constructed       24
                     cells visited      318
                          circuits       91
                    markers placed      203
                   markers removed      139
                     starting cell  (3, 6)
>>> dead = DeadEnds(maze); len(dead)
20
>>> for cell in dead: cell.label="D"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D | D         |     D | D       D |     D |     D |
+   +---+---+   +   +---+---+   +---+   +---+   +---+
|   |                   |       | D |   |       | D |
+   +   +   +   +---+   +   +   +   +   +   +   +   +
|       | D | D | D |       |           |   |       |
+---+---+---+---+   +   +---+---+   +   +   +   +---+
| D             |       | D     |   | D |   | D | D |
+---+   +   +   +---+   +---+   +   +---+   +---+   +
| D     | D |           | D                         |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

We will use a sample of exactly 18 cells:
```
>>> dead.link_pairs(action="sample", q=18)
method DeadEnds.sample: 2 cells removed, 18 cells remain in the sample
method DeadEnds.link_pairs before: 18 samples, new passages: 8,
        after: 2 samples
```
Let's look at the result of this step...
```
>>> for cell in dead: cell.label="2"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D   D         |     D   D       D |     D |     D |
+   +---+---+   +   +---+---+   +   +   +---+   +   +
|   |                   |       | D |   |       | D |
+   +   +   +   +---+   +   +   +   +   +   +   +   +
|       | D | D   D |       |           |   |       |
+---+---+---+---+   +   +---+---+   +   +   +   +---+
| D             |       | D     |   | 2 |   | D   D |
+   +   +   +   +---+   +   +   +   +---+   +---+   +
| D     | 2 |           | D                         |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The two dead ends labelled "2" remain in the sample -- the other sixteen were paired by carving eight passages.  That accounts for all eighteen sample dead ends.  Two dead ends are unaccounted for, one in row 2 column 2, and the other in row 4 column 10.  Let's mark these for reference:
```
>>> maze.grid[2,2].label="X"
>>> maze.grid[4,10].label="X"
```

Now we want to use the two dead ends in the sample and leave the two marked dead ends untouched.  The only way to do this is with the custom option.  But we don't need to create a custom set as the *DeadEnd* object already has the required set (*i.e.*, the cells labelled "2").
```
>>> dead.remove_by_linking(action="custom")
User sample: 2 cells
method DeadEnds.remove_by_linking before: 2 samples, new passages: 2,
        after: 0 samples
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| D   D         |     D   D       D |     X |     D |
+   +---+---+   +   +---+---+   +   +   +---+   +   +
|   |                   |       | D |   |       | D |
+   +   +   +   +---+   +   +   +   +   +   +   +   +
|       | X | D   D |       |           |   |       |
+---+---+---+---+   +   +---+---+   +   +   +   +---+
| D             |       | D     |   | 2 |   | D   D |
+   +   +   +   +---+   +   +   +   +   +   +---+   +
| D       2 |           | D                         |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The cells labelled "2" are no longer dead ends, but the cells labelled "X" are still dead ends.  We can easily verify this by programming:
```
>>> dead.configure()
>>> list(cell.index for cell in dead)
[(4, 10), (2, 2)]
```
After reconfiguring, the two marked cells show up as dead ends.