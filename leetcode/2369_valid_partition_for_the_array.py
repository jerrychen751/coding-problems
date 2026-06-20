from typing import List


class Solution:
    def validPartition(self, nums: List[int]) -> bool:
        # Seems like a DP problem
        # Three possible valid partitions
        # Just need a single partition and we return True, at the end return False
        # dp[i] is bool tracking whether nums[:i] can have valid partition

        # If dp[i - 2] and nums[i - 2:i] is valid or dp[i - 3] and nums[i - 3:i] is valid it's true
        # otherwise false

        def is_valid(arr: List[int]) -> bool:
            if len(arr) == 2 and arr[0] == arr[1]:
                return True
            if len(arr) == 3 and arr[0] == arr[1] == arr[2]:
                return True
            if len(arr) == 3 and arr[2] - arr[1] == 1 and arr[1] - arr[0] == 1:
                return True

            return False

        n = len(nums)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(2, n + 1):
            if dp[i - 2] and is_valid(nums[i - 2:i]) or dp[i - 3] and is_valid(nums[i - 3:i]):
                dp[i] = True
            else:
                dp[i] = False

        return dp[-1]
