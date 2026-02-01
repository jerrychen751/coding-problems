from typing import List

class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        # subarrays can overlap
        # exact same subarray can be used more than once
        # value of subarray is amplitude (diff between max and mean)
        # total value is sum of values of chosen subarrays
        # return max possible value able to be achieved

        # questions
        # can k be zero? -> no
        # are we limited in terms of size of subarrays chosen?
        # how large can the numbers be?
        
        # approach
        # find min/max of all values in nums -> take their difference

        smallest = min(nums)
        largest = max(nums)
        return (largest - smallest) * k