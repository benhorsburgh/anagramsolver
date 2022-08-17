from typing import Dict, Generator, Any, Iterator, Iterable


class Node:
    def __init__(self):
        self.children: Dict[str, "Node"] = {}
        self.is_word = False
        self.word_length = -1


class Dictionary:

    @staticmethod
    def from_file(filename: str = "/usr/share/dict/words",):
        with open(filename, encoding="utf-8") as f:
            words = [word.rstrip().lower() for word in f]
            return Dictionary(words)

    def __init__(
        self,
        words: Iterable[str]
    ):
        self.root = Node()
        for word in words:
            cur = self.root
            for letter in word:
                if letter not in cur.children:
                    cur.children[letter] = Node()
                cur = cur.children[letter]
            cur.is_word = True
            cur.word_length = len(word)

    def __contains__(self, item) -> bool:
        """True if item is valid word in the dictionary"""
        cur = self.root
        for letter in item:
            if letter not in cur.children:
                return False
            cur = cur.children[letter]
        return cur.is_word

    def words(self) -> Iterator[str]:
        def _words(_node: Node = None):
            _node = _node or self.root

            if _node.is_word:
                yield ""

            for letter in _node.children:
                for suffix in _words(_node=_node.children[letter]):
                    yield letter + suffix
        yield from _words()

    def anagrams(
        self,
        letters: str,
        partial: bool = False,
        min_length: int = 1,
        multi: bool = False,
    ) -> Iterator[str]:
        """
        Generate anagrams of the input _letters
        Args:
            letters: string of characters from which to generate anagram words
            partial: (optional) if _partial anagrams are permitted. Defaults to False
            min_length: (optional) minimum length of word that can appear in the
            solution. Only applies when _partial=True
            multi: (optional) if multiple words are allowed in the solution. Defaults
            to False
        Returns:
            Generator of anagrams
        """

        def _anagrams(
            _letters: str,
            _node: Node = None,
            _partial: bool = False,
            _min_length: int = 1,
            _multi: bool = False,
        ):

            _node = _node or self.root

            if (
                _node.is_word
                and (len(_letters) == 0 or _partial)
                and _node.word_length >= _min_length
            ):
                yield ""

            seen_words = []
            seen_letters = []
            for i, letter in enumerate(_letters):
                if letter in _node.children and letter not in seen_letters:
                    seen_letters.append(letter)
                    for suffix in _anagrams(
                        _letters[:i] + _letters[i + 1 :],
                        _node=_node.children[letter],
                        _partial=_partial,
                        _min_length=_min_length,
                        _multi=_multi,
                    ):
                        word = letter + suffix
                        if word not in seen_words:
                            seen_words.append(word)
                            yield word

            if _multi and _node.is_word and _node.word_length >= _min_length:
                for suffix in _anagrams(
                    _letters,
                    _node=self.root,
                    _partial=_partial,
                    _min_length=_min_length,
                    _multi=_multi,
                ):
                    word = " " + suffix
                    if word not in seen_words:
                        seen_words.append(word)
                        yield word

        yield from _anagrams(
            _letters=letters, _partial=partial, _min_length=min_length, _multi=multi
        )
