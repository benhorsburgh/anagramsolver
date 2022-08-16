from typing import Dict


class Node:
    def __init__(self):
        self.children: Dict[str, "Node"] = {}
        self.is_word = False


class Dictionary:
    def __init__(self, filename: str = "/usr/share/dict/words"):
        self.root = Node()
        with open(filename, encoding="utf-8") as f:
            for word in f:
                cur = self.root
                for letter in word.rstrip().lower():
                    if letter not in cur.children:
                        cur.children[letter] = Node()
                    cur = cur.children[letter]
                cur.is_word = True

    def __contains__(self, item) -> bool:
        """True if item is valid word in the dictionary"""
        cur = self.root
        for letter in item:
            if letter not in cur.children:
                return False
            cur = cur.children[letter]
        return cur.is_word

    def solve_word(self, letters: str, node: Node = None, partial: bool = False):
        """
        Generate anagrams of the input letters
        Args:
            letters: string of characters from which to generate anagram words
            node: (optional) starting point in the dictionary. Defaults to root
            partial: (optional) if partial anagrams are permitted. Defaults to False

        Returns:
            Generator of anagrams
        """
        node = node or self.root

        if node.is_word and (len(letters) == 0 or partial):
            yield ""

        seen_letters = []
        seen_words = []
        for i, letter in enumerate(letters):
            if letter in node.children and letter not in seen_letters:
                seen_letters.append(letter)
                for suffix in self.solve_word(
                    letters[:i] + letters[i + 1 :],
                    node=node.children[letter],
                    partial=partial,
                ):
                    word = letter + suffix
                    if word not in seen_words:
                        seen_words.append(word)
                        yield letter + suffix
