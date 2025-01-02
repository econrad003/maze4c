"""
mazes.tools.coin_tossing - methods that simulate different kinds of coins
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Several methods are implemented here to handle various coin-tossing
    scenarios.  Common to all is a method that returns either True to
    represent a head or False to represent a tail.

    The implemented methods are:

        cointoss(*args, bias=0.5, **kwargs)
            returns a head with Bernoulli probability p=bias

        all_heads(*args, **kwargs)
            always returns a head (True)

        all_tails(*args, **kwargs)
            always returns a tail

        remote_control(*args, f:callable=coin_toss, **kwargs)
            returns f(*args, **kwargs)
            (if f is not specified, the behavior is the same as coin_toss)

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

def cointoss(*args, bias=0.5, **kwargs) -> bool:
    """a Bernoulli trial

    Arguments other than the keyword argument 'bias' are ignored.

    Returns True with probability p=bias.
    """
    return rng.random() < bias

def all_heads(*args, **kwargs) -> bool:
    """a Bernoulli trial with p=1"""
    return True

def all_tails(*args, **kwargs) -> bool:
    """a Bernoulli trial with p=0"""
    return False

def remote_control(*args, f:callable=cointoss, **kwargs) -> bool:
    """a Bernoulli trial with an attachable remote control

    if the keyword argument 'f' is specified, the return value is
        f(*args, **kwargs)
    the default is
        cointoss(*args, **kwargs)
    """
    return f(*args, **kwargs)

# end module mazes.tools.coin_tossing