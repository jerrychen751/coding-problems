from typing import List


class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        # Start right -> left
        # Base case is max pts obtainable from questions[i:] where i = n - 1
        # Let dp[i] = max pts from questions[i:]
        # Iterate from i = n-1..0
        # dp[i] = max(dp[i + 1], questions[i][0] + dp[i + questions[i][1] + 1]) if questions[i][1] + 1 < n else max(dp[i + 1], questions[i][0])
        n = len(questions)
        dp = [0] * n
        dp[-1] = questions[-1][0]
        def in_bounds(i: int) -> bool:
            return i < n

        for i in range(n - 2, -1, -1):
            pts, skips = questions[i]
            dp[i] = max(dp[i + 1], pts + dp[i + skips + 1]) if in_bounds(i + skips + 1) else max(dp[i + 1], pts)

        return dp[0]
