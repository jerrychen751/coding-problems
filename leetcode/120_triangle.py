import copy
from typing import List


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        # triangle[i] is i-th row of triangle, containing (i + 1) elements at indices 0..i
        # there may be negatives
        # greedy doesn't work; too shortsighted for overall min path
        # suppose we started working up from the bottom of the traingle
        # path must end at exactly one of those; at each level moving upward we track min path sum achieved
        # at each new level, we try each element on that level against prior min path sum

        # O(n^2) time, O(n) if optimizing space
        dp = copy.copy(triangle[-1])
        n = len(triangle)
        for i in range(n - 2, -1, -1):
            # adj elements on row below are at i, i + 1
            for j in range(i + 1): # j indexes elements on triangle[i]
                num = triangle[i][j]
                dp[j] = num + min(dp[j], dp[j + 1])

        return dp[0]
