# Change Log

## Release 0.11.6-1 - 18 December 2025 (small bug fixes)
1. Borůvka's algorithm: the implementation had the key inequality reversed.  The result: maximum cost instead of minimum cost.  FIXED!
2. Maze and Cell class: unlinking had a few bugs.  FIXED!
3. Kruskal: the wrong queue entry call was used -- as a result, edge weights were ignored.  FIXED!
4. new test module: *tests.minweight1* verifies that Kruskal and Boruvka class now work as intended.  Also, this module uses *maze.unlink\_all()* method, verifying that *Maze.unlink()* and *Cell.\_unlink()* work.

## Release 0.11.6 - December 2025 (Borůvka's algorithm; grids)
1. Borůvka's algorithm - another minimum cost spanning tree algorithm.  Unlike Kruskal and Prim, this algorithm requires the edge costs to be distinct, or, in the presence of equal cost edges, edge traversal must be stable.  If both conditions are violated, the resulting maze may contain circuits. (*Algorithm* class *Boruvka* in module *mazes.Algorithms.boruvka*.)
2. Complete grids K(*n*).  (*Grid* class *Complete* in module *mazes.Grids.complete*.)
3. Complete *k*-partite grids K(*n*₀,*n*₁,...,*nₖ*), with *k*≥2.  (*Grid* class *Partite* in module *mazes.Grids.complete*.)
4. Added property *graphviz_dot* to class *Grid* in module *mazes.Grid*.  It produces a very crude *graphviz* representation.  The output (a string) can be used to produce images with the command-line *graphviz* engines such as *dot*, *fdp*, *neato*, *twopi*, or *circo*.  Quality will vary considerably.  The output can also be used as a representation as a graph (or matroid) of a maze on a grid.  Isolated cells (cells with no incident passages) are normally omitted in this representation.  The output can also be edited to produce fancier image representions.
5. Multilevel grids in module *mazes.Grids.multilevel* (class *Multilevel* and subclass *Multistory*).  Class *Multistory* builds multilevel grids with one basic floorplan while class *Multilevel* admits multiple floorplans.  See the test module *tests.multilevel* for a simple example.

The grids in items (2) and (3) are based on *Kuratowski* graphs and are included mainly for a mix of completeness and a few demonstrations.

## Release 0.11.5 - 8 December 2025 (GraphViz drivers)
Two graphViz drivers and a lot of documentation.

## Release 0.11.4 - 6 December 2025 (binary trees)
1. A quasi-Kruskal binary tree carving algorithm. See module *mazes/Algorithms/binary_kruskal*, class *BinaryKruskal*.  As with the binary growing tree algorithms in release 0.11.3, trees  of other "airities" can be specified.  And as in the binary growing trees, the algorithm sometimes fails, ending with a forest instead of a tree.
2. Documentation is in section 4 of *doc/Algorithms.binary\_growing\_tree.py*.
3. A small amount of refactoring was done to make the module in (1) do almost all of its work inside the *Kruskal* class.

## Release 0.11.3 - 3-4 December 2025 (binary growing trees)
1. Binary growing tree (two new modules in *mazes/Algorithms* + documentation + README updates).
2. Statistics for some binary growing tree runs.
3. Some cosmetic fixes (typos, documentation fixes).

An addendum to the documentation mentioned in point 1 (Appendices B and C) was checked in on 4 December 2025 as v0.10.3.  It is really a late addition to v0.11.3.

## Release 0.11.2 - 1 December 2025 (loops & parallel passages)

For theoretical purposes and a cleaner basic interface:

Pseudomazes (mazes with loops), multimazes (mazes with parallel edges) and pseudomultimazes (mazes with loops and parallel edges) are now supported.  For pseudomazes, use class Pseudomaze in module *mazes.Mazes.pseudomaze*.  For multimazes and pseudomultimazes, use class Multimaze in module *mazes.Mazes.multimaze*.  Loops are disabled by default, but can be enabled at any time in either class.  Method *make\_loop()* can be used instead of *link()* to create a loop even if loops are disabled.

The methods *make\_Pseudomaze* and *make\_Multimaze* in these same two modules can be used to turn a class derived from *Maze* into a pseudomaze or multimaze class.

A loop is a circuit which encompasses a single cell.  Loops are potentially annoying, but probably harmless.  A parallel passage is a passage encompassing the same pair of cells as another passage,  (If both passages are directed, they are in the same direction -- oppositely directed passages are "anti-parallel".)  Parallel passages are generally worse than annoying, but they may be useful in some contexts, especially in testing.  Undirected parallel edges form circuits.  (Anti-parallel arcs form directed circuits.)

## Release 0.11.1-1 - 27 November 2025
* Fix handling of corner squares in the projective grid.
* Documentation: projective grid.
* Documentation: (pruning tree) using *BinaryTree* and *PruningTree* to create simple binary trees on the projective grid.

## Release 0.11.1 - 27 November 2025
1. (New module) Pruning tree algorithms (wall building counterparts of growing tree algorithms) - class *PruningTree* in module *mazes.WallBuilders.pruning\_tree*
2. (New modules) A few "new" queuing methods in the *mazes/Queues* folder - median queues, split stacks, split queues.
3. (Documentation) Notices about time inefficiency for the "basic wallbuilder" algorithms.

## Release 0.11.0 - 20 November 2025
<ol>
<li>Circuit location</li>
    <ol type="a">
    <li>module *qs\_circuit\_locator* based on class *GeneralizedQueue* -- defaults to depth-first search for circuit location</li>
    <li>module *dfs_circuit_locator*, rewritten as a wrapper (not a decorator!) for module *qs\_circuit\_locator*, with *circuit* and *label\_circuit* methods</li>
    <li>*bfs_circuit_locator*, a breadth-first search circuit locator.  It is a wrapper module (not a decorator) for module *qs\_circuit\_locator*.  Note that it locates an edge in a circuit, but not the entire circuit.</li>
    <li>*pq_circuit_locator*, a priority queue-based circuit locator.  It is also a wrapper module (not a decorator) for module *qs\_circuit\_locator*.  It likewise locates an edge in a circuit, but not the entire circuit.</li>
    </ol>
<li>basic wall building modules for the above.</li>
<li>some statistics to help evaluate the wall building modules.</li>
</ol>

## Release 0.10.15 - 18 November 2025
1. Circuit location -- finding a circuit in a maze...
2. Basic wall building by breaking circuits...

## Release 0.10.14-2 - 17 November 2025
1. do some statistical analysis of a few mazes generated by cellular automata.

## Release 0.10.14-1 - 14 November 2025
1. animate the cellular automata (*mazes.Graphics.animation2* + two videos).
2. improvements to the animation module (*mazes.Graphics.animation*), also some refactoring for item (1).
3. test modules (*tests.animation*, *tests.animation2*)

## Release 0.10.14 - 11 November 2025
1. dead end tools: *mazes.tools.dead\_ends*
2. *OblongGrid* *str()* method: tag hidden cells
3. First maze-generating cellular automata

## Release 0.10.13 - 9 November 2025
1. New algorithm - wallbuilding recursive division
2. Cosmetic correction to *mazes/WallBuilders/simple_binary_tree.py*

## Release 0.10.12 - 8 November 2025
1. New algorithm - wallbuilding simple binary tree
2. New class - *AlgorithmWB* for wallbuilding algorithms
3. Corrections to animation modules needed for wallbuilding animation

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

