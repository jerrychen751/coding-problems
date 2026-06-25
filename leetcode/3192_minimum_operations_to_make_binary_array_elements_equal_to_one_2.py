from typing import List


class Solution:
    def minOperations(self, nums: List[int]) -> int:
        # We are able to flip identities of nums[i:]

        n = len(nums)

        # The base case / greedy solution is achieved moving left -> right
        # Because we flip from i..n-1, the only possible way a 0 at index i an be flipped is if we flip it there and then
        # Then we only need to track parity of flips along with identity of nums[j]
        # If nums[j] == 0 and flip is odd, then it's actually 1 and vice versa
        flips = 0 # num flips to ensure 0..i-1 are all 1's
        for i in range(n):
            x = nums[i]
            if x == 0 and flips & 1 == 0:
                flips += 1
            elif x == 1 and flips & 1 == 1:
                flips += 1

        return flips
