from collections import deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        '''
        adj elements in wordList differ by single letter
        beginWord not in wordList, endWord is last word in wordList
        beginWord ... wordList[0..k]
        return number of words in shortest transformation seq from beginWord to endWord

        if endWord != wordList[-1] then return 0?
        beginWord is guaranteed 1 char diff from beginning of wordList? no
        all words same length? yes

        start w/ beginWord
        form set of candidates chosen from wordList that are 1 char diff from beginWord

        connections between words that are 1 char diff
        explore connections 1 layer at a time

        not going to reuse words; keep seen set
        1 is base transformation length
        hit
        hot
        dot, lot
        dog, log
        cog
        number of levels traversed til first formation of endWord is our answer

        given a curr word that we're processing
        iterate through indices, try each letter of the alphabet
        if that word is in wordList set and not seen before (not curr word, not prev processed word)
            if endWord: return levels ct
            else: add to queue

        N = len(wordList)
        M = len(beginWord)
        N * M^2
        '''
        letters = [chr(ord('a') + i) for i in range(26)]
        word_len = len(beginWord)
        queue = deque([beginWord])
        levels = 0
        words = set(wordList)
        seen = set()
        while queue:
            levels += 1
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr in seen:
                    continue

                seen.add(curr)
                if curr == endWord:
                    return levels
                for i in range(word_len):
                    for letter in letters:
                        candidate = curr[:i] + letter + curr[i + 1:]
                        if candidate in words and candidate not in seen:
                            queue.append(candidate)

        return 0
