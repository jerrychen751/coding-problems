from functools import cache


class Solution1:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        # In the base case, the number of ways to move ball out at any position (i, j) with a single move is the number of dirs
        # where the result is out of bounds

        # Let dp[i][j][k] represent the number of ways to move ball at (i, j) out of bounds with k more moves left
        # Then starting from 0, everything will be 0
        # Starting from k=1, it will be n_dirs_out / 4
        # From there on, dp[i][j][k] = sum of dp[a][b][k - 1] where there are 4 combinations of a,b (places ball could be next)

        # We notice that we also only depend on previous layer of 2D DP

        dp = [[0 for _ in range(n)] for _ in range(m)]
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def in_bounds(i: int, j: int, m: int, n: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        for k in range(1, maxMove + 1):
            new_dp = [[0 for _ in range(n)] for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for di, dj in dirs:
                        if in_bounds(i + di, j + dj, m, n): # Number of unique paths to move off grid given we didn't move off in this step
                            new_dp[i][j] = (new_dp[i][j] + dp[i + di][j + dj]) % (10**9 + 7)
                        else: # Number of unique paths given we moved off in this step
                            new_dp[i][j] = (new_dp[i][j] + 1) % (10**9 + 7)

            dp = new_dp

        return dp[startRow][startColumn]


class Solution2:
    def findPaths(
        self,
        m: int,
        n: int,
        maxMove: int,
        startRow: int,
        startColumn: int,
    ) -> int:
        MOD: int = 1_000_000_007

        @cache
        def dfs(i: int, j: int, moves_left: int) -> int:
            if i < 0 or i >= m or j < 0 or j >= n:
                return 1

            if moves_left == 0:
                return 0

            return (
                dfs(i - 1, j, moves_left - 1)
                + dfs(i + 1, j, moves_left - 1)
                + dfs(i, j - 1, moves_left - 1)
                + dfs(i, j + 1, moves_left - 1)
            ) % MOD

        return dfs(startRow, startColumn, maxMove)
