from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        # binary search, lo, hi, mid
        # if mid < hi then new hi is mid - 1
        # ie over half of right side is sorted so we should move left but also track curr since it might be min
        # if mid > hi then that means theres a rotation and the whole left side is sorted but right is smaller so new lo is mid + 1
        smallest = nums[0]
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[hi]:
                hi = mid - 1
                smallest = min(smallest, nums[mid])
            else:
                lo = mid + 1
                smallest = min(smallest, nums[hi])

        return smallest
