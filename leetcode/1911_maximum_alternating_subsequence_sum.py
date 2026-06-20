import random
from typing import List


class Solution1:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        # Imagine sorting nums by abs magnitude, from largest to smallest
        # Then take indices 0..n//2, square them, subtract squares of n//2 + 1..n-1
        n = len(nums)

        nums = sorted([x * x for x in nums])
        k = n // 2
        return sum(nums[k:]) - sum(nums[:k])


class Solution2:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        # Alternatively basically find the value at n//2 index here, and then partition array so that
        # all values to left are smaller, all values to right are larger, in no particular order within partition
        # This is an application of quickselect sort
        n = len(nums)

        # Consider an array, start with whole array nums
        # pick a random element
        # partition array around element, place element at its location where it would go if sorted based on abs value
        # if element at idx n // 2, we have found answer -> sum from n // 2 to end and then subtract 0..n//2 - 1
        # if element at idx < n // 2, count up 0..idx in "subtract" var and then repeat with adjusted bounds

        def calc_max_alt_sum(start: int, end: int, sub: int, add: int) -> int:
            # No other number was n//2 up to this point, so this must be number at that idx if array was sorted by abs magnitude
            if start == end:
                return nums[start] + add - sub

            pivot_idx = random.randint(start, end)
            pivot = nums[pivot_idx]
            nums[start], nums[pivot_idx] = nums[pivot_idx], nums[start]
            i, j = start + 1, end
            while True:
                while i <= j and nums[i] <= pivot:
                    i += 1
                while i <= j and nums[j] >= pivot:
                    j -= 1

                if i >= j:
                    break
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

            nums[start], nums[j] = nums[j], nums[start] # swap pivot back into place
            if j == n // 2:
                return sum(nums[j:end + 1]) - sum(nums[start:j]) + add - sub
            elif j < n // 2:
                return calc_max_alt_sum(
                    j + 1,
                    end,
                    sub + sum(nums[start:j + 1]),
                    add
                )
            else:
                return calc_max_alt_sum(
                    start,
                    j - 1,
                    sub,
                    add + sum(nums[j:end + 1])
                )

        return calc_max_alt_sum(0, n - 1, 0, 0)
