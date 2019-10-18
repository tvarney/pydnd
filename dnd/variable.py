
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, List, Optional, Tuple, Union
    VariableCallback = Callable[['Variable', Any, Any, Optional[str]], None]
    VariableListener = Union[VariableCallback, 'Listener']


class Listener(object):
    def update(self, variable: 'Variable', old_value: 'Any', new_value: 'Any', note: 'Optional[str]' = None) -> None:
        raise NotImplementedError()

    def __call__(self, variable: 'Variable', old_value: 'Any', new_value: 'Any', note: 'Optional[str]' = None) -> None:
        self.update(variable, note, old_value, new_value)


class Variable(object):
    def __init__(self, **kwargs):
        self._listeners = list()  # type: List[VariableListener]

        listener = kwargs.pop('listener', None)    # type: Optional[VariableListener]
        listeners = kwargs.pop('listeners', None)  # type: Optional[List[VariableListener]]

        if listener is not None:
            self._listeners.append(listener)
        if listeners is not None:
            self._listeners.extend(listeners)

        extra_keys = kwargs.keys()
        if len(extra_keys) > 0:
            raise KeyError("Unknown keyword arguments: {}".format(",".join(extra_keys)))

    def add_listener(self, listener: 'VariableListener') -> None:
        self._listeners.append(listener)

    def remove_listener(self, listener: 'VariableListener') -> None:
        self._listeners.remove(listener)

    def get_listener(self, index: int) -> 'VariableListener':
        return self._listeners[index]

    def notify(self, old_value: 'Any', new_value: 'Any', note: 'Optional[str]' = None) -> None:
        for listener in self._listeners:
            listener(self, old_value, new_value, note)


class AnyVar(Variable):
    def __init__(self, value: 'Any', **kwargs) -> None:
        Variable.__init__(self, **kwargs)
        self._value = value

    def get(self) -> 'Any':
        return self._value

    def set(self, value: 'Any') -> None:
        old_value, self._value = self._value, value
        self.notify(old_value, value)

    def __add__(self, other: 'Any') -> 'Any':
        return self._value + other

    def __sub__(self, other: 'Any') -> 'Any':
        return self._value - other

    def __mul__(self, other: 'Any') -> 'Any':
        return self._value * other

    def __truediv__(self, other: 'Any') -> 'Any':
        return self._value / other

    def __floordiv__(self, other: 'Any') -> 'Any':
        return self._value // other

    def __mod__(self, other: 'Any') -> 'Any':
        return self._value % other

    def __divmod__(self, other: 'Any') -> 'Tuple[Any, Any]':
        return divmod(self._value, other)

    def __pow__(self, other: 'Any', modulo: 'Any' = None):
        return pow(self._value, other, modulo)

    def __lshift__(self, other: 'Any') -> 'Any':
        return self._value << other

    def __rshift__(self, other: 'Any') -> 'Any':
        return self._value >> other

    def __and__(self, other: 'Any') -> 'Any':
        return self._value & other

    def __xor__(self, other: 'Any') -> 'Any':
        return self._value ^ other

    def __or__(self, other: 'Any') -> 'Any':
        return self._value | other

    def __radd__(self, other: 'Any') -> 'Any':
        return other + self._value

    def __rsub__(self, other: 'Any') -> 'Any':
        return other - self._value

    def __rmul__(self, other: 'Any') -> 'Any':
        return other * self._value

    def __rtruediv__(self, other: 'Any') -> 'Any':
        return other / self._value

    def __rfloordiv__(self, other: 'Any') -> 'Any':
        return other // self._value

    def __rmod__(self, other: 'Any') -> 'Any':
        return other % self._value

    def __rdivmod__(self, other: 'Any') -> 'Any':
        return divmod(other, self._value)

    def __rpow__(self, other: 'Any') -> 'Any':
        return other ** self._value

    def __rlshift__(self, other: 'Any') -> 'Any':
        return other << self._value

    def __rrshift__(self, other: 'Any') -> 'Any':
        return other >> self._value

    def __rand__(self, other: 'Any') -> 'Any':
        return other & self._value

    def __rxor__(self, other: 'Any') -> 'Any':
        return other ^ self._value

    def __ror__(self, other: 'Any') -> 'Any':
        return other | self._value

    def __iadd__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value + other)
        return self

    def __isub__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value - other)
        return self

    def __imul__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value * other)
        return self

    def __itruediv__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value / other)
        return self

    def __ifloordiv__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value // other)
        return self

    def __imod__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value % other)
        return self

    def __ipow__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value ** other)
        return self

    def __ilshift__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value << other)
        return self

    def __irshift__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value >> other)
        return self

    def __iand__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value & other)
        return self

    def __ior__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value | other)
        return self

    def __ixor__(self, other: 'Any') -> 'AnyVar':
        self.set(self._value ^ other)
        return self

    def __neg__(self) -> 'Any':
        return -self._value

    def __pos__(self) -> 'Any':
        return +self._value

    def __abs__(self) -> 'Any':
        return abs(self._value)

    def __invert__(self) -> 'Any':
        return ~self._value

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return "AnyVar({})".format(repr(self._value))


