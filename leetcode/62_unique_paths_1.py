class Solution1:
    def uniquePaths(self, m: int, n: int) -> int:
        # dp[i][j] should store the number of unique paths that the robot can take to reach grid[i][j]
        # Base case is first row / column, where the number of unique paths is always 1
        # From there on, since the robot may have travelled from either dp[i - 1][j] or dp[i][j - 1], we set dp[i][j] as the
        # sum of those paths since they are disjoint / unique
        dp = [[1 for _ in range(n)] for _ in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[-1][-1]


class Solution2:
    def uniquePaths(self, m: int, n: int) -> int:
        # Optimize w/ 1D DP
        dp = [1] * n
        for i in range(1, m):
            left = 1
            for j in range(1, n):
                dp[j] = left + dp[j]
                left = dp[j]

        return dp[-1]
