"""
demos.dcm_sw_25 - color gradient for a sidewinder tree with 25% bias
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demo produces a distance-colored maze.

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
import os

from matplotlib.colors import to_rgb
from demos.colormap import main as sketch_example
from mazes.Algorithms.sidewinder import Sidewinder

ROWS = 13
COLS = 21
CENTER = 'c'
CARVER = (Sidewinder, (), {"bias":0.25})

HOT = to_rgb("crimson")
COLD = to_rgb("skyblue")
ZERO = to_rgb("goldenrod")

basename = os.path.basename(__file__).split('.')[0]
pathname = "gallery/" + basename + ".png"

spider = sketch_example(ROWS, COLS, HOT, COLD, ZERO, CENTER, CARVER)
spider.title("Sidewinder (25% bias)")
spider.fig.tight_layout()
spider.save_image(filename=pathname)
print(f"saved image to: {pathname}")

# end module demos.dcm_sw_25