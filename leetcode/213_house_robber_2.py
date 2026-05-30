from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        # Same as House Robber I if we end up skipping 1st house -> won't lead to issue w/ circular arrangement no matter how ending is picked (whether prev2 or prev1 is used)
        # Same with skipping last house by guarantee
        # So then there are two cases, treat nums[1:] and nums[:-1] as two lines of houses and run House Robber I on them
        # Pick the max of these two cases

        def rob_linear(nums: List[int], start: int, end: int) -> int:
            # Start/end avoids making slices
            # Let start/end be inclusive
            prev2, prev1 = 0, nums[start]
            for i in range(start + 1, end + 1):
                best = max(prev2 + nums[i], prev1)
                prev2 = prev1
                prev1 = best

            return max(prev1, prev2)

        n = len(nums)
        # Edge case: n == 1
        if n <= 2:
            return max(nums)

        return max(rob_linear(nums, 0, n - 2), rob_linear(nums, 1, n - 1)) # first is exclude last, second is exclude first
