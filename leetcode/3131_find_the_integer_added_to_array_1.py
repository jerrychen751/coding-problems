from typing import List

class Solution:
    def addedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        # Approach:
        # Sort the two arrays; if adding the same value to each one then relative ordering doesn't change
        # Return the difference between element at same index in both arrays (num2[i] - num1[i])

        # Optimization step:
        # Since we really only need the difference between a single index in either array, we can just find the min/max element in both and then take the difference
        # O(max(len(nums1), len(nums2))) time (find min of both arrays)
        # O(1) space

        return min(nums2) - min(nums1)