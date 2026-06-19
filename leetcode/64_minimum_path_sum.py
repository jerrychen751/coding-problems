from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        # Suppose we maintain dp of shape m x n
        # dp[i][j] contains min path sum to arrive at dp[-1][-1]
        # move from bottom up, right to left
        # dp[i][j] = grid[i][j] + min(dp[i + 1][j], dp[i][j + 1]); i.e., pick min of bottom or right since we're moving backward
        m = len(grid)
        n = len(grid[0])
        if m == 0 or n == 0:
            return 0

        # Can optimize to 1D DP
        dp = [0 for _ in range(n)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                right = dp[j + 1] if j + 1 < n else float('inf')
                bottom = dp[j] if i < m - 1 else float('inf')
                dp[j] = grid[i][j] + min(right, bottom)
                if dp[j] == float('inf'):
                    dp[j] = grid[i][j]

        return dp[0]
