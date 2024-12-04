# Documentation for package *mazes*

Unless otherwise noted, all modules are written in Python 3.

## Package folders

* *mazes* - the package.  This folder contains modules which define the base classes.  In addition, it contains two files, *\_\_init\_\_.py* and *\_\_main\_\_.py*.  The first of these makes the *mazes* folder a package.  It also loads certain frequently used modules and classes. The second is a module main program.  It currently does nothing.

### Subfolders

* *mazes/Algorithms* - contains modules which implement various algorithms, especially algorithms that create mazes.

* *mazes/AGT* - contains modules that make use of the arc-based growing tree algorithm (class *ArcGrowingTree*) implemented in *mazes/Algorithms/growing\_tree2.py*.

* *mazes/Grids* - contains modules that either define grid classes or define special methods for accessing grids.

* *mazes/Graphics* - contains drivers for creating graphical representations of mazes

* *mazes/Queues* - contains modules that define queuing classes for the growing tree and other algorithms

* *mazes/VGT* - contains modules that make use of the cell-based growing tree algorithm (class *VertexGrowingTree*) implemented in *mazes/Algorithms/growing\_tree1.py*.

## Folders containing other modules

* *demos* - modules used both for testing and demonstration

* *tests* - modules used primarily or exclusively for testing

## Other folders

*doc* - documentation - the current plan is to use markdown files (extension: .md).

*gallery* - some sample output - main images in portable network graphics files (extension: .png).

