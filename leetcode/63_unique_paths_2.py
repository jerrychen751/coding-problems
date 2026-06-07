from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        # Again, let dp[i][j] be number of unique paths that exist to reach grid[i][j]
        # If obstacleGrid[i][j] == 1, then dp[i][j] should be set to 0
        # Still, dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        # Base case is treated specially

        # Can destination be an obstacle? -> YES
        if obstacleGrid[0][0] == 1 or obstacleGrid[-1][-1] == 1:
            return 0

        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        dp = [0] * n
        first_row = obstacleGrid[0]
        for i in range(n):
            if first_row[i] == 1:
                break
            dp[i] = 1

        met_obstacle_down = False # traversing down first column
        for i in range(1, m):
            if obstacleGrid[i][0] == 0 and not met_obstacle_down:
                left = 1
            else:
                met_obstacle_down = True
                left = 0

            for j in range(1, n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0
                else:
                    dp[j] = dp[j] + left

                left = dp[j]

        return dp[-1]
