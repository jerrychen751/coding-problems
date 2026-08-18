from typing import List


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_word = False

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        '''
        words, list of strings
        4-connected neighbors can form word
        cell can be reused across words but not reused in same word
        return empty array if none found

        iterate through all cells as potential starts, for each cell iterate through words
            recurse into neighbors, looking for next letter in word, track used cells for the word to not reuse letters

        trie, build from list of words
        use trie to prune paths that we explore; if some prefix doesn't appear in trie stop exploring that path

        define and build trie using words
        def backtrack(i: int, j: int, node: TrieNode, seen: set[tuple[int, int]], path: list[str]) -> None:
            if node.is_word, add word to resulting list

            add i, j to seen
            for each neighbor:
                if neighbor is in bounds and not in seen and neighbor letter is in node.children:
                    update path state
                    recurse
                    pop end of path

        for each cell:
            call backtrack()

        n*m*4*l
        '''

        # Construct the Trie
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True

        found_words = []
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        m = len(board)
        n = len(board[0])
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n
        def backtrack(i: int, j: int, node: TrieNode, seen: set[tuple[int, int]], path: list[str]) -> None:
            if node.is_word:
                found_words.append("".join(path))
                node.is_word = False # no longer search for word again

            for di, dj in dirs:
                new_i, new_j = i + di, j + dj
                if in_bounds(new_i, new_j) and (new_i, new_j) not in seen and board[new_i][new_j] in node.children:
                    letter = board[new_i][new_j]
                    path.append(letter)
                    seen.add((new_i, new_j))
                    backtrack(new_i, new_j, node.children[letter], seen, path)
                    path.pop()
                    seen.remove((new_i, new_j))

                    if not node.children[letter].is_word and not node.children[letter].children:
                        del node.children[letter]

        for i in range(m):
            for j in range(n):
                letter = board[i][j]
                if letter in root.children:
                    child = root.children[letter]
                    backtrack(i, j, child, set([(i, j)]), [letter])

                    if not child.is_word and not child.children:
                        del root.children[letter]

        return found_words
