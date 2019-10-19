
import typing
if typing.TYPE_CHECKING:
    from typing import Optional


class Scanner(object):
    def __init__(self, data: str) -> None:
        self._data = data
        self._len = len(data)
        self._idx = 0

    def discard_spaces(self) -> None:
        while self._idx < self._len and self._data[self._idx].isspace():
            self._idx += 1

    def next_token(self) -> 'Optional[str]':
        self.discard_spaces()
        if self._idx >= self._len:
            return None

        start = self._idx
        while self._idx < self._len and not self._data[self._idx].isspace():
            self._idx += 1

        return self._data[start:self._idx]

    def next_int(self, require_space: bool = True) -> 'Optional[int]':
        self.discard_spaces()
        start = self._idx

        if start >= self._len:
            return None

        if not self._data[self._idx].isnumeric():
            self._idx = start
            raise ValueError("next token is not numeric")

        self._idx += 1
        # Use str.isdecimal(), since we only want '0'-'9'.
        # str.isdigit() includes superscripts, and str.isnumeric() includes
        # all number code points.
        while self._idx < self._len and self._data[self._idx].isdecimal():
            self._idx += 1

        char = self.current_char
        if require_space and char is not None and not char.isspace():
            self._idx = start
            raise ValueError("next token is not numeric")

        return int(self._data[start:self._idx])

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def current_char(self) -> 'Optional[str]':
        if self._idx >= self._len:
            return None
        return self._data[self._idx]
