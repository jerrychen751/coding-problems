class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = []
        i, j = 0, 0
        # as long as (i + j) % 2 == 0, use letter from word1[i] and increment
        # otherwise use letter from word2
        n, m = len(word1), len(word2)
        while i < n and j < m:
            if (i + j) % 2 == 0:
                res.append(word1[i])
                i += 1
            else:
                res.append(word2[j])
                j += 1

        if i < n:
            res.append(word1[i:])
        else:
            res.append(word2[j:])

        return "".join(res)
