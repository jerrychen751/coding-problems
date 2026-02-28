from typing import List

class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        # 3 stones: [1, 2, 3]
        # We can either combine 1, 2 -> [1, 3]
        # Or we can combine 1, 3 -> [2, 2]
        # Or we can combine 2, 3 -> [1 ,1]

        # At each smash, one stone is positive and one stone is negative
        # We seek to obtain subsets P, N such that |P - N| is minimized, with constraint P + N = sum(stones)
        # I.e., we want P to be as close to total // 2 as possible
        # We can return min(total - P, P) where P is the closest attainable subgroup sum to total // 2
        
        total = sum(stones)
        target = total // 2
        dp = [False] * (target + 1) # dp[i] contains whether i as a subgroup sum is attainable
        dp[0] = True

        for stone in stones:
            for i in range(len(dp) - 1, stone - 1, -1):
                dp[i] = dp[i] or dp[i - stone]
        
        i = len(dp) - 1
        while not dp[i]:
            i -= 1
        
        return abs(i - (total - i)) # abs(P - N)

        # stones = [2, 7, 4, 1, 8, 1]
        # total = 23
        # target = 11
        # dp = [T, F, T, F, T, F, T, T, F, T, F, T]
