
import pytest

from dnd import scanner


def test_scanner_discard_spaces():
    s = scanner.Scanner("    one")
    s.discard_spaces()
    assert s.current_char == 'o'


def test_scanner_next_token():
    s = scanner.Scanner(" one two three ")
    assert s.next_token() == "one"
    assert s.next_token() == "two"
    assert s.next_token() == "three"
    assert s.next_token() is None

    s = scanner.Scanner("one")
    assert s.next_token() == "one"
    assert s.next_token() is None


def test_scanner_next_int():
    s = scanner.Scanner("1 2 3")
    assert s.next_int() == 1
    assert s.next_int() == 2
    assert s.next_int() == 3
    assert s.next_int() is None

    s = scanner.Scanner("1a 2b 3c")
    assert s.next_int(require_space=False) == 1
    assert s.next_token() == "a"
    assert s.next_int(require_space=False) == 2
    assert s.next_token() == "b"
    assert s.next_int(require_space=False) == 3
    assert s.next_token() == "c"
    assert s.next_int() is None

    with pytest.raises(ValueError):
        s = scanner.Scanner("1b")
        s.next_int()
