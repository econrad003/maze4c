# Change Log

## Release 0.10.11-2 - 8 November 2025
1. Animations for outward Eller and recursive division.

## Release 0.10.11 - 7 November 2025
1. More video capture animations (in the *movies* folder: binary tree, sidewinder, Eller, simplified Prim, and DFS with no shuffling).  These are documented in *doc/animation.md*.
2. *mazes.Algorithms.sidewinder* - correct a docstring
3. *mazes.Algorithms.simple\_binary\_tree* - add a *randomize* option to shuffle the grid: this makes a better animation to illustrate the cell-independence of the algorithm.

## Release 0.10.10 - 3 November 2025
1. Update README.
2. Cosmetic changes and minor corrections. (*demos.watershed\_partial*)
3. New demos.  (*demos.basin\_maze* - carve mazes in the basins)
4. Animations. (documentation: *doc/animation.md; modules: *mazes.Graphics.animate*, *mazes.animated\_maze*; new folder: *movies*)
5. Some updates needed for animations (modules: *mazes.maze*)

For (4), passage carving has been tested.  Wall building needs to be tested.  Some additional updates are needed to allow other kinds of visits to figure into the animations,

## Release 0.10.9 part 5 - 3 November 2025 - updates to watershed division documentation
* This is the last part of v0.10.9

## Release 0.10.9 part 4 - 2 November 2025 - updates to watershed documentation

## Release 0.10.9 part 3 - 2 November 2025 - updates to *maze\_group* module
* more algorithms in *mazes/misc/maze\_group* module.
* changelog and README.

## Release 0.10.9 part 2 - 1 November 2025 - add miscellaneous directory
* one module builds almost everything (*mazes/misc/maze\_group*).
* some statistics for twistiness and directness.

## Release 0.10.9 part 1 - 25 October 2025 - cosmetic correction
* changed class Phocidae (unintentionally named after a family of seals) to class Pholcidae (named after the arachnid family which includes the daddy long legs spider, as intended).

## Release 0.10.8 part 2 - masked mazes
1. corrections (cell module, Moore grid module)
2. new tool (image to mask - for creating masks from images)
3. demos and documentation

The infrastructure for masking was built into the cell and grid modules back in 2024.  Text and image masks are new.

## Release 0.10.8 part 1 - 9-10 October 2025 - statistics, rotation group
1. More statistical analyses
2. Rotation group module (for fractal tessellation)

## Release 0.10.7 - 9 October 2025 - more statistics
* minor additions to the stats folder and a new csv.

## Release 0.10.6 - 8 October 2025 - minor fixes / statistics

1. New folders: *stats* and *csv* - statistical experiments
2. New algorithm: multiple seed random walk, a generalization of the Aldous/Broder first entrance random walk (no the mazes are not uniform).  Module *mazes.Algorithms.mt\_random\_walk*.  Colormap demo module: *demos.dcm\_mt\_random\_walk*  Gallery image: *gallery/mt\_random\_walk.png*
3. Minor module fixes: *mazes.tournament*, *mazes.round\_robin*
4. Cosmetic module fix: *mazes.Algorithms.outward\_eller*
5. Statistical experiments: 7 October 2025.  See the *stats* and *csv* folders.  22 algorithms run 100 times each, extracting some summary statistics.

## Release 0.10.5 - 5 October 2025 - Moore grid graphics / save / load

1. Spider graphics for the Moore grid (neighbors in the corners as well as the sides of the square cell) - see the *Graphics.moore* module's *Huntsman* class.
2. Save maze passages to a CSV file - see the *save\_maze* module.
3. Load maze passages from a CSV file - see the *load\_maze* module.
4. Documentation for the above, along with a demo for #1 and a test module for #2 and #3.
5. Gallery images to go with the documentation of #1.

## Release 0.10.4 - 1 October 2025 - Growing forest algorithms

1. New module *mazes.tournament* for task management.
2. New module *mazes.round_robin* for task management.
3. New module *mazes.Algorithms.dff* for depth-first forest maze carving (*aka* recursive backtracking with parallel seeds).

## Release 0.10.3 - 26 September 2026 - Tessellation

1. New module *Algorithms.dihedral* for generating certain dihedral group orbits.
2.  New module *Algorithms.fractal\_tess* for generating fractal mazes (and other mazes) by tessellation of tiles which are themselves mazes.  It works with classes *OblongGrid* and (with a small tweak *MooreGrid*.

## Release 0.10.2 - 24 August 2025

1. New module *console\_tools* - display rectangular mazes with Unicode block characters using method *unicode\_str*.
2. See *doc/console\_tools.md* for details.
3. Corrections and enhancements to the watershed recursive division algorithm.
4. New grids: torus, cylinder, Moebius strip, projective plane, Klein bottle.  (These *might* require some graphical enhancements)
5. New grids: Moore grid, upsilon grid, 6-connected, 8-connected.  (These *will* need some graphical support.)

## Release 0.10.1 - 17 August 2025

1. New data structure - *Watershed* in *mazes.watershed*
2. New algorithm - watershed recursive division in module *watershed\_division* in the *mazes.Algorithms* folder, a passage carver
3. Corrections and additions to the recursive division
4. Documentation for the above

## Release 0.10.0 - 12 August 2025

1. New algorithm - recursive division (as a passage carver)

## Release 0.9.5 - 25 July 2025

1. Added polar versions of Eller's algorithm.

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

