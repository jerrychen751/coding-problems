class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_word = False

class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str) -> bool:
        return self._search(word, self.root, 0)
        
    def _search(self, word: str, node: TrieNode, idx: int) -> bool:
        # when we are on char = word[idx], we must check node.children for char
        if idx >= len(word):
            return node.is_word

        if word[idx] == '.':
            for child in node.children.values():
                if self._search(word, child, idx + 1):
                    return True
        else:
            char = word[idx]
            if char in node.children:
                return self._search(word, node.children[char], idx + 1)
        
        return False

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)
