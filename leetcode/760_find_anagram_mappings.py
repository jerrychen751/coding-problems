from typing import List


class Solution:
    def anagramMappings(self, nums1: List[int], nums2: List[int]) -> List[int]:
        indices = {}
        for i, num in enumerate(nums2):
            indices[num] = i

        res = []
        for num in nums1:
            res.append(indices[num])

        return res
