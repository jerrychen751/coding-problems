from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # iterate through prices
        # initialize low, high at inf
        # also track best (largest price increase seen so far)
        # each time we see a lower price, we can immediately update low, and also move high down
        # each time we see a higher price, just update high and best

        best = 0
        low = float('inf')

        # At each step, we only care about finding a new minimum or new larger difference between curr element and prior min
        for price in prices:
            low = min(low, price)
            best = max(best, price - low)
        
        return int(best)