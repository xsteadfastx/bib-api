import pytest

from app import tools


@pytest.mark.parametrize('input,expected', [
    ((['a', 'b', 'c'], 'b'), 'c'),
    ((['a', 'b', 'c'], 'a'), 'b'),
    ((['a', 'b', 'c'], 'c'), None),
    ((['a', 'b', 'c'], 'd'), None)
])
def test_next_page(input, expected):
    assert tools.next_page(input[0], input[1]) == expected
