#!/usr/bin/python3

import random

import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional


class Parser(object):
    def __init__(self):
        self._valuestring = ""
        self._length = 0
        self._index = 0

    def init(self, valuestring: str):
        self._valuestring = valuestring
        self._length = len(self._valuestring)
        self._index = 0
    
    def skip_whitespace(self) -> None:
        while self._index < self._length:
            if not self._valuestring[self._index].isspace():
                return
            self._index += 1
    
    def number(self) -> int:
        if self._index >= self._length:
            raise ValueError("No more characters to parse")
        ch = self._valuestring[self._index]
        if not ch.isdigit():
            raise ValueError("Invalid character '{}'".format(ch))
        value = int(ch)
        self._index += 1
        while self._index < self._length:
            ch = self._valuestring[self._index]
            if not ch.isdigit():
                return value
            value *= 10
            value += int(ch)
            self._index += 1
        return value
    
    def consume(self, ch: str) -> bool:
        if self._index >= self._length:
            return False
        if self._valuestring[self._index] == ch:
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
    def parse(rollstring: str) -> 'Roll':
        parser = Parser()
        parser.init(rollstring)
        parser.skip_whitespace()
        num = parser.number()
        if not parser.consume('d'):
            raise ValueError("Missing 'd' in rollstring")
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
        rolls = [rand.randint(1, self._sides) for i in range(self._num)]
        if self._drop_lowest > 0 or self._drop_highest > 0:
            rolls.sort()
            vrolls = rolls[self._drop_lowest:self._num-self._drop_highest]
            lowest = rolls[0:self._drop_lowest] if self._drop_lowest > 0 else list()
            highest = rolls[self._num-self._drop_highest:] if self._drop_highest > 0 else list()
            return RollValue(vrolls, lowest, highest, self._add)
        return RollValue(rolls, [], [], self._add)
    
    def __str__(self) -> str:
        strval = "{}d{}".format(self._num, self._sides)
        if self._drop_highest > 0:
            strval += "H{}".format(self._drop_highest)
        if self._drop_lowest > 0:
            strval += "L{}".format(self._drop_lowest)
        if self._add > 0:
            strval += "+{}".format(self._add)
        elif self._add < 0:
            strval += "-{}".format(self._add)
        return strval


if __name__ == "__main__":
    import sys
    progname = sys.argv.pop(0)
    rolls = list()
    verbosity = 1
    for arg in sys.argv:
        if arg == "-v" or arg == "--verbose":
            verbosity = 2
        elif arg == "-q" or arg == "--quite":
            verbosity = 1
        elif arg == "-h" or arg == "--help":
            print("roll.py [-vqh] [rollstrings...]\n")
            print("  -h | --help")
            print("      Print this message and exit")
            print("  -q | --quite")
            print("      Don't output the parsed roll string")
            print("  -v | --verbose")
            print("      If the individual dice rolls should be shown")
            sys.exit(1)
        else:
            try:
                rolls.append(Roll.parse(arg))
            except ValueError as ve:
                rolls.append((ve, arg))
    
    for roll in rolls:
        if type(roll) is tuple:
            print("Error in {}: {}".format(roll[1], roll[0]))
        else:
            if verbosity == 0:
                print(roll.roll().value())
            elif verbosity == 1:
                print("{} = {}".format(roll, roll.roll().value()))
            else:
                rval = roll.roll()
                print("{} = {}".format(roll, rval.value()))
                print("  values: {}".format(rval.rolls()))
                if len(rval.dropped_low()) > 0:
                    print("  dropped low: {}".format(rval.dropped_low()))
                if len(rval.dropped_high()) > 0:
                    print("  dropped high: {}".format(rval.dropped_high()))

