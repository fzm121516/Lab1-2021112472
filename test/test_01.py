import pytest
from src.main import query_bridge_words


@pytest.mark.parametrize(
    "word1, word2, expected_result",
    [
        ("cat", "dog", "The bridge words from \"cat\" to \"dog\" are: fish, bird."),
        ("apple", "banana", "No bridge words from \"apple\" to \"banana\"!"),
        ("hello", "world", "No \"hello\" in the graph!"),
        ("world", "hello", "No \"world\" in the graph!"),
    ],
)

def test_query_bridge_words(word1, word2, expected_result):
    assert query_bridge_words(word1, word2) == expected_result
