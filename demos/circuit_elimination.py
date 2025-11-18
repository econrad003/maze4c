"""
demos.circuit_elimination - using the circuit locator to remove circuits
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Cellular automata methods typically create disconnected mazes with
    circuits.  In this demo, we eliminate the circuits and connect the
    components.

    To remove circuits, we use the circuit locator.

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

def parse(rules:str) -> tuple:
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

def evk(maze):
    """Euler characteristics"""
    e = len(maze)
    v = len(maze.grid)
    k = 0
    unvisited = set(maze.grid)
    components = dict()
    component_of = dict()
    while unvisited:
        rest = list(unvisited)
        start = rest.pop()
        packet = (start, iter(start.passages))
        k += 1
        component = {start}
        component_of[start] = start
        stack = [packet]
        unvisited.remove(start)
        while stack:
            cell, gen = stack[-1]
            try:
                nbr = next(gen)
                if nbr in unvisited:
                    component.add(nbr)
                    component_of[nbr] = start
                    packet = (nbr, iter(nbr.passages))
                    stack.append(packet)
                    unvisited.remove(nbr)
            except StopIteration:
                stack.pop()
        components[start] = component
    return e, v, k, components, component_of

class MazeMaker(object):
    """class to prepare the maze"""

    DESC = "using the circuit locator to remove circuits"

    def __init__(self, args:"Namespace"):
        """constructor"""
        self.verbose = not args.quiet
        self.ca = ca = self.make_maze(args)
        if not args.very_quiet:
            print(f"Starting the cellular automaton ({args.rules})...")
        if self.verbose:
            print(ca.maze)
        try:
            for n in range(51):
                ca.next_generation(verbose=self.verbose)
        except StopIteration:
            if self.verbose:
                print(f"The automation crashed after {n} generations")
        except Warning:
            if self.verbose:
                print(f"The automation was stable after {n} generations")
        if self.verbose:
            print(ca.maze)
        if not args.very_quiet:
            print(f"Cellular automaton complete...")
        e, v, k, components, component_of = evk(ca.maze)
        if not args.very_quiet:
            print(f"{e=}, {v=}, {k=}, {e-v+k=}")
        self.euler = e, v, k
        self.components = components
        self.component_of = component_of
        if not args.very_quiet:
            print(f"Removing circuits...")
        self.remove_circuits()
        if not args.very_quiet:
            print(f"Joining components...")
        self.join_components()

    def make_maze(self, args):
        """create the maze object"""
        from mazes.Cellular.etc_automaton import Automaton, Automaton2

        births, deaths = parse(args.rules)
        types = {"ETC6":Automaton, "ETC8":Automaton2}
        key = args.automaton.upper()
        if key in types:
            AutomatonType = types[key]
        else:
            print("Undefined type key; using 'Automaton'")
            AutomatonType = Automaton
        rows, cols = args.dim
        bias = args.bias/100
        border = args.border
        ca = AutomatonType(births, deaths, rows, cols, bias=bias, border=border)
        return ca

    def remove_circuits(self):
        """run the circuit locator to break circuits"""
        from mazes.Algorithms.dfs_circuit_locator import CircuitFinder

        e, v, k = self.euler
        n = 0
        while e-v+k > 0:
            status = CircuitFinder.on(self.ca.maze)
            if self.verbose:
                print(status)
            cell1, edge, cell2 = status.result
            self.ca.maze.unlink(edge)
            if self.verbose:
                print(self.ca.maze)
            e -= 1
        self.euler = e, v, k
        if self.verbose:
            print(f"{e=}, {v=}, {k=}, {e-v+k=}")

    def join_components(self):
        """join components by adding edges"""
        e, v, k = self.euler
        components = self.components
        component_of = self.component_of
        maze = self.ca.maze
        walls = list()
        for cell in maze.grid:
            for nbr in cell.neighbors:
                if cell.is_linked(nbr):
                    continue
                if component_of[cell] == component_of[nbr]:
                    continue
                packet = cell, nbr
                walls.append(packet)
        while k > 1:
            n = rng.randrange(len(walls))
            cell1, cell2 = walls[n]
            walls[n] = walls[-1]
            walls.pop()
            key1 = component_of[cell1]
            key2 = component_of[cell2]
            if key1 == key2:
                continue
            maze.link(cell1, cell2)
            for cell in components[key2]:
                 components[key1].add(cell)
                 component_of[cell] = key1
            del components[key2]
            k -= 1
            e += 1
            if self.verbose:
                print(maze)
                print(f"linked grid[{cell1.index}]--grid[{cell2.index}]")
                print(f"{e=}, {v=}, {k=}, {e-v+k=}")
        self.euler = e, v, k

def main(argv):
    """main entry point"""
    import argparse

    DESC = "using the circuit locator to remove circuits"
    parser = argparse.ArgumentParser(description=DESC, \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--dim", nargs=2, type=int, \
        metavar=("ROWS", "COLS"), default=(8, 13), \
        help="dimensions of the target maze.")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--very_quiet", action="store_true")
    cell_grp = parser.add_argument_group("Cellular automata", \
        description="identifies the automaton to use to construct" \
        + " the rough version of the maze")
    cell_grp.add_argument("-A", "--automaton", type=str, \
        default="ETC6", metavar="CA", \
        help="one of \"ETC6\" or \"ETC8\".")
    cell_grp.add_argument("-R", "--rules", type=str, \
        default="12345/3", metavar="<digits>/<digits>", \
        help="the death rule and the birth rule.")
    cell_grp.add_argument("-b", "--bias", type=int, default=35, \
        help="the percentage change of birth in the first generation.")
    cell_grp.add_argument("-B", "--border", type=int, default=2, \
        help="the width in cells of the border.")
    
    args = parser.parse_args(argv)
    if args.very_quiet:
        args.quiet = True
    if not args.quiet:
        print(args)
    obj = MazeMaker(args)
    return obj

if __name__ == "__main__":
    import sys
    obj = main(sys.argv[1:])
    print(obj.ca.maze)
    e, v, k = obj.euler
    print(f"Expected: {e=}, {v=}, {k=}, {e-v+k=}")
    e, v, k, _1, _2 = evk(obj.ca.maze)
    print(f"  Actual: {e=}, {v=}, {k=}, {e-v+k=}")
    
# END demos.circuit_elimination
