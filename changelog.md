# Change Log

## Release 0.9.4 - 2 January 2025 - corrections

1. theta maze binary tree and winder algorithms corrections - handling of bias arguments

## Release 0.9.3 - 1 January 2025

1. theta maze winder algorithms (inwinder and outwinder)

## Release 0.9.2 - 31 December 2024

1. simple binary tree for theta mazes

## Release 0.9.1 - 30 December 2024

1. demonstration modules for theta mazes
2. update change log and README

## Release 0.9 - 30 December 2024

1. theta (or polar or circular) mazes

## Release 0.8.2 - 25 December 2024 - quick update

1. add distance color mapping demo *demos.colormap2* and documentation *doc/distance\_colormaps.md*

## Release 0.8.1 - 24 December 2024 - quick update

1. add distance colormap for hunt and kill

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

