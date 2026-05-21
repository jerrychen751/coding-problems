from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Can sell + buy on same day
        # Can only hold one share at a time
        # Ideally, if we see the price drop the next day, we always sell what we currently have
        # and then buy the next day -> worst case is buy-sell on same day then buy at a lower price again
        # If we see the price rise, we always buy curr price and then sell it at that higher price

        profit = 0
        for i in range(len(prices) - 1):
            curr, nxt = prices[i], prices[i + 1]
            if curr < nxt:
                profit += nxt - curr

        return profit
