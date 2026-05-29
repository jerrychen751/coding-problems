from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        # Cannot rob two adjacent homes
        # Greedy will not work
        # If only 1 house, always rob
        # If two homes, either pick prev choice of robbing first home, or rob second (not both)
        # If 3 homes, either pick prev choice of robbing 2nd home, or money from 1st + 3rd
        # If 4 homes, either pick prev choice of robbing 3rd home (total profit by then) or total from 2nd + 4th
        n = len(nums)
        dp = [0] * (n + 1) # dp[i] = max money taken from first i homes
        dp[1] = nums[0] # 1 home = base case, just rob that one house
        for i in range(1, n):
            num = nums[i]
            best = max(dp[i], dp[i - 1] + num) # two choices; take total up to prev home or take total up to 2 before + this
            dp[i + 1] = best

        return max(dp[-1], dp[-2])
        # This could be further optimized in terms of state to just two prev houses
