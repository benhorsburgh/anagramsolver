import pytest

from anagramsolver.dictionary import Dictionary


@pytest.fixture(scope="module")
def dictionary() -> Dictionary:
    return Dictionary()


def test_dictionary_contains_all_letters(dictionary):
    assert len(dictionary.root.children) == 26


@pytest.mark.parametrize(
    "word, expected", [("a", True), ("mous", False), ("mouse", True)]
)
def test_in_dictionary(dictionary, word, expected):
    assert (word in dictionary) == expected


@pytest.mark.parametrize(
    "letters, solutions",
    [
        ("art", ["art", "rat", "tar", "tra"]),
        ("cat", ["cat", "act"]),
        ("ramble", ["ramble", "ambler", "marble", "blamer", "lamber"]),
        ("anagram", ["anagram"]),
    ],
)
def test_solve_word(dictionary, letters, solutions):
    found = list(dictionary.solve_word(letters))
    assert all(solution in found for solution in solutions)
    assert len(solutions) == len(found)


def test_performance(dictionary):
    assert len(list(dictionary.solve_word("basiparachromatin"))) == 2
