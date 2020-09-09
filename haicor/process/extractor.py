"""
Copyright (c) 2020 Hecong Wang

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""
from __future__ import annotations

from itertools import groupby
from typing import Generator, Iterable, Tuple

MatchGenerator = Generator[Tuple[int, Tuple[str, ...]], None, None]


class TrieConceptExtractor:
    """A trie-based concept extractor."""

    def __init__(self, dictionary: Iterable[Tuple[str, ...]]):
        self.dictionary = self.to_trie(dictionary)

    def extract(self, tokens: Iterable[str]) -> MatchGenerator:
        """Extracts all concepts from the given tokens.

        Args:
            tokens (Iterable[str]): Tokens, as string, to extract concepts from.

        Returns:
            MatchGenerator: A `MatchGenerator` with each element consists of the
                string index of the match, and the tokens of the match.
        """
        matches, updates = [], []

        for index, token in enumerate(tokens):
            matches.append(((index, []), self.dictionary))

            for (start, match), pointer in matches:
                if token not in pointer:
                    continue

                matched, pointer = pointer.get(token)

                if matched:
                    yield start, match + [token]

                updates.append(((start, match + [token]), pointer))

            matches, updates = updates, []

    @staticmethod
    def to_trie(dictionary: Iterable[Tuple[str, ...]]) -> dict:
        """Returns a trie structure representing the given dictionary.

        Args:
            dictionary (Iterable[Tuple[str, ...]]): Concepts to be extracted by
                the extractor. Concepts are specified as tuple of strings, each
                representing a token of the concept.

        Returns:
            dict: The trie structure representing the given dictionary.
        """
        def build_trie(entries: Iterable[Tuple[str, ...]]) -> Tuple[bool, dict]:
            match, entries = [] in entries, (i for i in entries if i)

            return match, {head: build_trie([i[1:] for i in tails])
                           for head, tails
                           in groupby(entries, key=lambda x: x[0])}

        return build_trie(sorted(dictionary))[1]
