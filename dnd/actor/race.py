
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


