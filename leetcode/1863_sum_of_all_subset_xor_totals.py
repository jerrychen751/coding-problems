from typing import List


class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        # Track curr state as idx + curr_xor
        # At each step we can either include number in subset or exclude number
        # If include, then we take curr_xor and XOR it with nums[idx] and then contribute to total
        # Otherwise just call next anyways?

        # Returns the subset XOR sum achievable given some path of decisions from 0..i-1 (all posibilities from i..n-1 covered in return value)
        def backtrack(idx: int, curr_xor: int) -> int:
            if idx == len(nums):
                return curr_xor
            
            # either include or exclude
            return backtrack(idx + 1, curr_xor ^ nums[idx]) + backtrack(idx + 1, curr_xor)
        
        return backtrack(0, 0)
