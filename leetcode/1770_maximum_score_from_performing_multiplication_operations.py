from functools import cache
from typing import List


class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        # nums of size n
        # multipliers of size m
        # can perform m operations

        # each operation, we can choose an integer from start/end of nums
        # and then add multipliers[i] * chosen num
        # and then remove that num from nums

        # At each step, we choose between front/back of array
        # pop, multiply with i-th multiplier

        # [1, 2, 3]
        # [3, 2, 1]
        # DP because we can't take locally optimal choice
        # Consider a simple case, where we have dp[k:] remaining of multipliers
        # Then we would have different i,j positions for left/right side of array
        # but no matter what i + (n - 1 - j) needs to equal k
        # So we would have like 0, -k to k, 0 offsets from 0 and n - 1

        # subproblems overlap because taking one from right then left vs. left then right
        # leaves us with same nums and multipliers

        # Let i, j be left and right endpoint indices for nums
        # Given a fixed operation number and left endpoint, j = n - 1 - (operation - left)
        # Let dp(operation, i) return max score achievable given multipliers[operation:] and we chose a number which is either nums[left] or nums[right] to remove and multiply

        n = len(nums)
        m = len(multipliers)

        @cache
        def dp(operation: int, i: int) -> int:
            # Base case; we've used up all of multipliers
            if operation == m:
                return 0

            # We can pick either left or right element to remove
            j = n - 1 - (operation - i)
            score_pick_left = nums[i] * multipliers[operation] + dp(operation + 1, i + 1)
            score_pick_right = nums[j] * multipliers[operation] + dp(operation + 1, i)

            return max(score_pick_left, score_pick_right)

        return dp(0, 0)
