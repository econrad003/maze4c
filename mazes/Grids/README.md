# The mazes/Grids modules

## Grids

1. *oblong.py* - class *OblongGrid* - 4-connected rectangular grid (or Von Neumann neighborhood grid)
2. *oblong6.py* - class *HexagonalGrid* - 6-connected rectangular grid
3. *oblong.py* - class *MooreGrid* - 8-connected rectangular grid (or Moore neighborhood grid)
4. *polar.py* - class *ThetaGrid* - polar grid
5. *cylinder.py* - class *CylinderGrid* - cylindrical grid obtained by identifying one pair of opposite side of a rectangle with no twisting
6. *moebius.py* - class *MoebiusGrid* - Möbius strip grid obtained by identifying one pair opposite sides of a rectangle with a half twist
7. *torus.py* - class *TorusGrid* - toroidal (*i.e.*: like the surface of a donut or a bagel) grid obtained by identifying each pair of opposite sides of a rectangle with no twisting
8. *klein.py* - class *KleinGrid* - Klein bottle grid obtained by identifying each pair of opposite sides of a rectangle, one pair with a half twist, the other without twisting
9. *projective.py* - class *ProjectiveGrid* - real projective planar grid obtained by identifying each pair of opposite sides of a rectangle with a half twist
10. *upsilon.py* - class *UpsilonGrid* - a rectangular grid consisting of cells which alternate between Von Neuman (S/E/N/W) and Moore (8 compass directions) neighborhoods

## Grid support

1. *oblong\_rings.py* - class *ConcentricOblongs* - for working with  rectangular grids in concentric rectangular rings, somewhat analogous to the concentric circular rings (or annular rings) in polar coordinates.  This approach leads to some interesting analogues of sidewinder and Eller's algorithm, and perhaps other algorithms that are designed for class *OblongGrid* above. (See notes 1 and 2 below.)

## NOTES

1. Inspired by a note in the Jamis Buck book, I wrote a program implementing an analogue of sidewinder for polar mazes back in 2015.  Years later, in 2024, I implemented an analogue of Eller's algorithm for the polar grid.
2. *oblong\_rings,py* - Iterating through the cells of a rectangular grid in concentric rectangles instead of by row or by column does not seem to appear in the Jamis Buck book.  The idea came to me in 2024 as I was thinking about polar mazes and their concentric rings of cells.  (See note 1 above.)  I realized that the techniques could be adapted to the humble rectangular grid.  The results were analogues of sidewinder and Eller's algorithm for the rectangular grid which use concentric rectangles.