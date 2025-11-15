"""
mazes.tests.animation2 - test the simpler Python turtle animation driver
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a quick and dirty test module.  At some point, it should be
    expanded into a more useful demo.

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
from time import sleep

from mazes.Cellular.etc_automaton import Automaton
from mazes.Graphics.animation2 import SimpleAnimation

RULES = "12345/3"               # a maze-creating automaton
CONWAY_LIFE = "23/3"            # test of parse rules
ROWS, COLS = 10, 10
TARDIS_BLUE = "#003B6F"
KWARGS = {"border":3, "bias":0.3}

    # prepare the automaton

def parse_rules(rules:str) -> tuple:
    """parse a Conway-style rule

    The rule takes the form "D+/D+" where D+ indicates one or more digits.
    The part before the slash is the death rule, that after: the birth rule.
    For example, Conway's Life uses the rule string "23/3".

    Returns the rules as two fsets, birth first, death second.  For
    example, parse_rules("23/3") returns the tuple as ({2,3}, {3})
    """
    items = rules.split("/")            # "23/3" -> ["23", "3"]
    births = set(map(int, list(items[1])))
    deaths = set(map(int, list(items[0])))
    return births, deaths

# print(parse_rules(CONWAY_LIFE))
assert parse_rules(CONWAY_LIFE) == (set([3]), set([2,3]))
BIRTHS, DEATHS = parse_rules(RULES)
print(f"birth rule:, {set(BIRTHS)} (any other, then dead cell remains dead)")
print(f"death rule:, {set(DEATHS)} (any other, then live cell dies)")
print(f"keyword options: {KWARGS}")
ca = Automaton(BIRTHS, DEATHS, ROWS, COLS, **KWARGS)

    # prepare the animation
spider = SimpleAnimation(ca.maze, speed=3, foreground=TARDIS_BLUE, pen_width=4)
spider.title(f"{BIRTHS=}, {DEATHS=}")
spider.set_window_size(400, 400)

    # carve the maze

ca.maze = spider.maze           # wrap the maze
try:
    for n in range(30):
        ca.next_generation()
except Warning:
    print(f"Simulation stopped after {n} generations.")
except StopIteration:
    print(f"No live cells after {n} generations.")

print("Ten second timeout -- set up the video capture:")
for t in range(10, 0, -1):
    print(f"{t=}...")
    sleep(1)

    # animation
print("When maze is complete, click on the screen to exit...")
spider.animate()
print("Bye-bye!")
