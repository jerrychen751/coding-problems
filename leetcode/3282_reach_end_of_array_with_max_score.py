from typing import List


class Solution:
    def findMaximumScore(self, nums: List[int]) -> int:
        # score gain from a jump from i -> j is (j - i) * nums[i]
        # can only jump forward / right
        # no negative integers in array

        # try to jump large distances from large numbers
        # [1, 3, 1 ,5] -> start on nums[0]==1
        # We see that 3 is close and larger, so we jump to 3 so we can start jumping next time from a larger number
        # Jump to closest number that is larger than current starting point

        best = nums[0]
        best_idx = 0
        score = 0
        for i in range(1, len(nums) - 1):
            if nums[i] > best:
                score += (i - best_idx) * best
                best = nums[i]
                best_idx = i

        # Process the very last value
        dist = len(nums) - 1 - best_idx
        score += dist * best
        return score
