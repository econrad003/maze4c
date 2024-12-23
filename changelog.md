# Change Log

## Release 0.7 - 22 December 2024

### New algorithms

1.  Unbiased algorithms (Aldous/Broder, reverse Aldous/Broder, Wilson)
2.  Houston's algorithm (a hybrid that starts as in Aldous/Broder and finishes as in Wilson)
3.  Hunt and kill

### Documentation

1.  *unbiased.md* - documents the three unbiased maze carvers (Aldous/Broder, reverse Aldous/Broder. Wilson) and the hybrid (Houston) which might be biased.
2.  *dijkstra.md* - add longest path examples for outward Eller and th e four algorithms documented in point 1.
3.   *hunt\_kill.md* - documentation for hunt and kill.

## Release 0.6 - 19 December 2024

### New algorithms

1.  Dijkstra's shortest path algorithm
2.  Eller's algorithm
3.  Outward Eller's - working in rings from the center out using Eller's algorithm.

## Release 0.5 - 12 December 2024

### New algorithms

1.  Kruskal's algorithm
2.  Outwinder

See folder doc/algorithms for documentation.

## New modules

1.  mazes.components - connected component management
2.  mazes.tools.automaton1 - a simple cellular automaton
3.  tests.components - for checking mazes.components

## Minor and cosmetic changes

typos, docstring corrections, etc.

## Other changes

Removed all through 0.2 from this changelog.

## Release 0.4 - 9 December 2024

I've started using *git* for updates.  Since 0.3, I've been organizing and reorganizing documentation.

Apart from getting the documentation organized and written, there is one update.  Module *VGT.vprim* now supports the *cache* option.  If you don't want the priority queue to create vertex weights on the fly, you can specify *cache=False*.  This is covered in the *doc/Algorithms/growing\_trees1.md* documentation.  In the next update, I will start removing some of the older entries in the changelog.

