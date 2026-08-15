from math import ceil
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        piles of len n is number of bananas in each pile
        k is what we return; number of bananas eaten per hour
        have h hours

        while h be at least len(piles)? yes
        h * k >= sum(piles)

        sorting?
        if h == len(piles) -> k = max(piles)
        h is len(piles) + 1 -> k = max(piles[-2], piles[-1] // 2)

        hours taken at rate k = ceil(piles[i]/k) for i in range(len(piles))
        if hrs > h: -> curr k is too small -> increase k
        how to we form lower and upper bound for k? max for k is max(piles), min for k is ceil(sum(piles) / h)

        why can we use binary search on the answer? when a candidate answer is easily testable
        and monotonic

        when k is small, we always get "too slow" / doesn't finish in h hours
        when k is large, we always get "finish"
        we want to find the leftmost "finish" at some k
        answer is easily testable in O(n) time, repeat search logn times for nlogn time
        """
        lo, hi = ceil(sum(piles) / h), max(piles)
        best_k = hi
        while lo <= hi:
            k = lo + (hi - lo) // 2 # test candidate k
            h_taken = sum(ceil(piles[i] / k) for i in range(len(piles)))
            if h_taken > h:
                # too slow
                lo = k + 1
            else:
                # we finished
                best_k = k
                hi = k - 1

        return best_k
