
import dnd.variable as _v

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Dict, List, Union, Optional
    from dnd.variable import Attribute, Points, StrVar, IntVar


class Race(object):
    def __init__(self, name, **kwargs) -> None:
        self._name = name

        self.any_bonus = int(kwargs.get("any", 0))
        self.str_bonus = int(kwargs.get("strength", 0))
        self.dex_bonus = int(kwargs.get("dexterity", 0))
        self.con_bonus = int(kwargs.get("constitution", 0))
        self.int_bonus = int(kwargs.get("intelligence", 0))
        self.wis_bonus = int(kwargs.get("wisdom", 0))
        self.cha_bonus = int(kwargs.get("charisma", 0))

        self.speed = int(kwargs.get("speed", 30))
        self.perks = list(kwargs.get("perks", list()))


class Actor(object):
    def __init__(self, **kwargs) -> None:
        self._pass_through = lambda a, o, n, m=None: self.notify()

        self._name = _v.StrVar(kwargs.get("name", ""), listener=self._pass_through)  # type: StrVar
        self._race = kwargs.get("race", None)  # type: Race
        self._init_mod = int(kwargs.get("init_mod", 0))  # type: int
        self._init_roll = 0  # type: int
        self._max_dex_mod = int(kwargs.get("max_dex_mod", 0))  # type: int
        self._speed = _v.IntVar(30 if self._race is None else self._race.speed)  # type: IntVar

        # An object that we notify whenever we update things that aren't already attached
        self._listeners = list()  # type: List[Callable[['Actor'], None]]
        
        self._armor = None

        self._attributes = {
            'hp': _v.Points(10, listener=self._pass_through),
            'mp': _v.Points(10, listener=self._pass_through),

            'str': _v.Attribute(listener=self._pass_through),
            'dex': _v.Attribute(listener=self._pass_through),
            'con': _v.Attribute(listener=self._pass_through),
            'int': _v.Attribute(listener=self._pass_through),
            'wis': _v.Attribute(listener=self._pass_through),
            'cha': _v.Attribute(listener=self._pass_through)
        }  # type: Dict[str, Union[Points, Attribute]]

    def notify(self) -> None:
        for listener in self._listeners:
            listener(self)

    def add_listener(self, listener: 'Callable[[Actor], None]'):
        self._listeners.append(listener)
        listener(self)

    def remove_listener(self, listener: 'Callable[[Actor], None]'):
        self._listeners.remove(listener)

    def attribute(self, key: str) -> 'Union[Points, Attribute]':
        return self._attributes[key]

    def hp(self) -> 'Points':
        return self._attributes['hp']

    def mp(self) -> 'Points':
        return self._attributes['mp']

    def strength(self) -> 'Attribute':
        return self._attributes['str']

    def dexterity(self) -> 'Attribute':
        return self._attributes['dex']

    def constitution(self) -> 'Attribute':
        return self._attributes['con']

    def intelligence(self) -> 'Attribute':
        return self._attributes['int']

    def wisdom(self) -> 'Attribute':
        return self._attributes['wis']

    def charisma(self) -> 'Attribute':
        return self._attributes['dex']

    def initiative(self, roll_value: 'Optional[int]' = None) -> int:
        if roll_value is not None:
            self._init_roll = max(min(roll_value, 20), 1)
        return self._init_mod + min(self.dexterity().mod(), self._max_dex_mod)

    def speed(self) -> IntVar:
        return self._speed

    def __getitem__(self, key: str):
        return self._attributes[key]