class IntVar(AnyVar):
    def __init__(self, value: int, **kwargs) -> None:
        AnyVar.__init__(self, value, **kwargs)

    def get(self) -> int:
        return self._value

    def set(self, value: int) -> None:
        old_value, self._value = self._value, int(value)
        self.notify(old_value, value)

    def __neg__(self) -> int:
        return -self._value

    def __pos__(self) -> int:
        return +self._value

    def __abs__(self) -> int:
        return abs(self._value)

    def __invert__(self) -> int:
        return ~self._value

    def __int__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return "IntVar({})".format(repr(self._value))


class FloatVar(AnyVar):
    def __init__(self, value: float, **kwargs) -> None:
        AnyVar.__init__(self, value, **kwargs)

    def get(self) -> float:
        return self._value

    def set(self, value: float) -> None:
        old_value, self._value = self._value, float(value)
        self.notify(old_value, value)

    def __neg__(self) -> float:
        return -self._value

    def __pos__(self) -> float:
        return +self._value

    def __abs__(self) -> float:
        return abs(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __repr__(self) -> str:
        return "FloatVar({})".format(repr(self._value))


class StrVar(AnyVar):
    def __init__(self, value: str, **kwargs) -> None:
        AnyVar.__init__(self, value, **kwargs)

    def get(self) -> str:
        return self._value

    def set(self, value: str) -> None:
        old_value, self._value = self._value, str(value)
        self.notify(old_value, value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    def __repr__(self) -> str:
        return "StrVar({})".format(repr(self._value))


class Attribute(Variable):
    def __init__(self, level: int = 10, **kwargs):
        self._level = level
        self._racial = int(kwargs.pop('racial', 0))
        self._enhance = int(kwargs.pop('enhance', 0))
        self._spell = int(kwargs.pop('spell', 0))
        Variable.__init__(self, **kwargs)

    def level(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._level = self._level, new_value
            self.notify(old_val, self._level, "level")
        return self._level

    def racial(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._racial = self._racial, new_value
            self.notify(old_val, self._racial, "racial")
        return self._racial

    def enhancement(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._enhance = self._enhance, new_value
            self.notify(old_val, self._enhance, "enhancement")
        return self._enhance

    def spell(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._spell = self._spell, new_value
            self.notify(old_val, self._spell, "spell")
        return self._spell

    def current(self) -> int:
        return self._level + self._racial + self._enhance + self._spell

    def mod(self) -> int:
        return (self.current() // 2) - 5

    def inc_level(self, amount: int = 1) -> int:
        return self.level(self._level + amount)

    def dec_level(self, amount: int = 1) -> int:
        return self.level(self._level - amount)

    def inc_enhancement(self, amount: int = 1) -> int:
        return self.enhancement(self._enhance + amount)

    def dec_enhancement(self, amount: int = 1) -> int:
        return self.enhancement(self._enhance - amount)

    def inc_spell(self, amount: int = 1) -> int:
        return self.spell(self._spell + amount)

    def dec_spell(self, amount: int = 1) -> int:
        return self.spell(self._spell - amount)

    def __iadd__(self, other: 'Any') -> 'Attribute':
        self.level(self._level + other)
        return self

    def __isub__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level - other))
        return self

    def __imul__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level * other))
        return self

    def __itruediv__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level / other))
        return self

    def __ifloordiv__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level // other))
        return self

    def __imod__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level % other))
        return self

    def __ipow__(self, other: 'Any', modulo: 'Any') -> 'Attribute':
        self.level(int(pow(self._level, other, modulo)))
        return self

    def __ilshift__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level << other))
        return self

    def __irshift__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level >> other))
        return self

    def __iand__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level & other))
        return self

    def __ixor__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level ^ other))
        return self

    def __ior__(self, other: 'Any') -> 'Attribute':
        self.level(int(self._level | other))
        return self

    def __neg__(self) -> int:
        return -self.current()

    def __pos__(self) -> int:
        return +self.current()

    def __abs__(self) -> int:
        return abs(self.current())

    def __invert__(self) -> int:
        return ~self.current()

    def __int__(self) -> int:
        return int(self.current())

    def __float__(self) -> float:
        return float(self.current())

    def __str__(self) -> str:
        return "{} [{}]".format(self.current(), self.mod())

    def __repr__(self) -> str:
        parts = [str(self._level)]
        if self._racial != 0:
            parts.append('racial={}'.format(self._racial))
        if self._enhance != 0:
            parts.append("enhance={}".format(self._enhance))
        if self._spell != 0:
            parts.append("spell={}".format(self._spell))
        return "Attribute({})".format(", ".join(parts))


