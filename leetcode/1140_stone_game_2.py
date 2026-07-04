from functools import cache
from typing import List


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        # Takes piles[:X] where X can be from 1 to 2M
        # After each turn, M = max(M, X) -> M increases to at most 2M each turn
        # Not greedy, because we don't necessarily want to take max X each time since that means player after gets even more

        # Prefix sum
        # DP
        # On each person's turn, stones remaining are piles[i:]
        # There is a specific M
        # The person chooses X where 1 <= X <= 2M
        # The next person's turn has stones piles[i + X:]
        # The next person's turn as M = max(M, X)
        # Future state depends on i, M (doesn't depend on X because given i & M player always picks same X on their turn)

        # To determine the best X, we try 1..2M values for X
        # dp[i][j] stores the most points curr player can obtain from piles[i:] where M = j
        # dp[i][j] = MAX(sum(piles[i:]) - dp[i + X][max(j, X)]) across X values from 1..2M

        # We use dp (top-down memoization) instead of tabulation as state is easier to manage
        # base case is if X >= n - i then we can take all remaining stones and should always do so
        # otherwise we return for this function MAX(sum(piles[i:]) - dp[i + X][max(j, X)]) across X values from 1..2M

        n = len(piles)
        suffix_sum = [0] * n
        suffix_sum[-1] = piles[-1]
        for i in range(n - 2, -1, -1):
            suffix_sum[i] = piles[i] + suffix_sum[i + 1]

        @cache
        def dp(i: int, j: int) -> int:
            if i >= n:
                return 0

            if j >= n - i:
                return suffix_sum[i]

            opponent_score = float('inf') # want to minimize dp[i + X][max(j, X)]
            for x in range(1, 2 * j + 1):
                opponent_score = min(opponent_score, dp(i + x, max(j, x)))

            return suffix_sum[i] - opponent_score

        return dp(0, 1)
