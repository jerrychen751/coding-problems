from typing import List


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        # We have m x n grid, where r1 is located at grid[0][0] and r2 is located at grid[0][n - 1]
        # Return max number of cherries obtainable; cherries disappear after being collected by a robot
        # When on row i, r1 can access grid[i][:r_bound] and r2 can access grid[i][l_bound:]
        # where r_bound = max(n, i) and l_bound = min(n - 1 - i, 0)
        m = len(grid)
        n = len(grid[0])
        dp = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(m)]
        # dp[i][j1][j2] = max cherries collectable given r1 starts at grid[i][j1] and r2 starts at grid[i][j2]
        # and we have grid[i:]

        # Set base case
        for i in range(n):
            for j in range(n):
                if i == j:
                    dp[m - 1][i][j] = grid[m - 1][i]
                else:
                    dp[m - 1][i][j] = grid[m - 1][i] + grid[m - 1][j]

        def calc_best_prev_state_cherries(row: int, col1: int, col2: int, dp: list[list[list[int]]]) -> int:
            dirs = (-1, 0, 1)
            best = 0
            for d1 in dirs:
                j1 = col1 + d1
                for d2 in dirs:
                    j2 = col2 + d2
                    if j1 >= 0 and j1 < n and j2 >= 0 and j2 < n:
                        best = max(best, dp[row + 1][j1][j2])
            
            return best

        # Fill in remaining
        # dp[0][0][n - 1] is solution, since this represents cherries achievable given grid[0:] and r1 in col 0 and r2 in col n-1
        for i in range(m - 2, -1, -1):
            # dp[i][j1][j2] = best from row i + 1 plus grid[i][j1] plus grid[i][j2] (or just grid[i][j1] if j1==j2)
            # best from row i + 1 is taken from all candidates
            # dp[i + 1][j1 + dj1][j2 + dj2] for dj1 in (-1, 0, 1) for dj2 in (-1, 0, 1)
            for j1 in range(n):
                for j2 in range(n):
                    prev = calc_best_prev_state_cherries(i, j1, j2, dp)
                    new_cherries = grid[i][j1] + grid[i][j2] if j1 != j2 else grid[i][j1]
                    dp[i][j1][j2] = prev + new_cherries
        
        return dp[0][0][n - 1]
