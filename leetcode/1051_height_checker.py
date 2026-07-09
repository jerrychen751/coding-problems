from typing import List


class Solution:
    def heightChecker(self, heights: List[int]) -> int:
        # sorted order
        # return number of indices where students are not standing in sorted order

        # One idea is just to sort, then compare index by index
        n = len(heights)
        expected = sorted(heights)
        mismatch_ct = 0
        for i in range(n):
            if heights[i] != expected[i]:
                mismatch_ct += 1

        return mismatch_ct
