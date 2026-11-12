class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        k = 3 # 0=do nothing, 1=buy, 2=sell

        # dp[i][j] = max profix achievable with prices[i:] given action j on day i
        dp = [[0 for _ in range(k)] for _ in range(n)]
        best_profit_after_buying = dp[0][1] - prices[0] # max (dp[j][1] - prices[j]) for j in 0..i-1
        for i in range(1, n):
            cost = prices[i]

            # Do nothing => max profit from prev day; can do anything the previous day (buy, sell, do nothing)
            dp[i][0] = max(dp[i - 1])

            # Buy => forced to do nothing previous day
            dp[i][1] = dp[i - 1][0]

            # Sell => try all previous buy days
            # dp[i][2] = max(dp[j][1] + (prices[i] - prices[j]) for j in 0..i-1)
            # Across all options, prices[i] is fixed and (dp[j][1] - prices[j]) varies; we want the largest over all previous days
            # Keep a running tracker of this value, which represents max profit after buying on some previous day
            dp[i][2] = prices[i] + best_profit_after_buying
            best_profit_after_buying = max(best_profit_after_buying, dp[i][1] - prices[i])

        return max(dp[n - 1])
