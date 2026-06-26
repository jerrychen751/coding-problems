from typing import List


class Solution:
    def maxScoreSightseeingPair(self, values: List[int]) -> int:
        # values[i] stores value, difference between indices is distance
        # the score of a pair of sightseeing spots is values[i] + values[j] - (j - i) or -dist
        # At worst try each pair, O(n^2)
        # Iterate through possible right endpoints
        # As we iterate through 1..n-1, dp[i] stores best left endpoint (max values[i] + i)
        best_left = values[0] # best left score from 0..i-1
        res = 0 # best total score
        for i in range(1, len(values)):
            right = values[i]
            res = max(res, best_left + right - i)
            best_left = max(best_left, values[i] + i)

        return res
