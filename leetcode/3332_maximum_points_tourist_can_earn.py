from typing import List

class Solution:
    def maxScore(self, n: int, k: int, stayScore: List[List[int]], travelScore: List[List[int]]) -> int:
        '''
        n cities, k days, both zero-indexed
        can travel from one city to any other city; free starting point
        stayScore[k][n] gives score when choosing to stay in city n on day k
        travelScore[curr][dest] is points for moving from curr -> dest on any day

        day, city, action (stay, travel)
        dp[i][j] = pts earned from day i..k-1 given on day i curr city is j
        Base case: last day; dp[k - 1][j] = max(stayScore[k - 1][j], travelScore[j])
        Recurrence:
            - Stay: stayScore[i][j] + dp[i + 1][j]
            - Travel: best over k --- travelScore[j][k] + dp[i + 1][k]

        Return max(dp[0])
        '''
        # 1D DP since we only depend on next day
        dp = [0] * n
        for j in range(n): # fill in base case
            dp[j] = max(stayScore[k - 1][j], max(travelScore[j]))

        for i in range(k - 2, -1, -1):
            curr = [0] * n
            for j in range(n):
                best_travel = 0
                for d in range(n):
                    if d == j:
                        continue
                    best_travel = max(best_travel, travelScore[j][d] + dp[d])
                curr[j] = max(stayScore[i][j] + dp[j], best_travel)

            dp = curr

        return max(dp)
