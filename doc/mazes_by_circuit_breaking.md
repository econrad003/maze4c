# Full log for run of module *demos.circuit\_elimination*

## Metadata

* Date: 18 November 2025
* Command line:
```
        $ python -m demos.circuit_elimination -A etc8 -R 12345/3
                 -b 45 -B 5 > output.md
```

## Log with comments

### Argparse namespace

```
Namespace(dim=(8, 13), quiet=False, very_quiet=False, automaton='etc8', rules='12345/3', bias=45, border=5)
```

The 8-neighbor edge on a 13×18 torus automaton with Conway rule "12345/3" will be used to create an 8×13 rectangular maze.  No messages will be suppressed.

### Phase 1. Maze creation using a cellular automaton

```
Starting the cellular automaton (12345/3)...
```

This is the starting state of the maze.  Approximately 45% of the edges in the torus were marked as *alive*.  (Bias=45%)
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |       |   |   |   |           |           |   |
+---+---+---+   +   +   +---+   +   +   +---+   +---+
|   |       |   |   |               |   |   |   |   |
+---+---+   +---+   +   +---+---+---+---+   +   +---+
|   |           |   |   |       |       |   |   |   |
+---+---+---+   +---+---+   +---+   +---+---+---+   +
|               |   |       |   |       |       |   |
+   +---+   +---+   +   +---+   +---+---+---+   +---+
|   |       |   |           |   |       |           |
+---+   +---+---+   +---+   +---+   +---+   +   +   +
|   |   |   |               |   |   |           |   |
+---+---+---+---+   +   +---+---+---+   +---+---+---+
|           |   |   |   |   |       |           |   |
+---+   +   +   +---+---+---+---+   +---+---+   +   +
|       |       |   |           |       |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+

```

And here we proceed through up to 50 generations:
```
generation 0: (automaton) 210 alive; (maze) 78 passages.
generation 1: (automaton) 256 alive; (maze) 109 passages.
generation 2: (automaton) 247 alive; (maze) 101 passages.
generation 3: (automaton) 254 alive; (maze) 104 passages.
generation 4: (automaton) 257 alive; (maze) 104 passages.
generation 5: (automaton) 256 alive; (maze) 104 passages.
generation 5: stable configuration
The automation was stable after 5 generations
```
Stability was verified in generation 5.

Here is the maze as finished by the cellular automaton:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           |               |
+---+   +---+   +---+   +---+   +   +   +---+   +---+
|   |       |       |               |       |   |   |  <---
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |           |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |           |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           |   |  <---
+---+   +   +---+   +   +---+   +   +---+---+   +---+
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
Cellular automaton complete...
```

### Eulerian analysis

```
e=104, v=104, k=3, e-v+k=3
```

The maze is disconnected with *k=3* components.  (Note the arrows pointing to two isolated cells.)  There are *e=104* passages and *v=104* cells.  The Euler characteristic is given by χ=e-v+k=3.  That tells us that we are three circuits away from a forest.  (There may be more than 3 circuits, but we just need to break three circuits in order to to eliminate every circuit.)

We will then need to add two edges reduce the number of components to 1.

### Circuit elimination

We use depth-first search to locate circuits.  Instead of identify the circuits, we simply remove the critical edge detected by DFS.
```
Removing circuits...
          DFS Circuit Locator (statistics)
                            visits      109
                        start cell  (7, 7)
                  components found        1
               components finished        0
                     cells visited       53
                           shuffle        1
               maximum stack depth       33
                           circuit  ((5, 11), (5, 10))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           | *   *   *     |
+---+   +---+   +---+   +---+   +   +   +---+   +---+
|   |       |       |               | *   * | * |   |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       | U | V     |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |           |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           |   |
+---+   +   +---+   +   +---+   +   +---+---+   +---+
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The edge from U to V was removed.  The asterisks show the rest of the circuit that was broken.

```
          DFS Circuit Locator (statistics)
                            visits       71
                        start cell  (6, 10)
                  components found        1
               components finished        0
                     cells visited       28
                           shuffle        1
               maximum stack depth       10
                           circuit  ((2, 9), (2, 10))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           |               |
+---+   +---+   +---+   +---+   +   +   +---+   +---+
|   |       |       |               |       |   |   |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |   |       |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |         *   *   * |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   | U | V | *   * |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       | *   *   * |   |
+---+   +   +---+   +   +---+   +   +---+---+   +---+
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Above we show the second broken circuit.

```
          DFS Circuit Locator (statistics)
                            visits        9
                        start cell  (6, 8)
                  components found        1
               components finished        0
                     cells visited        5
                           shuffle        1
               maximum stack depth        4
                           circuit  ((6, 7), (6, 8))
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |     *   * |               |
+---+   +---+   +---+   +---+   +   +   +---+   +---+
|   |       |       |         U | V |       |   |   |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |   |       |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |   |       |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           |   |
+---+   +   +---+   +   +---+   +   +---+---+   +---+
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
And that's the last of the circuits...

```
e=101, v=104, k=3, e-v+k=0
```
The Euler characteristic is 0, so there are indeed no circuits,  Since the number of components (*k=3*) is greater than 1, the maze is a forest but not a tree,

### Merging components

We need to add two edges to join the components.  We need to "knock down" two of the six walls that bound the components.  Of course, not any two walls...  Once we choose one wall, we will be left with just three possible walls.  Of the fifteen possible combinations of six walls, only nine will work.

```
Joining components...
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           |               |
+---+   +---+   +---+   +---+   +   +   +---+   +---+
|   |       |       |           |   |       |   |   |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |   |       |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |   |       |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           | U |
+---+   +   +---+   +   +---+   +   +---+---+   +   +
|       |       |               |           |     V |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
linked grid[(1, 12)]--grid[(0, 12)]
e=102, v=104, k=2, e-v+k=0
```
The first choice was in the lower right...

```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           |             V |
+---+   +---+   +---+   +---+   +   +   +---+   +   +
|   |       |       |           |   |       |   | U |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |   |       |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |   |       |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           |   |
+---+   +   +---+   +   +---+   +   +---+---+   +   +
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
linked grid[(6, 12)]--grid[(7, 12)]
e=103, v=104, k=1, e-v+k=0
```
And the second choice was in the upper right.

### Summary

The final maze:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |           |               |
+---+   +---+   +---+   +---+   +   +   +---+   +   +
|   |       |       |           |   |       |   |   |
+   +   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |       |       |       |       |   |       |
+   +   +---+   +   +---+   +---+   +   +   +---+   +
|           |       |       |       |   |       |   |
+   +---+   +---+   +   +---+---+---+---+   +   +---+
|   |   |       |       |                   |       |
+---+   +   +---+   +---+   +   +   +---+   +---+   +
|           |       |       |   |   |   |       |   |
+   +---+---+   +---+---+   +---+---+   +---+   +---+
|           |       |       |       |           |   |
+---+   +   +---+   +   +---+   +   +---+---+   +   +
|       |       |               |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
Expected: e=103, v=104, k=1, e-v+k=0
  Actual: e=103, v=104, k=1, e-v+k=0
```
And we verify that it is a perfect maze: one component and one passage shy of the number of cells.