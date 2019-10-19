#!/usr/bin/python3

import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional


class Parser(object):
    def __init__(self):
        self._data = ""
        self._length = 0
        self._index = 0

    def init(self, data: str):
        self._data = data
        self._length = len(self._data)
        self._index = 0
    
    def skip_whitespace(self) -> None:
        while self._index < self._length:
            if not self._data[self._index].isspace():
                return
            self._index += 1
    
    def number(self) -> int:
        if self._index >= self._length:
            raise ValueError("No more characters to parse")
        ch = self._data[self._index]
        if not ch.isdigit():
            raise ValueError("Invalid character '{}'".format(ch))
        value = int(ch)
        self._index += 1
        while self._index < self._length:
            ch = self._data[self._index]
            if not ch.isdigit():
                return value
            value *= 10
            value += int(ch)
            self._index += 1
        return value
    
    def consume(self, ch: str) -> bool:
        if self._index >= self._length:
            return False
        if self._data[self._index] == ch:
            self._index += 1
            return True
        return False


class RollValue(object):
    def __init__(self, rolls: 'List[int]', dropped_low: 'List[int]', dropped_high: 'List[int]', add: int):
        self._rolls = rolls
        self._dropped_low = dropped_low
        self._dropped_high = dropped_high
        self._add = add
        self._value = sum(self._rolls) + self._add

    def value(self) -> int:
        return self._value

    def rolls(self) -> 'List[int]':
        return self._rolls

    def dropped_low(self) -> 'List[int]':
        return self._dropped_low

    def dropped_high(self) -> 'List[int]':
        return self._dropped_high

    def add(self) -> int:
        return self._add


class Roll(object):
    @staticmethod
    def parse(data: str) -> 'Roll':
        parser = Parser()
        parser.init(data)
        parser.skip_whitespace()
        num = parser.number()
        if not parser.consume('d'):
            raise ValueError("Missing 'd' in roll string")
        sides = parser.number()
        
        kwargs = dict()
        if parser.consume('H'):
            kwargs["drop_highest"] = parser.number()
            if parser.consume('L'):
                kwargs["drop_lowest"] = parser.number()
        elif parser.consume('L'):
            kwargs["drop_lowest"] = parser.number()
            if parser.consume('H'):
                kwargs["drop_highest"] = parser.number()

        if parser.consume('+'):
            kwargs["add"] = parser.number()
        elif parser.consume('-'):
            kwargs["add"] = -parser.number()
        
        return Roll(num, sides, **kwargs)
    
    _DefaultRandom = random.Random()
    
    def __init__(self, num: int, sides: int, **kwargs) -> None:
        if num < 1:
            raise ValueError("Number of rolls must be positive")
        if sides < 2:
            raise ValueError("Number of sides must be more than 1")
        
        self._num = num
        self._sides = sides
        
        self._drop_highest = kwargs.get("drop_highest", 0)
        self._drop_lowest = kwargs.get("drop_lowest", 0)
        
        self._add = kwargs.get("add", 0)
        
        if self._drop_highest < 0:
            raise ValueError("Drop Highest argument must be >= 0")
        if self._drop_highest >= num:
            raise ValueError("Drop Highest argument must be < number of rolls")
        if self._drop_lowest < 0:
            raise ValueError("Drop Lowest argument must be >= 0")
        if self._drop_lowest >= num:
            raise ValueError("Drop Lowest argument must be < number of rolls")
        if self._drop_lowest + self._drop_highest >= num:
            raise ValueError("Can not drop more dice than are rolled")

    def roll(self, rand: 'Optional[random.Random]' = None) -> 'RollValue':
        if rand is None:
            rand = Roll._DefaultRandom
        rolls = [rand.randint(1, self._sides) for _ in range(self._num)]
        if self._drop_lowest > 0 or self._drop_highest > 0:
            rolls.sort()
            keep = rolls[self._drop_lowest:self._num-self._drop_highest]
            lowest = rolls[0:self._drop_lowest] if self._drop_lowest > 0 else list()
            highest = rolls[self._num-self._drop_highest:] if self._drop_highest > 0 else list()
            return RollValue(keep, lowest, highest, self._add)
        return RollValue(rolls, [], [], self._add)

    def __str__(self) -> str:
        value = "{}d{}".format(self._num, self._sides)
        if self._drop_highest > 0:
            value += "H{}".format(self._drop_highest)
        if self._drop_lowest > 0:
            value += "L{}".format(self._drop_lowest)
        if self._add > 0:
            value += "+{}".format(self._add)
        elif self._add < 0:
            value += "-{}".format(self._add)
        return value


if __name__ == "__main__":
    import sys
    _name = sys.argv.pop(0)
    _rolls = list()
    _verbosity = 1
    for arg in sys.argv:
        if arg == "-v" or arg == "--verbose":
            _verbosity = 2
        elif arg == "-q" or arg == "--quite":
            _verbosity = 1
        elif arg == "-h" or arg == "--help":
            print("roll.py [-vqh] [rolls...]\n")
            print("  -h | --help")
            print("      Print this message and exit")
            print("  -q | --quite")
            print("      Don't output the parsed roll string")
            print("  -v | --verbose")
            print("      If the individual dice rolls should be shown")
            sys.exit(1)
        else:
            try:
                _rolls.append(Roll.parse(arg))
            except ValueError as ve:
                _rolls.append((ve, arg))
    
    for _roll in _rolls:
        if type(_roll) is tuple:
            print("Error in {}: {}".format(_roll[1], _roll[0]))
        else:
            if _verbosity == 0:
                print(_roll.roll().value())
            elif _verbosity == 1:
                print("{} = {}".format(_roll, _roll.roll().value()))
            else:
                _result = _roll.roll()
                print("{} = {}".format(_roll, _result.value()))
                print("  values: {}".format(_result.rolls()))
                if len(_result.dropped_low()) > 0:
                    print("  dropped low: {}".format(_result.dropped_low()))
                if len(_result.dropped_high()) > 0:
                    print("  dropped high: {}".format(_result.dropped_high()))
