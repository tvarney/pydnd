
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
