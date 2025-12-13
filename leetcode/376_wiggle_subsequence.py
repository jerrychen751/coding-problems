from typing import List

class Solution:
    # DP only
    def wiggleMaxLength(self, nums: List[int]) -> int:
        # We want to find the longest subsequence (able to remove certain indices) such that consecutive values within the subsequence have alternating deltas
        # Maintain a dp state array where dp[i] = longest valid subsequence ending at i
        n = len(nums)
        if n < 2:
            return n
        
        dp = [0] * n
        dp[0] = 1
        for j in range(1, n):
            # How do we calculate dp[j]?
            # The simple way is to iterate through dp[:j] and then calculate candidate value as abs(dp[i]) + 1 if dp[i] and nums[j] - nums[i] have different signs
            # Throughout iterations, we only keep the best state in the end, being the max valid subsequence able to be formed
            # We also need to track positive and negative deltas...
            # Could we do so with positive and negative integers at each index?
            # If nums[1] > nums[0], we could have a positive integer 2
            # And if nums[1] < nums[0] we could have a negative integer 2

            for i in range(j):
                delta = nums[j] - nums[i]
                # First element is a special case; can be considered either positive or negative delta
                if i == 0:
                    if delta > 0:
                        dp[j] = 2
                    elif delta < 0:
                        dp[j] = -2
                    else:
                        dp[i] = 1

                if delta > 0 and dp[i] < 0:
                    dp[j] = max(dp[j], abs(dp[i]) + 1)
                elif delta < 0 and dp[i] > 0:
                    dp[j] = -max(dp[j], dp[i] + 1) # issue is, dp[j] is always dp[i + 1] of prior value, and dp is strictly nondecreasing
                    # since delta cannot simultaneously be positive and negative, one element cannot possibly contribute to multiple subsequence lengths, so
                    # having an array to track state is pointless; only need 2 variables
        
        return abs(max(dp, key=abs))

    # This applies DP to achieve O(n^2). But looking closer, only the latest prior upturns and downturns matter
    # When calculating dp[j] = max(dp[j], abs(dp[i] + 1)) over and over, dp[j] is only ever increasing (prior counts that are not prior peaks are always overwritten)
    # At each step, the operation is binary. Either this current element contributes to a prior subsequence with last step increasing, or last step decreasing (negative and positive deltas respectively)
    
    # DP + Greedy optimization
    def wiggleMaxLength(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return n
        
        max_subsequence_up = 1
        max_subsequence_down = 1
        
        # Key insight is that if we keep on having the same signed delta, we can simply keep the longest subsequence length tracked the same, but now the element being compared to for next difference is higher (want to go higher to improve any chance of negative delta).
        # By combining the local optimal treatment, we only need to track two states (for the two different types of subsequences)
        for i in range(1, n):
            delta = nums[i] - nums[i - 1]
            if delta < 0:
                max_subsequence_down = max_subsequence_up + 1
            elif delta > 0:
                max_subsequence_up = max_subsequence_down + 1
        
        return max(max_subsequence_up, max_subsequence_down)

    
if __name__ == '__main__':
    s = Solution()
    print(s.wiggleMaxLength([1,2,3,4,5,6,7,8,9]))