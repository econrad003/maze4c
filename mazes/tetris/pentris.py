"""
mazes,tetris.pentris - a bag of Pentris tiles
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

NOTES ON ETYMOLOGY

                CARDINAL NUMBERS

    Ancient Greek names for small cardinal numbers:

        εἷς (heîs), μία (mía), ἕν (hén) - one
        δύο (dúo) - two
        τρεῖς (treîs), τρία (tría) - three
        τέσσαρες (téssares), τέσσαρα (téssara) - four
            Attic Greek: τέτταρες (téttares), τέτταρα (téttara)
        πέντε (pénte) - five
        ἕξ (héx) - six
        ἑπτά (heptá) - seven
        ὀκτώ (oktō) - eight
        ἐννέα (ennéa) - nine
        δέκα (déka) - ten
        ἕνδεκα (héndeka) - eleven
        δυώδεκα (duōdeka) - twelve
            Attic Greek: δώδεκα (dōdeka)
        τρεισκαίδεκα (treiskaídeka), τριακαίδεκα (triakaídeka),
            τρισκαίδεκα (triskaídeka) - thirteen
        εἴκοσι (eíkosi) - twenty

            Source: Wiktionary [1] CC-BY SA 4.0

                SOME COGNATES (ENTERTAINMENT)

    From the list, we can see some English words derived from Greek
    words, for example:
        tetrahedron - four-faced polyhedron (from Attic Greek)
        tesseract - four-dimensional generalization of a cube (from Ionic
            Greek)
        pentagon - five-sided polygon
        pentameter - a five-foot line in a poem, for example, in English
            poetry, if the feet consist of two syllables, the first
            unstressed, and the second stressed, the feet are called
            iambs, and we have iambic pentameter, common in Shakespeare:
                "No more; and by a sleep to say we end..." - Hamlet
                  .  /    .    / .    /   .  /   . /
            If we reverse the stress, the feet become trochees, and the
            resulting line is trochaic pentameter, also used in Shakespeare:
                "And my poor fool is hang’d! No, no, no life!" - King Lear
                 /    .   /    .  /   .       /   .   /  .
        tetrameter - a four foot line, common in English hymnody
        trimeter - a three foot line
            Consider the hymn Amazing Grace by John Newton, written in
            what is known as Common Meter (C.M.):
                Amazing grace, how sweet the sound,       A
                That saved a wretch like me.              B
                I once was lost but now I'm found;        A
                Was blind, but now I see.                 B
            The lines marked A are iambic tetrameters, while those marked
            B are iambic trimeter.  An example of another basic form, long
            meter (L.M.) is the hymn Windham by Daniel Read, set to a poem
            by Isaac Watts:
                Broad is the road that leads to death,    A
                And thousands walk to-gether there;       B
                But wisdom shows a narrow path,           A
                With here and there a traveller.          B
            In Windham, all four lines are iambic tetrameters.
        hexagon - six-sided polygon
        hexahedron - six-faced polyhedron, for example, the cube
        heptagon - seven-faced polygon
        decagon - ten-sided polygon
        decameter - ten meters in length; or a ten-foot line in poetry;
            the pronunciation usually differs -- the unit of length is
            commonly pronounced as a trochaic dimeter (dec'a-me'ter),
            whereas the unit of poetry is commonly pronounced as an
            iambic dimeter (dec-a'-me-ter').
        dodecahedron - twelve-faced polyhedron
        triskaidecaphobia - fear of the number thirteen
        icosahedron - twenty-faced polyhedron; the five Platonic solids
            are the regular tetrahedron, the cube, the regular octagon,
            the regular dodecahedron, and the regular icosahedron.  Along
            with the sphere, these are the only perfectly regular solids
            in Euclidean three-dimensional space.

                THE RELEVANT PARTS

    tetris - a game played with tiles consisting of four square cells
            each, with cells connected along their edges. The tiles are
            called tetrominos, as two-celled tiles are known as dominos.
    pentris - the generalization to five-celled tiles.  The tiles are
            called pentominos.

    By extension 6-ominos and 7-ominos could also be called hexominos and
    heptominos, and if they are being dropped as in tetris, the games might
    be referred to as hextrix and heptris. 

DESCRIPTION

    There are a total of 58 distinct configurations if rotations are
    counted separately.  Depending on how you count them, these come
    in either 15 different shapes (ignoring rotation), if you count
    each of the distinct mazes etched into the F and H type tiles
    separately, or just 11 if you ignore the mazes.

    There are a number of alternative methods to select a set of
    pentomino configurations.

USAGE

    To see the selection methods:

        >>> import mazes.tetris.pentris
        >>> mazes.tetris.pentris.__all__
        ('shape_lists', 'select_all', 'sample', 'tee', 'ell', 'squares',
         'stubbies', 'shape_range', 'names')

    We will briefly describe each of these entry points here:

        shape_list - this is a list of the 11 shape lists.  Each shape
            list includes either 2, 4, or 12 different configurations.

        select_all() - this is a method which returns a list which includes
            one copy of each of the 58 configurations

        sample(k:int, fill=False, replace=False) - this is a method which
            returns a sample of at most k configurations of each of the
            11 basic shapes.  The default is to select the sample without
            replacement.  If k>2, then there will be just the two A shape
            configurations, i.e. a 1x5 tile and a 5x1 tile.  If k>4, then
            there will be just four configurations for all shapes except
            A (which only has two), F, and H.  (F and H each have twelve
            distinct configurations.)
                If the 'fill' option is set to true and a shape's configurations
            have been exhausted, then that shape is reset so that more than
            one copy of a configuration is included.
                If the 'replace' option is set to True, the choices are made
            with replacement. This is like rolling a die -- the die may come
            up with the same number more than once.  (Note: replace=True
            implies fill=True.)

        tee() - returns the four J pentomino configurations.  One of these looks
            like a capital T: 
                    ┏━━━┳━━━┳━━━┓
                    ┃           ┃
                    ┗━━━╋   ╋━━━┛
                        ┃   ┃
                        ┣   ┫
                        ┃   ┃
                        ┗━━━┛
            The other three are rotations.

        ell() - returns the I and K pentomino configurations.  One of the I
            pentominos looks like a capital L, and its mirror image can be
            found in the K configurations.
                        (I)                     (K)
                    ┏━━━┓                           ┏━━━┓
                    ┃   ┃                           ┃   ┃
                    ┣   ┫                           ┣   ┫
                    ┃   ┃                           ┃   ┃
                    ┣   ╋━━━┳━━━┓           ┏━━━┳━━━╋   ┫
                    ┃           ┃           ┃           ┃
                    ┗━━━┻━━━┻━━━┛           ┗━━━┻━━━┻━━━┛
            The remaining six ell pentominos are rotations of one or the
            other.

        squares() - twenty-four of the configurations contain a 2x2 square.
            These are the F and the H configurations.  For example here are
            two distinct H pentominos:
                    ┏━━━┳━━━┓               ┏━━━┳━━━┓
                    ┃   ┃   ┃               ┃       ┃
                    ┣   ╋   ╋━━━┓           ┣   ╋━━━╋━━━┓
                    ┃           ┃           ┃           ┃
                    ┗━━━┻━━━┻━━━┛           ┗━━━┻━━━┻━━━┛
            Notice that they both have two rows, three cells below and two
            above, with just one cell in column three.  But notice that the
            placements of walls in the two tiles are not congruent.  Do you
            see that there we can move that moving wall to one more place
            inside the square without disconnecting the maze?  That gives
            three distinct etchings.  There are three more rotations for
            each of the three distinct etchings giving a total of twelve
            distinct H pentominos.  The F pentominos are their mirror images.

        stubbies() - these are the pentominos with exactly four cells either
            in a single row or a single column.  Here is just one example:
                        ┏━━━┓
                        ┃   ┃
                    ┏━━━╋   ╋━━━┳━━━┓
                    ┃               ┃
                    ┗━━━┻━━━┻━━━┻━━━┛
            There are four shapes: B, C, D and E, and four distinct rotations
            for each shape.  This give sixteen different configurations

        def shape_range(*, shortest=0, longest=5) - this method gives a way
            of selecting configurations based on the dimensions of the bounding
            rectangle (or bounding box).  For example, the bounding box for the
            stubbie shown above is:
                    +---┏━━━┓---+---+
                    |   ┃   ┃       |       two rows, four columns
                    ┏━━━╋   ╋━━━┳━━━┓
                    ┃               ┃
                    ┗━━━┻━━━┻━━━┻━━━┛
            If shortest is 0, 1 or 2 and longest is 4, 5 or 6, then all the
            stubbies will be returned in the list.

    For other ways of creating a sample, you can either play with the list
    'shape_lists', or you can import shapes directly, e.g.:

            from mazes.tetris.pentris import sA, sC, sK

    These are lists containing each of the configurations for the given shape.
    The names are sA, sB, sC, and so on through sK.  The list 'shape_lists' is
    here defined as:

            shape_lists = [sA, sB, sC, ..., sK]

    To see this definition in the source code, look two lines above the comment
    line below which contains the phrase "CHOOSE YOUR POISON" in capital letters.

    Most of this module was generated automatically using the following module:
            mazes.tetris.pentris_generator

REFERENCES

    [1] "Appendix: Ancient Greek numerals".  Wiktionary.  31 August
        2026.  Web.  Accessed 3 October 2026.
          URL: https://en.wiktionary.org/wiki/Appendix:Ancient_Greek_numerals

        The page is licensed under the CC BY-SA 4.0.  For license, see:
          URL: https://creativecommons.org/licenses/by-sa/4.0/

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from mazes import rng

# GENERATOR: mazes.tetris.pentris_generator
# BEGIN GENERATED CODE =================================================

n = 5                           # each tile has five cells

    # directions on the 4-connected rectangular grid
S, E, N, W = 'south', 'east', 'north', 'west'

# ---------- SHAPE DEFINITIONS GO HERE ----------

#   base shape:
#           ┏━━━┳━━━┳━━━┳━━━┳━━━┓
#           ┃                   ┃
#           ┗━━━┻━━━┻━━━┻━━━┻━━━┛
sA = list()
sA.append((((0, E, 1), (1, E, 2), (2, E, 3), (3, E, 4)), (1, 5, 0)))
sA.append((((0, N, 1), (1, N, 2), (2, N, 3), (3, N, 4)), (5, 1, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┳━━━┓
#           ┃   ┃ █ ┃ █ ┃ █ ┃
#           ┣   ╋━━━╋━━━╋━━━┫
#           ┃               ┃
#           ┗━━━┻━━━┻━━━┻━━━┛
sB = list()
sB.append((((0, E, 2), (0, N, 1), (2, E, 3), (3, E, 4)), (2, 4, 0)))
sB.append((((0, E, 1), (1, N, 2), (2, N, 3), (3, N, 4)), (4, 2, 0)))
sB.append((((0, N, 1), (1, W, 2), (2, W, 3), (3, W, 4)), (2, 4, 3)))
sB.append((((0, N, 1), (1, N, 2), (2, N, 3), (3, E, 4)), (4, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┳━━━┓
#           ┃ █ ┃   ┃ █ ┃ █ ┃
#           ┣━━━╋   ╋━━━╋━━━┫
#           ┃               ┃
#           ┗━━━┻━━━┻━━━┻━━━┛
sC = list()
sC.append((((0, E, 1), (1, E, 3), (1, N, 2), (3, E, 4)), (2, 4, 0)))
sC.append((((0, N, 1), (1, N, 3), (1, W, 2), (3, N, 4)), (4, 2, 1)))
sC.append((((0, N, 1), (1, E, 4), (1, W, 2), (2, W, 3)), (2, 4, 2)))
sC.append((((0, N, 1), (1, N, 2), (2, E, 4), (2, N, 3)), (4, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┳━━━┓
#           ┃ █ ┃ █ ┃   ┃ █ ┃
#           ┣━━━╋━━━╋   ╋━━━┫
#           ┃               ┃
#           ┗━━━┻━━━┻━━━┻━━━┛
sD = list()
sD.append((((0, E, 1), (1, E, 2), (2, E, 4), (2, N, 3)), (2, 4, 0)))
sD.append((((0, N, 1), (1, N, 2), (2, N, 4), (2, W, 3)), (4, 2, 1)))
sD.append((((0, N, 1), (1, E, 3), (1, W, 2), (3, E, 4)), (2, 4, 1)))
sD.append((((0, N, 1), (1, E, 4), (1, N, 2), (2, N, 3)), (4, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┳━━━┓
#           ┃ █ ┃ █ ┃ █ ┃   ┃
#           ┣━━━╋━━━╋━━━╋   ┫
#           ┃               ┃
#           ┗━━━┻━━━┻━━━┻━━━┛
sE = list()
sE.append((((0, E, 1), (1, E, 2), (2, E, 3), (3, N, 4)), (2, 4, 0)))
sE.append((((0, N, 1), (1, N, 2), (2, N, 3), (3, W, 4)), (4, 2, 1)))
sE.append((((0, N, 1), (1, E, 2), (2, E, 3), (3, E, 4)), (2, 4, 0)))
sE.append((((0, E, 4), (0, N, 1), (1, N, 2), (2, N, 3)), (4, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃ █ ┃   ┃   ┃
#           ┣━━━╋   ╋   ┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sF = list()
sF.append((((0, E, 1), (1, E, 3), (1, N, 2), (3, N, 4)), (2, 3, 0)))
sF.append((((0, N, 1), (1, N, 3), (1, W, 2), (3, W, 4)), (3, 2, 1)))
sF.append((((0, N, 1), (1, E, 2), (2, E, 4), (2, S, 3)), (2, 3, 0)))
sF.append((((0, E, 4), (0, N, 1), (1, E, 3), (1, N, 2)), (3, 2, 0)))
#   move the wall (1):
#           ┏━━━┳━━━┳━━━┓
#           ┃ █ ┃       ┃
#           ┣━━━╋   ╋   ┫
#           ┃       ┃   ┃
#           ┗━━━┻━━━┻━━━┛
sF.append((((0, E, 1), (1, N, 2), (2, E, 3), (3, S, 4)), (2, 3, 0)))
sF.append((((0, N, 1), (1, W, 2), (2, N, 3), (3, E, 4)), (3, 2, 1)))
sF.append((((0, E, 2), (0, N, 1), (2, N, 3), (3, E, 4)), (2, 3, 0)))
sF.append((((0, E, 1), (1, N, 2), (2, W, 3), (3, N, 4)), (3, 2, 0)))
#   move the wall (2):
#           ┏━━━┳━━━┳━━━┓
#           ┃ █ ┃       ┃
#           ┣━━━╋   ╋━━━┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sF.append((((0, E, 1), (1, E, 4), (1, N, 2), (2, E, 3)), (2, 3, 0)))
sF.append((((0, N, 1), (1, N, 4), (1, W, 2), (2, N, 3)), (3, 2, 1)))
sF.append((((0, E, 1), (1, N, 2), (2, E, 4), (2, W, 3)), (2, 3, 0)))
sF.append((((0, N, 1), (1, E, 3), (1, N, 2), (3, S, 4)), (3, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃   ┃ █ ┃   ┃
#           ┣   ╋━━━╋   ┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sG = list()
sG.append((((0, E, 2), (0, N, 1), (2, E, 3), (3, N, 4)), (2, 3, 0)))
sG.append((((0, E, 1), (1, N, 2), (2, N, 3), (3, W, 4)), (3, 2, 0)))
sG.append((((0, N, 1), (1, E, 2), (2, E, 3), (3, S, 4)), (2, 3, 0)))
sG.append((((0, E, 4), (0, N, 1), (1, N, 2), (2, E, 3)), (3, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃   ┃   ┃ █ ┃
#           ┣   ╋   ╋━━━┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sH = list()
sH.append((((0, E, 2), (0, N, 1), (2, E, 4), (2, N, 3)), (2, 3, 0)))
sH.append((((0, E, 1), (1, N, 2), (2, N, 4), (2, W, 3)), (3, 2, 0)))
sH.append((((0, N, 1), (1, E, 3), (1, W, 2), (3, S, 4)), (2, 3, 1)))
sH.append((((0, N, 1), (1, E, 4), (1, N, 2), (2, E, 3)), (3, 2, 0)))
#   move the wall (1):
#           ┏━━━┳━━━┳━━━┓
#           ┃       ┃ █ ┃
#           ┣   ╋   ╋━━━┫
#           ┃   ┃       ┃
#           ┗━━━┻━━━┻━━━┛
sH.append((((0, N, 1), (1, E, 2), (2, S, 3), (3, E, 4)), (2, 3, 0)))
sH.append((((0, E, 4), (0, N, 1), (1, E, 2), (2, N, 3)), (3, 2, 0)))
sH.append((((0, E, 3), (0, N, 1), (1, W, 2), (3, N, 4)), (2, 3, 1)))
sH.append((((0, N, 1), (1, E, 2), (2, N, 3), (3, W, 4)), (3, 2, 0)))
#   move the wall (2):
#           ┏━━━┳━━━┳━━━┓
#           ┃       ┃ █ ┃
#           ┣   ╋━━━╋━━━┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sH.append((((0, E, 3), (0, N, 1), (1, E, 2), (3, E, 4)), (2, 3, 0)))
sH.append((((0, E, 2), (0, N, 1), (2, N, 3), (3, N, 4)), (3, 2, 0)))
sH.append((((0, E, 1), (1, N, 2), (2, W, 3), (3, W, 4)), (2, 3, 1)))
sH.append((((0, N, 1), (1, N, 2), (2, E, 3), (3, S, 4)), (3, 2, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃   ┃ █ ┃ █ ┃
#           ┣   ╋━━━╋━━━┫
#           ┃   ┃ █ ┃ █ ┃
#           ┣   ╋━━━╋━━━┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sI = list()
sI.append((((0, E, 3), (0, N, 1), (1, N, 2), (3, E, 4)), (3, 3, 0)))
sI.append((((0, E, 1), (1, E, 2), (2, N, 3), (3, N, 4)), (3, 3, 0)))
sI.append((((0, N, 1), (1, N, 2), (2, W, 3), (3, W, 4)), (3, 3, 2)))
sI.append((((0, N, 1), (1, N, 2), (2, E, 3), (3, E, 4)), (3, 3, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃ █ ┃   ┃ █ ┃
#           ┣━━━╋   ╋━━━┫
#           ┃ █ ┃   ┃ █ ┃
#           ┣━━━╋   ╋━━━┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sJ = list()
sJ.append((((0, E, 1), (1, E, 4), (1, N, 2), (2, N, 3)), (3, 3, 0)))
sJ.append((((0, N, 1), (1, N, 4), (1, W, 2), (2, W, 3)), (3, 3, 2)))
sJ.append((((0, N, 1), (1, N, 2), (2, E, 4), (2, W, 3)), (3, 3, 1)))
sJ.append((((0, N, 1), (1, E, 3), (1, N, 2), (3, E, 4)), (3, 3, 0)))

#   base shape:
#           ┏━━━┳━━━┳━━━┓
#           ┃ █ ┃ █ ┃   ┃
#           ┣━━━╋━━━╋   ┫
#           ┃ █ ┃ █ ┃   ┃
#           ┣━━━╋━━━╋   ┫
#           ┃           ┃
#           ┗━━━┻━━━┻━━━┛
sK = list()
sK.append((((0, E, 1), (1, E, 2), (2, N, 3), (3, N, 4)), (3, 3, 0)))
sK.append((((0, N, 1), (1, N, 2), (2, W, 3), (3, W, 4)), (3, 3, 2)))
sK.append((((0, N, 1), (1, N, 2), (2, E, 3), (3, E, 4)), (3, 3, 0)))
sK.append((((0, E, 3), (0, N, 1), (1, N, 2), (3, E, 4)), (3, 3, 0)))

# ---------- SHAPE DEFINITIONS END HERE ----------

# ---------- LIST ALL THE SHAPE CLASSES ----------

shape_lists = [sA, sB, sC, sD, sE, sF, sG, sH, sI, sJ, sK]

# ---------- CHOOSE YOUR POISON ----------

# END GENERATED CODE ===================================================

def select_all() -> list:
    """include all the shapes"""
    result = list()
    for shapes in shape_lists:
        for shape in shapes:
            result.append(shape)
    print(f"{len(result)} shapes")
    return result

def sample(k:int, fill=False, replace=False) -> list:
    """choose at most k shapes from each list, without replacement

    If a list contains fewer than k shapes, then some shapes will
    be underrepresented.  If you want a full complement of each
    shape set 'fill' to True.  If you want the choices to be made
    with replacement, set 'replace' to True.  Note that if 'replace'
    is True, the the setting of 'fill' is ignored.  If 'fill' is True
    and 'sample' is False, then duplicates will be kept to a minimum.
    """
    if replace and not fill:
        print("WARNING: 'fill=True' is assumed when 'replace=True'")
    result = list()
    for shapes in shape_lists:
        if replace:
            result.extend(rng.choices(shapes, k=k))
        elif fill:
            h = k
            while len(shapes) <= h:
                result.extend(shapes)
                h -= len(shapes)
            if h > 0:
                result.extend(rng.sample(shapes, h))
        else:                       # both are False
            if k < len(shapes):
                result.extend(rng.sample(shapes, k))
            else:
                result.extend(shapes)
    print(f"{len(result)} shapes")
    return result

def tee():
    """returns the four T shapes"""
    print(f"{len(sJ)} shapes")
    return list(sJ)

def ell():
    """returns the eight L shapes"""
    result = list(sI)
    result.extend(sK)
    print(f"{len(result)} shapes")
    return result

def squares():
    """returns the 24 shapes that contain a 2x2 square"""
    result = list(sF)
    result.extend(sH)
    print(f"{len(result)} shapes")
    return result

def stubbies():
    """returns the 16 shapes with longest size 4"""
    result = list(sB)
    result.extend(sC)
    result.extend(sD)
    result.extend(sE)
    print(f"{len(result)} shapes")
    return result

def shape_range(*, shortest=0, longest=5):
    """selects shapes based on shortest and longest dimension

    The default is to accept all 58 shapes
    """
    if 0 <= shortest <= longest <= 5:
        pass
    else:
        raise ValueError(f"Need 0 <= {shortest=} <= {longest=} <= 5.")
    result = list()
    if longest >= 5:
        result.extend(sA)
    if (shortest < 5) and (longest > 3):
        result.extend(sB)
        result.extend(sC)
        result.extend(sD)
        result.extend(sE)
    if (shortest < 4) and (longest > 2):
        result.extend(sF)
        result.extend(sG)
        result.extend(sH)
    if (shortest < 4) and (longest > 3):
        result.extend(sI)
        result.extend(sJ)
        result.extend(sK)
    print(f"{len(result)} shapes")
    return result

__all__ = ("shape_lists", "select_all", "sample", "tee", "ell",
           "squares", "stubbies", "shape_range")

# END mazes.tetris.pentis
