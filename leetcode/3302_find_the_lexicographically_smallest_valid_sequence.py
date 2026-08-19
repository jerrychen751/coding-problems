from typing import List


class Solution:
    def validSequence(self, word1: str, word2: str) -> List[int]:
        '''
        single char diff means almost equal
        sequence of indices need to be where indices are in ascending order; may not need to be adjacent
        word1[i] for i in indices -> word that is almost equal to word2

        changing identity of character only; no insertion/deletion
        word1 is at least as long as word2

        two pointer
        on first difference, check if we alr used swap -> if not use it, if so invalid
        start matching from beginning -> lexicographically smallest

        abcd acd 
        O(n^2)
        word1 letter -> 2 options: use it or skip it
        if we use it, then word1[i + 1:] must be able to form word2[j + 1:] (if we exchange word1[i] for word2[j])
        suffix[j] stores rightmost index needed in word1 to match j:

        iterate through word1 indices in order
        if char matches:
            take it and advance next index
        elif not swap_used and i < suffix[j + 1]:
            use swap
        else:
            try to use next index i
        
        if j > len(word2): return array
        otherwise return empty array
        '''
        n = len(word1)
        m = len(word2)
        if m > n:
            return []
        suffix = [-1] * m
        j = m - 1
        for i in range(n - 1, -1, -1):
            if j >= 0 and word1[i] == word2[j]:
                suffix[j] = i
                j -= 1
        
        i = 0
        j = 0
        indices = []
        swap_used = False
        while i < n and j < m:
            if word1[i] == word2[j]:
                indices.append(i)
                i += 1
                j += 1
            elif not swap_used and (j == m - 1 or i < suffix[j + 1]):
                # nothing from indices 0..i are needed to build word2[j + 1:]
                indices.append(i)
                swap_used = True
                i += 1
                j += 1
            else:
                i += 1
        
        if j >= m:
            return indices
        
        return []
