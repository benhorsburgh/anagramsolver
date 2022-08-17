import pytest

from anagramsolver.dictionary import Dictionary


@pytest.fixture(scope="module")
def dictionary() -> Dictionary:
    return Dictionary.from_file()


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
def test_find_anagram_default(dictionary, letters, solutions):
    found = list(dictionary.anagrams(letters))
    assert all(solution in found for solution in solutions)
    assert len(solutions) == len(found)


@pytest.mark.parametrize(
    "letters, solutions",
    [
        ("pur", ["p", "pu", "pur", "u", "up", "ur", "r"]),
        ("red", ["r", "re", "red", "e", "er", "erd", "ed", "d", "de"]),
    ],
)
def test_partial(dictionary, letters, solutions):
    found = list(dictionary.anagrams(letters, partial=True))
    assert all(solution in found for solution in solutions)
    assert len(solutions) == len(found)


def test_performance(dictionary):
    assert len(list(dictionary.anagrams("basiparachromatin"))) == 2


@pytest.mark.parametrize("min_length", [1, 2, 3, 4, 5])
def test_min_length(dictionary, min_length):
    found = list(dictionary.anagrams("mixed", partial=True, min_length=min_length))
    assert all(len(solution) >= min_length for solution in found)
    assert len(found) > 0


@pytest.mark.parametrize(
    "letters, anagrams",
    [
        (
            "wood",
            [
                "do ow",
                "do wo",
                "od ow",
                "od wo",
                "ow do",
                "ow od",
                "wo do",
                "wo od",
                "wood",
            ],
        )
    ],
)
def test_multi(dictionary, letters, anagrams):
    found = sorted(list(dictionary.anagrams(letters, multi=True, min_length=2)))
    assert all(anagram in found for anagram in anagrams)
    assert len(found) == len(anagrams)
    print(found)


def test_words():
    words = ["a", "Aa", "b", "c", "cat"]
    dictionary = Dictionary(words=words)
    assert all(word in dictionary.words() for word in words)
    assert len(words) == len(list(dictionary.words()))
