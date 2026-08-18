'''
map each word in words to a cursor idx; cursor is next letter to be compared (new stream input char)
don't know when to reset cursor; suffix may not match initially but later may match

e.g., aab vs. aaab

Build a trie from words, but with each word reversed
For each new char in stream, check if it matches last character of some word (root of trie)
iterate backward in stream + trie to match the suffix

store at most the last max(len(word) for word in words) for stream
'''

from collections import deque
from typing import List

class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_word = False

class StreamChecker:

    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.max_len = max(map(len, words))
        self.stream = deque()

        for word in words:
            node = self.root
            for char in reversed(word):
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]

            node.is_word = True

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        if len(self.stream) > self.max_len:
            self.stream.popleft()

        node = self.root
        for char in reversed(self.stream):
            if char not in node.children:
                return False
            node = node.children[char]
            if node.is_word:
                return True

        return False


# Your StreamChecker object will be instantiated and called as such:
# obj = StreamChecker(words)
# param_1 = obj.query(letter)
