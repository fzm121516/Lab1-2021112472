import pytest
from src.main import query_bridge_words

@pytest.mark.parametrize(
    "word1, word2, expected_result",
    [
        ("", "", "Word1 and word2 cannot be empty!"),
        ("new", "", "Word1 and word2 cannot be empty!"),
        ("new2", "to1", "Word1 and word2 should only contain English letters!"),
        ("new2", "to", "Word1 and word2 should only contain English letters!"),
        ("new", "to", "The bridge words from \"new\" to \"to\" are: worlds."),
        ("new", "buy", "No \"buy\" in the graph!"),
        ("two", "buy", "No \"two\", \"buy\" in the graph!"),
        ("new", "worlds", "No bridge words from \"new\" to \"worlds\"!"),
    ],
)
def test_query_bridge_words(word1, word2, expected_result):
    assert query_bridge_words(word1, word2) == expected_result
