import math
from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # Make a copy of the first n - k elements, store in separate array, where n is length of nums
        # Copy last k elements to the front of nums
        # Store each element in copy to the end of nums

        # There should be a smarter way to do this
        # The issue is that we need to keep track of elements which are displaced once a rotated element goes in their spot
        # To obtain an in-place solution we need to place that displaced element immediately into its new spot
        # We repeat this until we notice a cycle; i.e., a displaced element is trying to go into another already-displaced element's spot
        def replace(start: int, new_val: int, new_idx: int, k: int, nums: List[int]) -> None:
            while new_idx != start:
                displaced_num = nums[new_idx]
                nums[new_idx] = new_val

                new_idx = (new_idx + k) % len(nums)
                new_val = displaced_num
            
            nums[start] = new_val
            

        n = len(nums)
        gcd = math.gcd(n, k)
        for i in range(gcd):
            replace(i, nums[i], (i + k) % n, k, nums)

        

        """
        # Method 1
        n = len(nums)

        if k % n == 0:
            return

        k = k % n
        last_k = nums[-k:]
        for i in range(n - k - 1, -1, -1):
            nums[i + k] = nums[i]
        
        nums[:k] = last_k
        """