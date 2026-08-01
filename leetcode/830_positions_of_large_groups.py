from typing import List


class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        # group is identifie by [i, j] index positions
        # group is large if len >= 3
        # return intervals of all large groups sorted by start index
        
        # [0,0], [1,2], [3,6], [7,8], [9,9]
        # large is j - i > 2
        # sliding approach, maintain i, j indices
        
        # if s[i] != s[j], then group indices are [i,j-1] and size is j - i
        # if size is >= 3, then we append [i,j-1] to results
        # since we slide window from left -> right, we go by sorted order for start index
        
        res = []
        i = 0
        n = len(s)
        for j in range(n):
            if s[i] == s[j]:
                continue
            
            win_size = j - i
            if win_size >= 3:
                res.append([i, j - 1])
            i = j
        
        # process the very last window
        j = n - 1
        win_size = j - i + 1
        if win_size >= 3:
            res.append([i, j])
        
        return res
