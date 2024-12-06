"""
mazes.tools.flipflop - methods that switch state after each call
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    State switching method.

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

class FlipFlop(object):
    """flip-flop objects"""

    __slots__ = ("__state", "__iftrue", "__iffalse")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, iftrue, iffalse, initialstate:bool=False):
        """constructor

        If initialstate is True, the value sequence is:
            f, t, f, t, ...
        If initialstate is False (default), the value sequence is:
            t, f, t, f, ...
        """
        self.__iftrue = iftrue
        self.__iffalse = iffalse
        self.reset(initialstate)

    def reset(self, initialstate:bool=False):
        """reset

        If initialstate is True, the value sequence is:
            f, t, f, t, ...
        If initialstate is False (default), the value sequence is:
            t, f, t, f, ...
        """
        self.__state = bool(initialstate)

    def value(self, *args, **kwargs):
        """first changes the state, then returns the associated value"""
        self.__state = not self.__state
        return self.__iftrue if self.__state else self.__iffalse

# end module mazes.tools.flipflop