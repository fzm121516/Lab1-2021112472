import pytest
from src.main import calc_shortest_path


@pytest.mark.parametrize(
    "word1, word2, expected_result",
    [
        ("you", "me", "No \"you\", \"me\" in the graph!"),
        ("new", "me", "No \"me\" in the graph!"),
        ("new", "new", "Shortest path: new\nPath weight: 0"),
        ("civilizations", "to", "No path from \"civilizations\" to \"to\""),
        ("seek", "out", "Shortest path: seek -> out\nPath weight: 1"),
        ("seek", "civilizations", "Shortest path: seek -> out -> new -> earlier -> civilizations\nPath weight: 4"),
        ("earlier", "new", "No path from \"earlier\" to \"new\""),
    ],
)
def test_calc_shortest_path(word1, word2, expected_result):
    assert calc_shortest_path(word1, word2) == expected_result
