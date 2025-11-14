# Maze creation using an edge-based cellular automaton

Module: *mazes.Cellular.etc\_automaton*
Classes: *Automaton*, *Automaton2*

## The theory

### What does the "etc" mean?

* e = edge-based
* t = torus
* c = Conway-style birth/death rules

### Neighborhoods

The automaton looks at grid edges on a toroidal lattice.  These edges are the cells of the lattice.  (Don't confuse the cells of the automaton with cells in a maze.  Yes, the terminology is confusing, but mazes and cellular automata are two separate contexts.  If we talk about *pounds of potatoes*, we mean a unit of weight, but if we say *the potatoes cost a pound*, we mean a monetary unit.  Context is important.)

There are two types of neighborhoods.

In class *Automaton* each cell (or grid edge) has six neighboring cells.  The neighbors of a grid edge in class *Automaton* are the six incident grid edges.

In class *Automaton2* each cell (or grid edge) has eight neighboring cells.  The neighbors of a grid edge in class *Automaton2* include the six incident grid edges plus the two grid edges that run parallel immediately either left and right or up and down.

```
          Figure 1                         Figure 2
    +---+---+---+---+---+            +---+---+---+---+---+
    |   |   | 2 |   |   |            |   |   |   |   |   |
    +---+---+---+---+---+            +---+---+---+---+---+
    |   | 1 | B | 3 |   |            |   |   | 6 | 1 |   |
    +---+---+ | +---+---+            +---+---+---+---+---+
    |   | 6 | A | 4 |   |            |   | 5 | A - B | 2 |
    +---+---+---+---+---+            +---+---+---+---+---+
    |   |   | 5 |   |   |            |   |   | 4 | 3 |   |
    +---+---+---+---+---+            +---+---+---+---+---+
    |   |   |   |   |   |            |   |   |   |   |   |
    +---+---+---+---+---+            +---+---+---+---+---+
```

In Figure 1, we have a north-south edge {A,B}.  The incident edges, *i.e.*
edges other than {A,B} which share a *vertex* with edge {A,B}, are {B,1}, {B,2}, {B,3}, {A,4}, {A,5}, and {A,6}.  These six edges are neighbors of {A,B} in both automata.

Class *Automaton2* adds two edges to the neighborhood, namely {3,4} an {6,1}.

If we look at the east-west edge {A,B} in Figure 2, the incident edges are {B,1}, {B,2}, {B,3}, {A,4}, {A,5}, and {A,6}.  The two edges added in class *Automaton2* are {3,4} and {6,1}.

Since we are using a toroidal lattice, the bottom edge of the lattice is due north of the top edge and the left edge of the lattice is due east of the right edge.

### Conway rules

Named after mathematician John Conway, they consist of two sets, denoted as a birth rule and a death rule.

Each cell (*i.e.* each grid edge) is either *alive* or *dead* at any given time.  If *s(c,t)* is the state of a cell at time t, then the state *s(c,t+1)* at time t+1 is governed by two rules:

* the birth rule applies if *s(c,t)* = *dead* -- if and only if the number of living neighbors satisfies the birth rule, then *s(c,t+1)* = *alive*; and
* the death rule applies if *s(c,t)* = *alive* -- if and only if the number of living neighbors satisfies the death rule, then *s(c,t+1)* = *alive*.

In shorthand, if the rules are "23|3":

* the birth rule (after the vertical bar) is the set {3}: a dead cell with exactly three living neighbors becomes alive; and
* the death rule (before the vertical bar) is the set {2,3}: a live cell with either two or three living neighbors remains alive.

In all other cases, the cell is dead in the next time unit.

Changes happen at the same time. The state *s(c,t+1)* depends only on the number of living neighbors of cell *c* at time *t*.

For example, if an asterisk denotes grid edges which are alive, then consider the following configuration in class *Automaton*:
```
        +---+---+---+---+---+
        |   |   |   |   |   |
        +---+---+ * +---+---+
        |   |   |   |   |   |       Figure 3a - living edges at time t
        +---+---+ * + * +---+
        |   |   |   |   |   |
        +---+---+ * +---+---+
        |   |   |   |   |   |
        +---+---+---+---+---+
        |   |   |   |   |   |
        +---+---+---+---+---+

        +-0-+-0-+-1-+-0-+-0-+
        0   0   1   1   0   0
        +-0-+-1-+ 1 +-2-+-0-+
        0   0   2   3   0   0       Figure 3b - numbers of edges incident to
        +-0-+-1-+ 3 + 1 +-1-+           living edges
        0   0   2   3   0   0
        +-0-+-1-+ 1 +-2-+-0-+
        0   0   1   1   0   0
        +-0-+-0-+-1-+-0-+-0-+
        0   0   0   0   0   0
        +-0-+-0-+-0-+-0-+-0-+

        +---+---+---+---+---+
        |   |   |   |   |   |
        +---+---+---+---+---+
        |   |   |   *   |   |       Figure 3c - living edges at time t+1
        +---+---+ * +---+---+
        |   |   |   *   |   |
        +---+---+---+---+---+
        |   |   |   |   |   |
        +---+---+---+---+---+
        |   |   |   |   |   |
        +---+---+---+---+---+
```
In Figure 3b, any edge with any number other than 2 or 3 will die or remain dead.  Any edge with a 3 will become or remain alive.  Edges with a 2 remain in the same state as at time t.

### From automata to mazes

Cells in the top few rows and columns might be a border.  Those are ignored.  The north and east boundary edges are always a border.  Removing the border, any live edges become passages, and any dead edges bcome walls.

## Example 1: Generating a maze using the incident edges automaton

We first initialize the automaton.  That involves an import and a call to the constructor:
```
$ python
Python 3.10.12
>>> from mazes.Cellular.etc_automaton import Automaton
>>> ca = Automaton({3}, {1,2,3,4,5}, 8, 13, bias=0.4)
```
Our rule set is "12345/3".  Our birth rule {3} says that passage is born from a wall if and only if the wall is incident to exactly three passages.  The generated maze will be a rectangular maze with 8 rows and 13 columns.  The bias argument of 0.4 (default: 0.1) says that the state of a cell at time 0 has a 40% chance of being alive.  In addition, there is a border argument (default: 5) which tells us the number of extra rows and columns.  A border of 5 on an 8×13 maze uses a 13×18 toroidal grid.

Next we run several generations:
```
>>> for _ in range(30): ca.next_generation()
...
```
We're going for 30 generations...

```
generation 0: (automaton) 178 alive; (maze) 60 passages.
generation 1: (automaton) 248 alive; (maze) 98 passages.
generation 2: (automaton) 285 alive; (maze) 115 passages.
generation 3: (automaton) 288 alive; (maze) 113 passages.
generation 4: (automaton) 300 alive; (maze) 119 passages.
generation 5: (automaton) 307 alive; (maze) 121 passages.
generation 6: (automaton) 317 alive; (maze) 126 passages.
generation 7: (automaton) 322 alive; (maze) 129 passages.
generation 8: (automaton) 322 alive; (maze) 130 passages.
generation 9: (automaton) 324 alive; (maze) 130 passages.
generation 10: (automaton) 325 alive; (maze) 130 passages.
generation 11: (automaton) 326 alive; (maze) 130 passages.
generation 12: (automaton) 329 alive; (maze) 130 passages.
generation 13: (automaton) 329 alive; (maze) 130 passages.
generation 14: (automaton) 333 alive; (maze) 130 passages.
generation 15: (automaton) 335 alive; (maze) 131 passages.
generation 15: stable configuration
Warning: generation 15: stable configuration
```
A *Warning* exception was raised -- the message: "stable configuration".  What it means is that generation 16 is the same as generation 15.  Since there is no time delay in state changes, there is no point in running more generations -- the state won't change.

If we are running inside a program, we need to trap the *Warning* exception:
```python
    try:
        for _ in range(30):
            ca.next_generation()
    except Warning as msg:
        if msg == "stable configuration:
            print("maze is ready)
        else:
            raise Warning(msg)   # something else happened
```

Here is the maze that we built:
```
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |                           |           |   |
+   +   +   +   +   +---+---+---+   +   +   +---+   +
|   |                               |       |       |
+   +   +---+---+---+   +   +   +   +   +   +   +   +
|   |                       |   |               |   |
+   +   +---+   +   +   +   +   +   +---+---+   +   +
|       |   |   |       |       |                   |
+---+---+---+---+   +   +   +   +   +   +   +---+---+
|           |   |               |   |               |
+   +   +---+   +   +---+---+   +   +   +---+   +   +
|               |                                   |
+---+   +   +---+   +   +   +---+---+   +   +---+---+
|           |       |   |                           |
+   +---+---+   +---+   +   +   +   +---+---+   +   +
|               |       |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Some observations... This is not a perfect maze.  This algorithm may produce mazes that are disconnected as well as mazes that have circuits.  This one has an isolated cell in row 4 column 2 (so it is disconnected as well as a four-cell circuit in the lower right.

```
>>> len(ca.grid)
104
>>> len(ca.maze)
131
```
The maze has just 104 cells and 131 passages, so, in fact, it has a boatload of circuits.

## Example 2: Same automaton with different rules...

In addition, we'll remove all but the north and east boundaries from the border:
```
>>> ca = Automaton({3}, {1,2,3,4}, 8, 13, bias=0.4, border=0)
```

Thirty generations -- maybe:
```
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 82 alive; (maze) 73 passages.
generation 1: (automaton) 108 alive; (maze) 100 passages.
generation 2: (automaton) 117 alive; (maze) 106 passages.
generation 3: (automaton) 117 alive; (maze) 105 passages.
generation 4: (automaton) 123 alive; (maze) 113 passages.
generation 5: (automaton) 118 alive; (maze) 104 passages.
generation 6: (automaton) 131 alive; (maze) 117 passages.
generation 7: (automaton) 126 alive; (maze) 113 passages.
generation 8: (automaton) 129 alive; (maze) 115 passages.
generation 9: (automaton) 126 alive; (maze) 113 passages.
generation 10: (automaton) 129 alive; (maze) 115 passages.
generation 11: (automaton) 126 alive; (maze) 113 passages.
generation 12: (automaton) 129 alive; (maze) 115 passages.
generation 13: (automaton) 126 alive; (maze) 113 passages.
generation 14: (automaton) 129 alive; (maze) 115 passages.
generation 15: (automaton) 126 alive; (maze) 113 passages.
generation 16: (automaton) 129 alive; (maze) 115 passages.
generation 17: (automaton) 126 alive; (maze) 113 passages.
generation 18: (automaton) 129 alive; (maze) 115 passages.
generation 19: (automaton) 126 alive; (maze) 113 passages.
generation 20: (automaton) 129 alive; (maze) 115 passages.
generation 21: (automaton) 126 alive; (maze) 113 passages.
generation 22: (automaton) 129 alive; (maze) 115 passages.
generation 23: (automaton) 126 alive; (maze) 113 passages.
generation 24: (automaton) 129 alive; (maze) 115 passages.
generation 25: (automaton) 126 alive; (maze) 113 passages.
generation 26: (automaton) 129 alive; (maze) 115 passages.
generation 27: (automaton) 126 alive; (maze) 113 passages.
generation 28: (automaton) 129 alive; (maze) 115 passages.
generation 29: (automaton) 126 alive; (maze) 113 passages.
```
We didn't end up with a stable configuration. From generation 7 on, we seem to alternate between 115 and 113 passages.

```
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |           |       |           |           |
+---+---+   +---+---+---+   +   +   +---+   +   +---+
|           |               |                       |
+---+   +   +   +---+   +   +   +---+---+---+---+   +
|       |       |       |       |           |       |
+   +   +---+   +   +   +---+---+   +   +   +   +---+
|   |               |       |                       |
+   +   +   +---+   +---+   +   +---+---+   +---+   +
|   |   |           |       |               |       |
+---+   +   +   +   +   +   +---+---+   +   +   +---+
|   |       |       |       |           |           |
+   +---+---+---+---+   +---+   +   +   +---+---+---+
|   |       |           |       |       |       |   |
+   +   +   +   +---+---+   +---+   +---+   +   +   +
|       |           |       |       |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The two cells top left form a component, so this maze is disconnected.  The number of passages tells us that there are circuits, some of which are quite obvious, Seven cells on the lower form a small component with a four-cell circuit.

And here is the next generation:
```
>>> ca.next_generation()
generation 30: (automaton) 129 alive; (maze) 115 passages.
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |           |       |           |           |
+---+---+   +---+---+---+   +   +   +---+   +   +---+
|           |               |                       |
+---+   +   +   +---+   +   +   +---+---+---+---+   +
|       |       |       |       |           |       |
+   +   +---+   +   +   +---+---+   +   +   +   +---+
|   |               |       |           |   |       |
+   +   +   +---+   +---+   +   +---+---+---+---+   +
|   |   |           |       |               |       |
+---+   +   +   +   +   +   +---+---+   +   +   +---+
|   |       |       |       |           |           |
+   +---+---+---+---+   +---+   +   +   +---+---+   +
|   |       |           |       |       |           |
+   +   +   +   +---+---+   +---+   +---+   +   +   +
|       |           |       |       |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 3: the *StopIteration* exception

Here we'll use the rule set "3|5" -- 5 incident passages turns a wall into a passage and anything but 3 incident passages turns a passage into a wall:
```
>>> ca = Automaton({5}, {3}, 8, 13, bias=0.4, border=0)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 82 alive; (maze) 70 passages.
generation 1: (automaton) 27 alive; (maze) 22 passages.
generation 2: (automaton) 5 alive; (maze) 4 passages.
StopIteration: All the grid edges are dead.
```
After 3 generations, all our grid edges died.  A *StopIteration* exception was raised.  There are only two things that can happen when everything is dead.  The first is that everything stays dead.  The second possibility occurs if the birth rule contains zero: everything revives. Neither situation is particularly interesting.

## Example 4: the 8-neighbor automaton

A slightly different import:
```
>>> from mazes.Cellular.etc_automaton import Automaton2
```

Everything else is similar:
```
>>> ca = Automaton2({3}, {1,2,3,4,5}, 8, 13, bias=0.4)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 181 alive; (maze) 70 passages.
generation 1: (automaton) 236 alive; (maze) 86 passages.
generation 2: (automaton) 238 alive; (maze) 93 passages.
generation 3: (automaton) 255 alive; (maze) 98 passages.
generation 4: (automaton) 260 alive; (maze) 100 passages.
generation 5: (automaton) 260 alive; (maze) 100 passages.
generation 6: (automaton) 258 alive; (maze) 99 passages.
generation 6: stable configuration
Warning: generation 6: stable configuration
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |   |       |           |   |
+   +   +---+---+   +---+   +---+   +   +   +---+   +
|   |               |       |       |       |       |
+   +---+---+   +---+   +---+   +   +---+---+   +---+
|   |       |       |   |       |               |   |
+---+   +---+   +---+   +---+---+   +   +---+   +   +
|       |   |   |           |           |       |   |
+   +---+   +   +   +---+   +   +---+---+---+   +---+
|   |   |       |   |       |                       |
+   +   +---+   +   +---+   +---+   +   +---+---+   +
|   |       |           |   |       |       |   |   |
+---+---+   +---+---+   +---+---+   +---+   +   +   +
|       |       |   |       |       |       |       |
+   +   +---+   +   +---+   +   +---+   +---+   +---+
|   |       |   |       |       |       |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The change in topology might result in a change in the biases of mazes that are produced.

## Example 5: 8 neighbors, new rules

### Example 5a
We will try slightly different rule sets.  First:
```
>>> ca = Automaton2({3}, {1,2,3,4}, 8, 13, bias=0.4)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 185 alive; (maze) 70 passages.
generation 1: (automaton) 224 alive; (maze) 89 passages.
generation 2: (automaton) 201 alive; (maze) 90 passages.
generation 3: (automaton) 221 alive; (maze) 90 passages.
generation 4: (automaton) 231 alive; (maze) 87 passages.
generation 5: (automaton) 222 alive; (maze) 93 passages.
generation 6: (automaton) 230 alive; (maze) 90 passages.
generation 7: (automaton) 225 alive; (maze) 91 passages.
generation 8: (automaton) 232 alive; (maze) 91 passages.
generation 9: (automaton) 231 alive; (maze) 92 passages.
generation 10: (automaton) 229 alive; (maze) 94 passages.
generation 11: (automaton) 237 alive; (maze) 94 passages.
generation 12: (automaton) 231 alive; (maze) 93 passages.
generation 13: (automaton) 236 alive; (maze) 93 passages.
generation 14: (automaton) 231 alive; (maze) 93 passages.
generation 15: (automaton) 234 alive; (maze) 93 passages.
generation 16: (automaton) 238 alive; (maze) 93 passages.
generation 17: (automaton) 233 alive; (maze) 93 passages.
generation 18: (automaton) 235 alive; (maze) 93 passages.
generation 19: (automaton) 238 alive; (maze) 93 passages.
generation 20: (automaton) 233 alive; (maze) 93 passages.
generation 21: (automaton) 235 alive; (maze) 93 passages.
generation 22: (automaton) 238 alive; (maze) 93 passages.
generation 23: (automaton) 233 alive; (maze) 93 passages.
generation 24: (automaton) 235 alive; (maze) 93 passages.
generation 25: (automaton) 238 alive; (maze) 93 passages.
generation 26: (automaton) 233 alive; (maze) 93 passages.
generation 27: (automaton) 235 alive; (maze) 93 passages.
generation 28: (automaton) 238 alive; (maze) 93 passages.
generation 29: (automaton) 233 alive; (maze) 93 passages.
```
93 passages with the automaton varying 235, 238 and 233...
```
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |   |       |       |       |       |
+---+   +---+   +   +---+   +---+---+   +---+   +---+
|   |       |   |       |       |       |       |   |
+   +---+   +   +---+   +---+   +   +---+   +---+   +
|       |           |       |       |       |       |
+---+   +   +---+   +---+   +---+   +---+---+   +---+
|       |   |       |       |       |       |       |
+---+   +---+   +---+   +   +---+---+   +   +---+---+
|   |           |       |       |       |           |
+   +---+   +---+   +---+---+   +---+   +---+---+---+
|       |       |           |       |           |   |
+---+   +---+   +---+---+   +---+   +---+---+   +---+
|           |       |       |       |       |       |
+   +---+   +---+---+   +---+   +---+   +---+---+   +
|   |           |       |       |       |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
This maze is severely disconnected:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| B   B | B   B | C | K   K | H  H  | K   K | I   I |
+---+   +---+   +   +---+   +---+---+   +---+   +---+
| B | B   B | B | C   C | K   K | K   K | I   I | G |
+   +---+   +   +---+   +---+   +   +---+   +---+   +
| B   B | B   B   B | C   C | K   K | I   I | G   G |
+---+   +   +---+   +---+   +---+   +---+---+   +---+
| B   B | B | B   B | C   C | K   K | J   J | G   G |
+---+   +---+   +---+   +   +---+---+   +   +---+---+
| A | B   B   B | C   C | C   C | J   J | J   J   J |
+   +---+   +---+   +---+---+   +---+   +---+---+---+
| A   A | B   B | C   C   C | C   C | J   J   J | F |
+---+   +---+   +---+---+   +---+   +---+---+   +---+
| A   A   A | B   B | C   C | C   C | D   D | J   J |
+   +---+   +---+---+   +---+   +---+   +---+---+   +
| A | A   A   A | C   C | C   C | D   D | E   E | J |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
        12 components!
```

### Example 5b

```
>>> ca = Automaton2({3}, {1,2,3,4,5,6}, 8, 13, bias=0.4)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 191 alive; (maze) 68 passages.
generation 1: (automaton) 253 alive; (maze) 95 passages.
generation 2: (automaton) 273 alive; (maze) 108 passages.
generation 3: (automaton) 275 alive; (maze) 108 passages.
generation 4: (automaton) 277 alive; (maze) 110 passages.
generation 5: (automaton) 278 alive; (maze) 111 passages.
generation 6: (automaton) 279 alive; (maze) 112 passages.
generation 7: (automaton) 280 alive; (maze) 113 passages.
generation 7: stable configuration
Warning: generation 7: stable configuration
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                               |   |   |       |   |
+---+   +---+---+   +---+---+   +   +---+   +   +---+
|   |   |           |   |   |                   |   |
+   +   +   +---+   +   +   +   +---+   +---+   +   +
|   |           |           |           |           |
+   +---+   +   +   +   +   +---+   +   +   +   +---+
|       |   |       |   |           |   |   |   |   |
+   +   +   +   +   +   +---+   +   +---+   +---+---+
|   |   |       |                   |               |
+---+   +---+   +   +---+   +---+   +---+   +---+---+
|       |               |   |           |           |
+   +   +   +   +   +   +   +   +---+   +   +   +   +
|               |   |           |           |   |   |
+   +---+---+---+   +---+   +---+   +---+---+---+   +
|   |           |           |   |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 5c

```
>>> ca = Automaton2({2,3}, {1,2,3,4,5}, 8, 13, bias=0.4)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 195 alive; (maze) 81 passages.
generation 1: (automaton) 307 alive; (maze) 124 passages.
generation 2: (automaton) 195 alive; (maze) 71 passages.
generation 3: (automaton) 257 alive; (maze) 107 passages.
generation 4: (automaton) 255 alive; (maze) 97 passages.
generation 5: (automaton) 261 alive; (maze) 106 passages.
generation 6: (automaton) 252 alive; (maze) 98 passages.
generation 7: (automaton) 256 alive; (maze) 102 passages.
generation 8: (automaton) 258 alive; (maze) 104 passages.
generation 9: (automaton) 257 alive; (maze) 103 passages.
generation 9: stable configuration
Warning: generation 9: stable configuration
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |               |       |   |   |   |           |
+   +---+---+   +   +---+   +   +   +   +   +---+---+
|       |       |           |       |       |       |
+---+   +---+---+   +   +---+   +   +---+---+   +   +
|   |               |   |       |       |       |   |
+   +---+---+   +---+   +   +   +---+   +   +---+   +
|           |           |   |       |           |   |
+---+   +   +---+   +---+   +---+   +---+---+   +---+
|   |   |       |       |       |           |       |
+   +---+   +   +---+---+   +   +---+   +   +---+---+
|           |               |       |       |       |
+   +---+   +---+   +---+---+---+   +---+---+   +   +
|   |               |           |               |   |
+   +---+   +   +---+---+   +   +---+   +---+   +   +
|   |   |   |           |   |       |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

