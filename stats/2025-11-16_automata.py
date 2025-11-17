"""
stats.automata - cellular automaton maze statistics
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This program gathers statistics for some maze algorithms that use
    cellular automata.  Wilson's algorithm is used as a baseline.

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

from math import sqrt

import mazes
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Cellular.etc_automaton import Automaton, Automaton2

ROWS, COLS = 25, 25
GENERATIONS = 50
VERBOSE = False
SAMPLE_SIZE = 100

def components(maze:Maze):
    """return a list of components for a maze"""
    unprocessed = list(maze.grid)
    the_components = dict()     # component index -> cells
    cells = dict()              # cell -> component index
    while unprocessed:
        first = unprocessed.pop()
        the_components[first] = [first]
        cells[first] = first
        stack = [iter(first.passages)]
        unvisited = set(unprocessed)
        while stack:            # depth-first search
            curr = stack[-1]
            try:
                cell = next(curr)
                if cell in unvisited:
                    the_components[first].append(cell)
                    cells[cell] = first
                    stack.append(iter(cell.passages))
                    unvisited.remove(cell)
            except StopIteration:
                stack.pop()
        unprocessed = list(unvisited)
    return the_components

def status(maze:Maze, name:str, generations:int=0, stable:int=1, all_die:int=0):
    """information about the run"""
    def is_linked(cell1, cell2, cell3):
        """look for a link"""
        return cell2 and cell3 and cell1.is_linked(cell2) \
            and cell1.is_linked(cell3)
    the_components = components(maze)
    kappa = len(the_components)
    kappa0 = 0
    for index in the_components:
        kappa0 = max(len(the_components[index]), kappa0)
    degseq = {0:0, 1:0, 2:0, 3:0, 4:0}
    turns = 0
    eastbound = 0
    northbound = 0
    for cell in maze.grid:
        degree = len(list(cell.passages))
        degseq[degree] += 1
        if degree == 2:
            if is_linked(cell, cell.east, cell.west):
                eastbound += 1
            elif is_linked(cell, cell.north, cell.south):
                northbound += 1
            else:
                turns += 1
    assert degseq[2] == northbound + eastbound + turns
    sumdeg = sum(degseq[i] for i in degseq)
    wgtsumdeg = sum(degseq[i]*i for i in degseq)
    assert wgtsumdeg == 2 * len(maze)
    assert sumdeg == len(maze.grid)
    return {"name":name, "generations":generations,
            "stable":int(stable), "all die":int(all_die),
            "k":kappa, "e":len(maze), "v":len(maze.grid),
            "largest":kappa0,
            "isolates":degseq[0], "dead_ends":degseq[1],
            "turns":turns, "northbound":northbound, "eastbound":eastbound,
            "degree 3":degseq[3], "degree 4":degseq[4]}

keys = ["generations", "stable", "all die",
        "k", "e", "v", "largest", "isolates", "dead_ends",
        "turns", "northbound", "eastbound", "degree 3", "degree 4"]

def run_wilson():
    """run the baseline algorithm"""
    maze = Maze(OblongGrid(ROWS, COLS))
    Wilson.on(maze)
    return status(maze, "Wilson"), maze

    # prepare the automaton

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

def run_ca1(rules:str, bias_pct:int, border:int, verbose=VERBOSE):
    """run the 6-neighbor automaton"""
    births, deaths = parse(rules)
    name = f"ETC6:{rules} {bias_pct}% {border}"
    ca = Automaton(births, deaths, ROWS, COLS, bias=bias_pct/100, border=border)
    # counts = set()
    # generations = set()
    try:
        stable = False
        all_die = False
        for n in range(GENERATIONS + 1):
            ca.next_generation(verbose=verbose)
    #        new_counts = (ca.living, len(ca.maze))
    #        curr = ca.current_state
    #        if new_counts in counts:
    #            if curr in generations:
    #                stable = True
    #                break
    #            counts.add(new_counts)
    #            generations.append(curr)
    except Warning:
        stable = True
    except StopIteration:
        stable = True
        all_die = True
    return status(ca.maze, name, n, stable, all_die), ca.maze

def run_ca2(rules:str, bias_pct:int, border:int, verbose=VERBOSE):
    """run the 8-neighbor automaton"""
    births, deaths = parse(rules)
    name = f"ETC8:{rules} {bias_pct}% {border}"
    ca = Automaton2(births, deaths, ROWS, COLS, bias=bias_pct/100, border=border)
    # counts = set()
    # generations = set()
    try:
        stable = False
        all_die = False
        for n in range(GENERATIONS + 1):
            ca.next_generation(verbose=verbose)
    #        new_counts = (ca.living, len(ca.maze))
    #        curr = ca.current_state
    #        if new_counts in counts:
    #            if curr in generations:
    #                stable = True
    #                break
    #            counts.add(new_counts)
    #            generations.append(curr)
    except Warning:
        stable = True
    except StopIteration:
        stable = True
        all_die = True
    return status(ca.maze, name, n, stable, all_die), ca.maze

def test1():
    """make sure everything up to here works as advertised"""
    print("Test 1")
    status, _ = run_wilson()
    print(status)
    status, _ = run_ca1("1234/3", 20, 3)
    print(status)
    status, _ = run_ca2("12345/3", 20, 3)
    print(status)

def stats(data:list):
    """mean and standard deviation"""
    # print(data)
    n = len(data)
    sumX = sum(data)
    sumXX = sum(datum**2 for datum in data)
    mean = sumX / n
    meanXX = sumXX / n
    variance = meanXX - mean**2
    return mean, sqrt(variance)

control_tests = list()
control_tests.append([run_wilson])                  # baseline / control
control_tests.append([run_ca1, "23/3", 30, 2])      # Conway lifelike (control)
control_tests.append([run_ca2, "23/3", 30, 2])      # Conway lifelike (control)
control_tests.append([run_ca1, "23/3", 40, 2])      # Conway lifelike (control)
control_tests.append([run_ca2, "23/3", 40, 2])      # Conway lifelike (control)
control_tests.append([run_ca1, "23/3", 30, 3])      # Conway lifelike (control)
control_tests.append([run_ca2, "23/3", 30, 3])      # Conway lifelike (control)


tests = list()
tests.append([run_wilson])                  # baseline / control
tests.append([run_ca1, "23/3", 40, 2])      # Conway lifelike (control)
tests.append([run_ca1, "123/3", 40, 2])
tests.append([run_ca2, "123/3", 40, 2])
tests.append([run_ca1, "1234/3", 40, 2])
tests.append([run_ca2, "1234/3", 40, 2])
tests.append([run_ca1, "12345/3", 40, 2])
tests.append([run_ca2, "12345/3", 40, 2])
tests.append([run_ca1, "2345/3", 40, 2])
tests.append([run_ca2, "2345/3", 40, 2])
tests.append([run_ca1, "1234/23", 40, 2])
tests.append([run_ca2, "1234/23", 40, 2])

def gather(samples:list):
    """calculate mean and standard deviation"""
    n = len(samples)
    name = samples[0]["name"]
    means = list()
    stdevs = list()
    for key in keys:
        mean, stdev = stats(list(s[key] for s in samples))
        means.append(mean)
        stdevs.append(stdev)
    return name, means, stdevs

def test2():
    """make sure everything up to here works as advertised"""
    for test in tests[0:3]:
        f = test[0]
        args = test[1:]
        samples = list()
        for n in range(SAMPLE_SIZE):
            sample, _ = f(*args)
    #        print(sample["name"], n)
            samples.append(sample)
        name, means, stdevs = gather(samples)
        print(name)
        for i in range(len(keys)):
            print(keys[i], means[i], stdevs[i])
        print("-"*72)

def main1():
    """test that things work as advertised"""
    global SAMPLE_SIZE

    SAMPLE_SIZE = 10
    print(f"{SAMPLE_SIZE=}")
    test1()
    print("-"*72)
    test2()

def test3():
    """prepare a test csv"""
        # BUILD THE HEADER
    keys_to_str = ",".join(keys)
    line1 = "algorithm," + keys_to_str
    print(line1)

        # RUN THE TESTS
    for test in control_tests:         # <- some controls
        f = test[0]
        args = test[1:]
        samples = list()
        for n in range(SAMPLE_SIZE):
            sample, maze = f(*args)
            if n == 0:
                print(sample["name"])
                print(maze)
            samples.append(sample)
        name, means, stdevs = gather(samples)
        means_to_str = ",".join(list("%7.2f" % mean for mean in means))
        line1 = name + "," + means_to_str
        print(line1)
        stdevs_to_str = ",".join(list("%7.2f" % stdev for stdev in stdevs))
        line2 = "stdev," + stdevs_to_str
        print(line2)

def main2():
    """test csv"""
        # SO IT RUNS REASONABLY QUICKLY
    global SAMPLE_SIZE, ROWS, COLS

    SAMPLE_SIZE = 10
    ROWS = COLS = 10
    print(f"{SAMPLE_SIZE=}, {ROWS=}, {COLS=}, {GENERATIONS=}")
    test3()

def test4(fp):
    """the experiment"""
        # BUILD THE HEADER
    keys_to_str = ",".join(keys)
    line1 = "algorithm," + keys_to_str
    fp.write(line1 + "\n")
        # RUN THE TESTS
    for test in tests:         # <- some controls
        f = test[0]
        args = test[1:]
        samples = list()
        for n in range(SAMPLE_SIZE):
            sample, maze = f(*args)
            if n == 0:
                print(sample["name"])
            samples.append(sample)
            print(".", flush=True, end="")
        print()
        name, means, stdevs = gather(samples)
        means_to_str = ",".join(list("%7.2f" % mean for mean in means))
        line1 = name + "," + means_to_str
        fp.write(line1 + "\n")
        stdevs_to_str = ",".join(list("%7.2f" % stdev for stdev in stdevs))
        line2 = "stdev," + stdevs_to_str
        fp.write(line2 + "\n")

def main4():
    """the experiment"""
    with open("output.csv", "w") as fp:
        test4(fp)

if __name__ == "__main__":
    main4()

# END stats.automata
