from typing import List


class Solution:
    def maxSumMinProduct(self, nums: List[int]) -> int:
        '''
        2 monotonic stacks: left and right
        left[i] stores index of nearest strictly smaller element on left side; opposite with right[i]
        Iterate over min-element candidates; for i in 0..n-1, pretend like nums[i] is the smallest element in subarray
        and try expanding outward as much as we can until we reach a smaller element on left/right sides

        Finding sum of subarray is O(1) using prefix sum
        Finding indices of smaller value on left and right is O(1) using monotonic stack
        O(n) overall
        '''
        n = len(nums)
        prefix_sum = nums.copy()
        for i in range(1, n):
            prefix_sum[i] += prefix_sum[i - 1]

        left = [-1] * n # -1 is marker that there is no smaller element on left
        right = [n] * n # nums[i + 1:right[i]] is included in subarray as right partition
        stack = [] # monotonically increasing indices + values for left
        # decreasing indices + increasing values on right
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()

            if stack:
                # nums[stack[-1]] < nums[i] at this point
                left[i] = stack[-1]

            stack.append(i)

        # left is filled up
        stack.clear()
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()

            if stack:
                right[i] = stack[-1]

            stack.append(i)

        # now right is filled up

        best = float('-inf')
        MOD = 10**9 + 7
        for i in range(n):
            l = left[i]
            r = right[i]
            subarray_sum = prefix_sum[r - 1] if l == -1 else prefix_sum[r - 1] - prefix_sum[l]
            best = max(best, subarray_sum * nums[i])

        return best % MOD
