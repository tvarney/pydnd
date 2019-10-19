
from dnd import scanner

import typing
if typing.TYPE_CHECKING:
    from typing import Dict, Tuple, Union
    from numbers import Real

MoneyType = typing.Union['Money', 'Real']


def parse_coin_spec(data: str) -> 'Tuple[int, int, int, int]':
    """Parses a string into a set of coin values.

    This function is used by the Money type to parse and initialize a
    Money value from a string. The spec must consist of pairs of values
    where each pair consists of a numeric value and a coin spec. Valid
    coin specs are 'cp', 'sp', 'gp', and 'pp'. The numeric value must
    be the first item of each pair. If any of these constraints are
    violated, a ValueError is raised. A coin spec may be used multiple
    times, but this is not recommended.

    The value returned is not normalized at all - giving this function
    the string "10000 cp" will return (10000, 0, 0, 0).

    :param data: The coin spec to parse.
    :return: A tuple of the form [cp, sp, gp, pp]
    """
    cp, sp, gp, pp = 0, 0, 0, 0
    parsed = 0
    s = scanner.Scanner(data)
    while True:
        value = s.next_int(require_space=False)
        if value is None:
            break
        if value < 0:
            raise ValueError("coin value may not be negative")

        coin = s.next_token()
        if coin is None:
            raise ValueError("value without coin specifier")

        coin = coin.lower()
        if coin == "cp":
            cp += value
        elif coin == "sp":
            sp += value
        elif coin == "gp":
            gp += value
        elif coin == "pp":
            pp += value
        else:
            raise ValueError("unknown coin type '{}'".format(coin))
        parsed += 1

    if parsed == 0:
        raise ValueError("no coins specified in coin spec")

    return cp, sp, gp, pp


