from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        '''
        since all elements are unique, subsets just need to be unique by index chosen
        represent indices chosen to be in subset by 1's in bitstring
        '''
        res = []
        n = len(nums)
        for bits in range(1 << n):
            subset = []
            for i in range(n):
                if bits & (1 << i):
                    subset.append(nums[i])
            res.append(subset)

        return res
