# *stats* folder

This folder contains statistics gathering programs.  Some of the output appears in the *csv* folder.

## Degree Sequences - 7 October 2025

In this experiment, the degree sequences and diameters produced by a given algorithm were averaged over 100 runs for each of a number of maze algorithms.  Means and standard deviations were calculated for each algorithm.

Each mazes in the experiment was a perfect maze (*i.e.* a spanning tree) on a 21×34 rectangular grid with Von Neumann neighborhoods (*i.e.* up to 4 neighbors in the principal compass directions - type *OblongGrid(21, 34)).

The pseudorandom number generator used to produce the mazes was the native Python (v3.12) *random* module.  The Mersenne twister implementation reportedly avoids poor distribution in two dimensions.
