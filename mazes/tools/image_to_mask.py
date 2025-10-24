"""
mazes.tools.image_to_mask - for converting a PNG image to an image mask
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Convert a PNG image (or other RGB image) to a rectangular image mask.

USAGE

    To create a text mask:

        from mazes.tools.image_to_mask import image_open, image_mask

        filename = "foo.png"            # RGB image file
        start = (3, 3)                  # column, row
        step = (5, 5)                   # colum, row
        minvalues = (50, 50, 50)        # (red, green, blue)

        img = image.open(filename)      # type: PIL.Image
        print("(width, height) =", image.size)
        rows, cols, mask = image_mask(img, start, step, minvalues)

    To create a 0/1 threshold mask:

        from mazes.tools.image_to_mask import image_open, image_threshold_mask

        filename = "foo.png"            # RGB image file
        start = (3, 3)                  # column, row
        step = (5, 5)                   # colum, row
        minvalues = (50, 50, 50)        # (red, green, blue)

        img = image.open(filename)      # type: PIL.Image
        print("(width, height) =", image.size)
        mask = image_threshold_mask(img, start, step, minvalues)
        rows = len(mask)
        cols = len(mask[0])

    See module demos.masked_maze for an example of masking a part of the
    grid before carving.

    Note that the mask will be upside down as it reflects the left-handed
    image coordinates (y-axis from top to bottom) instead of the usual
    right-handed coordinates (y-axis from bottom to top):

        Image Coordinates:              Calculus Class Coordinates

              0                               y
            0 +-------> x                     Λ
              |                               |
              |   Q1                          |   Q1
              |                               |
              V                             0 +--------> x
              y                               0

IMPLEMENTATION NOTES

    The approach here differs from the masking approach in [1].  In [1],
    masks are top down, using a MaskedMaze class.  Our approach is
    bottom-up, with masking implemented directly in the base classes
    Cell and Grid.  (That part of the implementation was set up early
    in development in 2024.)

    The programmer interface is in the Cell class.  Instance methods
    Cell.hide() and Cell.reveal() change the state of a cell to masked
    are unmasked, respectively.  Cell.hidden is a property which returns
    the current state.

    The Grid iterator and the Grid.cells() generator both iterate through the
    unmasked cells.  The Grid._cells() generator iterates through all the
    cells, both masked and unmasked.

    The toolbox in this module consists of several methods which interface
    with the PIL package (aka Python 'pillow'):

        1) image_open - reads an RGB image file into a pillow Image object
        2) image_threshold_mask - uses a pillow Image object to create
           a rectangular 0/1 mask array.  This is just a two-dimension
           list of zeros and ones.
        3) image_mask - uses a pillow Image object to create a string
           array of ' ' and 'X' characters and, as a row separator,
           newline characters which can stored in or read from a text
           file. 

REFERENCES

    [1] Jamis Buck.  "Fitting mazes to shapes", Chapter 6 in Mazes for
        Programmers. Pragmatic Bookshelf, 2015.  Pages 83-96.
"""

from PIL import Image

def image_open(filename:str, debug:bool=False):
    """open the image"""
    if debug:
        print(f"Opening {filename}...", end="")
    image = Image.open(filename)
    if debug:
        width, height = image.size
        print(f" {width}×{height}")
    return image

def pixel_value(image:Image, x:int, y:int, debug:bool=False) -> tuple:
    """Get pixel value"""
    xy = (x, y)
    pixel = image.getpixel(xy)
    if debug:
        print(f"pixel at {xy}:", pixel)
    return pixel

def threshold(pixel:tuple, minvalues:tuple, AND:bool=True) -> (0, 1):
    """threshold filter for a pixel

    The tuple 'minvalues' is an RGB tuple consisting of three integers.
    If the value is positive or zero, it is used as a minimum (or low
    threshold).  If the value is negative, it's absolute value is used
    as a maximum (or high threshold).

    For example, the triple (50, -10, 0) will "accept" an RGB triple
    (R, G, B) if:
        R ≥ 50;
        G ≤ 10; and
        B ≥ 0.

    Note that the color values are integers in the interval [0,255] (i.e.
    Python range(256)).  In the above scenario, the condition B ≥ 0 is
    always satisfied.  The triple (50, -10, 0) is equivalent to R ≥ 50 and
    G ≤ 10

    To change from checking whether all conditions are satisfied (i.e.
    'and-ing') to checking whether at least one condition is satisfied
    (i.e. 'or-ing'), set the option 'AND' to False.

    Note that the condition B ≥ 0 would guarantee acceptance if 'AND'
    were false. To ignore a color (e.g. blue ) when 'AND' is false,
    use the value 256 or float('inf'), e.g. B ≥ 256.  So instead of
    (50, -10, 0), to test whether R ≥ 50 or G ≤ 10, we could use either
    (50, -10, 256).

    If the pixel is accepted, 1 is returned.  If the pixel is rejected,
    0 is returned.
    """
    def test(i) -> bool:
        """check the pixel"""
        px, value = pixel[i], minvalues[i]
        return px >= value if value >= 0 else px <= abs(value)

    if AND:
        return 1 if test(0) and test(1) and test(2) else 0

        # OR
    return 1 if test(0) or test(1) or test(2) else 0

def image_threshold_mask(image:Image, start:tuple, step:tuple,
                         minvalues:tuple, AND:bool=True, debug=False):
    """convert an image to a 0/1 threshold mask"""
    mask = list()
    startx, starty = start
    stepx, stepy = step
    stopx, stopy = image.size
    for y in range(starty, stopy, stepy):
        mask.append(list())
        for x in range(startx, stopx, stepx):
            pixel = pixel_value(image, x, y)
            t = threshold(pixel, minvalues, AND=AND)
            mask[-1].append(t)
    if debug:
        print(f"threshold mask: {len(mask)} rows, {len(mask[0])} columns")
    return mask

def image_mask(image:Image, start:tuple, step:tuple,
               minvalues:tuple, AND:bool=True, debug=False):
    """convert an image to a string mask

    Returns the number of rows, number of columns, and the mask.

    The mask consists of ' ' (for cells that meet the threshold) and 'X'
    for cells below the threshold
    """
    mask = image_threshold_mask(image, start, step, minvalues,
                                AND=AND, debug=debug)
    i = 0
    j = 0
    s = ""
    for row in mask:
        i += 1
        j = 0
        for column in row:
            j += 1
            s += " " if column else "X"
        s += "\n"
    if debug:
        print(f"mask: {i} rows, {j} columns")
    return i, j, s[:-1]

# end mazes.tools.image_to_mask
