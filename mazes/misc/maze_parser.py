"""
mazes.misc.maze_parser.py - argument parser for maze makers
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides a parser for maze making.

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
import argparse

class MazeParser(object):
    """
    a parser dedicated to making mazes
    """

    __slots__ = ("__parser", "__groups", "__state")

    def __init__(self, description, epilog):
        """constructor"""
        self.__parser = argparse.ArgumentParser(description=description,
                                                epilog=epilog)
        self.__groups = dict()
        self.__state = dict()

    @property
    def parser(self) -> "ArgumentParser":
        """parser getter"""
        return self.__parser

    @property
    def groups(self) -> dict:
        """groups getter"""
        return self.__groups

    @property
    def state(self) -> dict:
        """state getter"""
        return self.__state

# end module mazes.misc.maze_parser
