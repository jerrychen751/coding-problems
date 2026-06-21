from typing import List


class Solution:
    def minSumOfLengths(self, arr: List[int], target: int) -> int:
        # Determine min combined length of two non-overlapping subarrays which each sum to target, or return -1 if none exists
        # Prefix sum?
        # No elements are negative
        # Sliding window -> we can adjust depending on sum of window relative to target

        # Maintain i, j which is [start, end] of window
        # Maintain curr_sum of window
        # Maintain two vars s1_len and s2_len; assume that s1_len <= s2_len always
        # If curr_sum == target, compare window size to s1_len and s2_len
        # If curr_sum < target, expand window rightward
        # Otherwise, shrink window leftward

        # At the end return sum of s1_len and s2_len

        if len(arr) == 0 or target < 0:
            return -1

        i, j = 0, 0
        n = len(arr)
        curr_sum = arr[i]
        dp = [float('inf')] * n # dp[i] represents shortest subarray ending at or before index i with target sum
        res = float('inf')
        while j < n:
            window_len = j - i + 1
            if curr_sum == target:
                if i > 0 and dp[i - 1] != float('inf'):
                    res = min(res, dp[i - 1] + window_len)

                dp[j] = window_len

                curr_sum -= arr[i]
                i += 1
            elif curr_sum < target:
                if j + 1 >= n:
                    break

                curr_sum += arr[j + 1]
                j += 1
            else:
                curr_sum -= arr[i]
                i += 1

            if j < i and i < n:
                j = i
                curr_sum += arr[i]

            if j > 0:
                dp[j] = min(dp[j], dp[j - 1])

        return -1 if res == float('inf') else res
