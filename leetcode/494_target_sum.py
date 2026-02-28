from typing import List

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        # Want to know number of different combinations of nums which makes up target
        # Must use all nums, either adding or subtracting each number
        
        # We can track whether some result i is attainable via dp[i]
        # dp[i] holds the number of expressions/ways we can obtain i
        
        # Let P be sum of positive subset, N be sum of negative subset
        # Conditions become, P - N = target, P + N = sum(nums)
        # We want P = (target + total) / 2 where total = sum(nums)

        total = sum(nums)
        if (target + total) & 1 != 0 or (total + target) < 0:
            return 0

        P = (target + total) // 2 # must be a sum of positive integers, and therefore must be even and non-negative
        # We want to count number of subsets summing to P
        dp = [0] * (P + 1) # dp[i] stores number of subsets summing to i
        dp[0] = 1 # base case

        for num in nums:
            for i in range(len(dp) - 1, num - 1, -1):
                dp[i] += dp[i - num]
        
        return dp[P]