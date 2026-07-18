from typing import List


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        # start from bottom, iterate upward
        # let dp[i][j] represent max number of points achievable in points[i:] starting at column j
        # dp[i][j] = points[i][j] + max(dp[i + 1][k] - abs(k - j)) where k ranges from 0..n - 1
        # also note that we can compress space to 1D DP since we only rely on state tracked from row below
        # For each number in points, we only want to iterate through row below it once
        # Consider we're at index i in that row
        # We iterate through row below once to determine max values on left and right of current point
        
        # For prev row, we can calculate a best_from_left and best_from_right
        # When we do best_from_left, best_from_left[i] = max(best_from_left[i - 1] - 1, prev_row[i])
        # dp[i] = max(best_from_left[i], best_from_right[i])
        # best_from_left and best_from_right have knowledge of max number of points achievable from prev row given we're at column i of all values from 0..i and i..n-1
        dp = points[-1]
        m = len(points)
        n = len(points[0])
        for i in range(m - 2, -1, -1):
            best_from_left = [0] * n
            best_from_left[0] = dp[0]
            for j in range(1, n):
                best_from_left[j] = max(best_from_left[j - 1] - 1, dp[j])
            best_from_right = [0] * n
            best_from_right[-1] = dp[-1]
            for j in range(n - 2, -1, -1):
                best_from_right[j] = max(best_from_right[j + 1] - 1, dp[j])
            
            for j in range(n):
                dp[j] = points[i][j] + max(best_from_left[j], best_from_right[j])
        
        return max(dp)
