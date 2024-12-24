# Change Log

## Release 0.8 - 23 December 2024

### Corrections

1. Outward Eller - two lines were added to fix an error which affects grids whose smaller dimension is odd.  Grids whose smaller dimension is even are not affected by the error or the fix.

### Graphics

1. Added fill coloring to Graphics.oblong1
2. Added distance colormaps - see *gallery/dcm_\*.png* for many colormaps... demo modules in *demos/dcm\*.py*

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

