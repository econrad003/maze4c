# *stats* folder

This folder contains statistics gathering programs.  Some of the output appears in the *csv* folder.

## Degree Sequences - 7 October 2025

In this experiment, the degree sequences and diameters produced by a given algorithm were averaged over 100 runs for each of a number of maze algorithms.  Means and standard deviations were calculated for each algorithm.

Each mazes in the experiment was a perfect maze (*i.e.* a spanning tree) on a 21×34 rectangular grid with Von Neumann neighborhoods (*i.e.* up to 4 neighbors in the principal compass directions - type *OblongGrid(21, 34)).

The pseudorandom number generator used to produce the mazes was the native Python (v3.12) *random* module.  The Mersenne twister implementation reportedly avoids poor distribution in two dimensions.

## Degree Sequences - 8 October 2025

This is a repeat of the 7 October experiment.  In the report, I look for significant changes (more than one standard deviation) in results.

## Fractal Tessellation (4 passes/16×16 mazes) - 9 October 2025

This experiment is similar to the October 7 experiment.  The list of algorithms was reduced, and the maze size was set at 16×16 to accommodate 4 passes of fractal tessellation using the trivial group, the rotation group, and the dihedral group.  The main purpose is to compare fractal tessellation with other algorithms.

## Fractal Tessellation (4 alternating passes/36×36 mazes) - 10 October 2025

Essentially a repeat of the 9 October experiment with on significant change.  Instead of four 2×2 tiling passes, 4 passes with alternating 2×3 and 3x2 tilings were used to create 36×36 fractal mazes.


