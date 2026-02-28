from typing import List
from collections import Counter

class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        # We want to track the number of subsets a certain combination of m, n can contain
        # We could have a 2D dp, where dp[i][j] stores max number of subsets with at most i 0's and j 1's

        # We can generate a counter as we iterate through strs
        
        def count_zeros_ones(s: str) -> tuple[int, int]:
            """Return tuple of zeros, ones count given a binary string."""
            count = Counter(s)
            return count['0'], count['1']

        # m = max zeros, n = max ones, dp[i][j] is max subsets for i zeros and j ones
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for s in strs:
            zeros, ones = count_zeros_ones(s)

            for i in range(m, zeros - 1, -1):
                for j in range(n, ones - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
        
        return dp[-1][-1]