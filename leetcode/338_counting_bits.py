from typing import List

class Solution:
    def countBits(self, n: int) -> List[int]:
        # binary representation of i from 0...n
        # res[i] should contain number of 1's in binary representation of i
        res = [0] * (n + 1)
        for i in range(1, n + 1):
            res[i] = res[i >> 1] + (i & 1)
        
        return res