class Points(Variable):
    def __init__(self, max_value: int, **kwargs):
        self._max = max_value
        self._current = int(kwargs.pop('current', max_value))  # type: int
        self._temp = int(kwargs.pop('temp', 0))  # type: int
        Variable.__init__(self, **kwargs)

    def max(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._max = self._max, int(new_value)
            self.notify(old_val, self._max, "max")
        return self._max

    def current(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._current = self._current, int(new_value)
            self.notify(old_val, self._current, "current")
        return self._current

    def temp(self, new_value: 'Optional[int]' = None) -> int:
        if new_value is not None:
            old_val, self._temp = self._temp, int(new_value)
            self.notify(old_val, self._temp, "temp")
        return self._temp

    def value(self) -> int:
        return self._current + self._temp

    def inc_max(self, amount: int = 1) -> int:
        old_val, self._max = self._max, int(self._max + amount)
        self._current += amount
        self.notify(old_val, self._max, "max,current")
        return self._max

    def dec_max(self, amount: int) -> int:
        return self.inc_max(-amount)

    def inc_current(self, amount: int = 1) -> int:
        old_val, self._current = self._current, min(int(self._current + amount), self._max)
        if old_val != self._current:
            self.notify(old_val, self._current, "current")
        return self._current

    def dec_current(self, amount: int = 1) -> int:
        return self.inc_current(-amount)

    def inc_temp(self, amount: int = 1) -> int:
        old_val, self._temp = self._temp, int(self._temp + amount)
        self.notify(old_val, self._current)
        return self._temp

    def __str__(self) -> str:
        return "{}/{}".format(self.value(), self._max)

    def __repr__(self) -> str:
        parts = [repr(self._max)]
        if self._current != self._max:
            parts.append("current={}".format(repr(self._current)))
        if self._temp != 0:
            parts.append("temp={}".format(repr(self._temp)))
        return "Points({})".format(", ".join(parts))