class Money(object):
    """Money is the value object for Items.

    Money values on items are split into 4 coin types - pp, gp, sp, and
    cp. These stand for, respectively:
      * platinum pieces
      * gold pieces
      * silver pieces
      * copper pieces

    The Money type ensures that a value is always valid, and always
    normalized - that is, the value for gp, sp, and cp stay under the
    maximal value prior to converting. Money types may not be negative,
    if an operation would set one of the values to be negative, then it
    will 'borrow' from the value higher than it in the hierarchy. If it
    is unable to do that (i.e. the highest value, pp, would be set to a
    negative value), a ValueError is raised.
    """
    def __init__(self, data: 'Union[Dict, str, Real, None]' = None) -> None:
        """Create a Money value with the given data.

        If the data value is a dictionary, it is unpacked as is into
        the resulting Money value. If there are keys in this dictionary
        which are not one of ['cp', 'sp', 'gp', 'pp'], then a KeyError
        is raised.

        If the data value is a numeric type (int or float), then it the
        value is multiplied by 100 and the cp type is set to that
        value, which should cascade the value up into higher types.
        Fractional cp values are truncated, though any negative value
        will result in a ValueError.

        If the data value is a string, that string will be parsed. The
        string must consist of pairs of values followed by a coin type.
        See the parse_coin_spec() function for more information.

        :param data: The data to unpack into a Money value.
        """
        self._cp, self._sp, self._gp, self._pp = 0, 0, 0, 0
        if data is None:
            return

        if type(data) == dict:
            self.pp = int(data.pop('pp', 0))
            self.gp = int(data.pop('gp', 0))
            self.sp = int(data.pop('sp', 0))
            self.cp = int(data.pop('cp', 0))
            if len(data.keys()) > 0:
                raise KeyError("Unknown keyword arguments: {}".format(", ".join(data.keys())))
        elif type(data) == str:
            raise NotImplementedError("Money(str) not implemented")
        elif type(data) == int or type(data) == float:
            if data < 0:
                raise ValueError("Money value may not be negative")
            self.cp = int(data * 100)
        else:
            raise ValueError("Money must be initialized with a dictionary, string, or number")

    @property
    def cp(self) -> int:
        return self._cp

    @cp.setter
    def cp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.sp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._cp = int(100 - remainder)
            else:
                self._cp = 0
            return

        self._cp = int(value)
        if self._cp > 100:
            self.sp += int(self._cp // 100)
            self._cp %= 100

    @property
    def sp(self) -> int:
        return self._sp

    @sp.setter
    def sp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.gp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._sp = int(100 - remainder)
            else:
                self._sp = 0
            return

        self._sp = int(value)
        if self._sp > 100:
            self.gp += int(self._sp // 100)
            self._sp %= 100

    @property
    def gp(self) -> int:
        return self._gp

    @gp.setter
    def gp(self, value: int) -> None:
        if value < 0:
            value = -value
            # Attempt to borrow from the next highest
            self.pp -= (value // 100) + 1
            remainder = value % 100
            if remainder > 0:
                self._gp = int(100 - remainder)
            else:
                self._gp = 0
            return

        self._gp = int(value)
        if self._gp > 100:
            self.pp += int(self._gp // 100)
            self._gp %= 100

    @property
    def pp(self) -> int:
        return self._pp

    @pp.setter
    def pp(self, value: int) -> None:
        if value < 0:
            raise ValueError("money value may not be negative")
        self._pp = int(value)

    @property
    def weight(self) -> float:
        return (self._cp + self._sp + self._gp + self._pp) * 0.02

    def json(self) -> 'Dict':
        """Convert a Money value to a json dict.

        :return: A dict representing the Money value
        """
        d = dict()
        if self._pp != 0:
            d["pp"] = self._pp
        if self._gp != 0:
            d["gp"] = self._gp
        if self._sp != 0:
            d["sp"] = self._sp
        if self._cp != 0:
            d["cp"] = self._cp
        return d

    def __eq__(self, rhs: 'MoneyType') -> bool:
        if type(rhs) is Money:
            return rhs._pp == self._pp and rhs._gp == self._gp and rhs._sp == self._sp and rhs._cp == self._cp
        if type(rhs) is int:
            return float(rhs) == self.__float__()
        if type(rhs) is float:
            return rhs == self.__float__()
        raise ValueError("can not compare Money and {}".format(type(rhs)))

    def __ne__(self, rhs: 'MoneyType') -> bool:
        return not self.__eq__(rhs)

    def __gt__(self, rhs: 'MoneyType') -> bool:
        rtype = type(rhs)
        if rtype is Money or rtype is int or rtype is float:
            return self.__float__() > float(rhs)
        raise ValueError("can not compare Money and {}".format(rtype))

    def __ge__(self, rhs: 'MoneyType') -> bool:
        return self.__eq__(rhs) or self.__gt__(rhs)

    def __lt__(self, rhs: 'MoneyType') -> bool:
        rtype = type(rhs)
        if rtype is Money or rtype is int or rtype is float:
            return self.__float__() < float(rhs)
        raise ValueError("can not compare Money and {}".format(rtype))

    def __le__(self, rhs: 'MoneyType') -> bool:
        return self.__eq__(rhs) or self.__lt__(rhs)

    def __cmp__(self, rhs: 'MoneyType') -> int:
        if self.__eq__(rhs):
            return 0

        if self.__float__() > float(rhs):
            return 1
        return -1

    def __add__(self, rhs: 'Money') -> 'Money':
        return Money({
            'pp': self._pp + rhs._pp,
            'gp': self._gp + rhs._gp,
            'sp': self._sp + rhs._sp,
            'cp': self._cp + rhs._cp,
        })

    def __iadd__(self, rhs: 'Money') -> 'Money':
        self.pp += rhs.pp
        self.gp += rhs.gp
        self.sp += rhs.sp
        self.cp += rhs.cp
        return self

    def __sub__(self, rhs: 'Money') -> 'Money':
        return Money({
            'pp': self._pp - rhs._pp,
            'gp': self._gp - rhs._gp,
            'sp': self._sp - rhs._sp,
            'cp': self._cp - rhs._cp,
        })

    def __isub__(self, rhs: 'Money') -> 'Money':
        self.cp -= rhs.cp
        self.sp -= rhs.sp
        self.gp -= rhs.gp
        self.pp -= rhs.pp
        return self

    def __mul__(self, rhs: 'Real') -> 'Money':
        return Money({
            'pp': self._pp * rhs,
            'gp': self._gp * rhs,
            'sp': self._sp * rhs,
            'cp': self._cp * rhs,
        })

    def __imul__(self, rhs: 'Real') -> 'Money':
        self.pp *= rhs
        self.gp *= rhs
        self.sp *= rhs
        self.cp *= rhs
        return self

    def __rmul__(self, lhs: 'Real') -> 'Money':
        return self.__mul__(lhs)

    def __truediv__(self, rhs: 'Real') -> 'Money':
        return Money({
            'pp': self._pp / rhs,
            'gp': self._gp / rhs,
            'sp': self._sp / rhs,
            'cp': self._cp / rhs,
        })

    def __itruediv__(self, rhs: 'Real') -> 'Money':
        self.pp /= rhs
        self.gp /= rhs
        self.sp /= rhs
        self.cp /= rhs
        return self

    def __floordiv__(self, rhs: 'Real') -> 'Money':
        return Money({
            'pp': self._pp // rhs,
            'gp': self._gp // rhs,
            'sp': self._sp // rhs,
            'cp': self._cp // rhs,
        })

    def __ifloordiv__(self, rhs: 'Real') -> 'Money':
        self.pp //= rhs
        self.gp //= rhs
        self.sp //= rhs
        self.cp //= rhs
        return self

    def __float__(self) -> float:
        return self._cp * 0.01 + self._sp + self._gp * 100 + self._pp * 1000

    def __str__(self):
        parts = list()
        if self._pp != 0:
            parts.append("{} pp".format(self._pp))
        if self._gp != 0:
            parts.append("{} gp".format(self._gp))
        if self._sp != 0:
            parts.append("{} sp".format(self._sp))
        if self._cp != 0:
            parts.append("{} cp".format(self._cp))
        if len(parts) > 0:
            return " ".join(parts)
        return "0 gp"

    def __repr__(self):
        parts = list()
        if self._pp != 0:
            parts.append("pp={}".format(self._pp))
        if self._gp != 0:
            parts.append("gp={}".format(self._gp))
        if self._sp != 0:
            parts.append("sp={}".format(self._sp))
        if self._cp != 0:
            parts.append("cp={}".format(self._cp))
        return "Money({{{}}})".format(", ".join(parts))
