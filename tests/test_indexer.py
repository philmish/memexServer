import pytest
from memexIndexer.indexer.utils import get_tokens


@pytest.mark.parametrize("inp, comp_vals", [
    ("I am going home", ["going", "home"]),
    ("The house we are staying in is really old", [
        "old",
        "house",
        "staying",
        "really"
        ]),
    ("THE WORLD IS BURNING", ["world", "burning"])
])
def test_get_tokens_basic(inp, comp_vals):
    data = get_tokens(inp)
    for val in comp_vals:
        assert val in data


@pytest.mark.parametrize("inp, comp_vals", [
    ("'Hello' she said, as she entered the room. 'How are you doing today ?'.", ["the", "she", "are", "'hello'"])
])
def test_get_tokens_stopdwords(inp, comp_vals):
    data = get_tokens(inp)
    for val in comp_vals:
        assert val not in data
