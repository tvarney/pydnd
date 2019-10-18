
import pytest

from dnd import io


def test_scanner_discard_spaces():
    scanner = io.Scanner("    asdf")
    scanner.discard_spaces()
    assert scanner.current_char == 'a'


def test_scanner_next_token():
    scanner = io.Scanner(" one two three ")
    assert scanner.next_token() == "one"
    assert scanner.next_token() == "two"
    assert scanner.next_token() == "three"
    assert scanner.next_token() is None

    scanner = io.Scanner("one")
    assert scanner.next_token() == "one"
    assert scanner.next_token() is None


def test_scanner_next_int():
    scanner = io.Scanner("1 2 3")
    assert scanner.next_int() == 1
    assert scanner.next_int() == 2
    assert scanner.next_int() == 3
    assert scanner.next_int() is None

    scanner = io.Scanner("1a 2b 3c")
    assert scanner.next_int(require_space=False) == 1
    assert scanner.next_token() == "a"
    assert scanner.next_int(require_space=False) == 2
    assert scanner.next_token() == "b"
    assert scanner.next_int(require_space=False) == 3
    assert scanner.next_token() == "c"
    assert scanner.next_int() is None

    with pytest.raises(ValueError):
        scanner = io.Scanner("1b")
        scanner.next_int()