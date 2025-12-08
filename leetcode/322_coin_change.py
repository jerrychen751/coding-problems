class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        if amount == 0:
            return 0
        
        # Only consider the coins which contain reasonable values
        valid_coins = [coin for coin in coins if 0 < coin <= amount]

        # Notice that possible coins length is not large and amount is also not that large
        # We want the fewest number of coins to make up target amount, so the state involves tracking coin amounts
        # Index represents that amount reached with some combination of coins
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0 # base case
        for i in range(len(dp)):
            for coin in valid_coins:
                if i - coin >= 0: # only need to consider all possible changes after adding a single coin
                    dp[i] = min(dp[i], dp[i - coin] + 1) # first coin combination found isn't necessary optimal
                    # In the case of coins = [1, 6] and amount = 12, it's possible to find dp[12] = min(float('inf'), dp[11] + 1), but a better solution is dp[6] + 1

        if dp[amount] == float('inf'):
            return -1
        
        return int(dp[amount])
    
if __name__ == '__main__':
    coins = [1, 6]
    amount = 12
    s = Solution()
    print(s.coinChange(coins, amount))