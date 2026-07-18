class Solution:
    def numTrees(self, n: int) -> int:
        # Let f(n) = num of unique BST structures built from n nodes
        # Let i be node that is root
        # Its left and right subtrees would have f(i - 1) and f(n - i) ways of being built independently
        # Combining them is cartesian product
        # f(n) = sum from i=1 to n of [f(i - 1) * f(n - i)]
        # Cache prev values with dp array

        dp = [1] * (n + 1)
        for x in range(1, n + 1):
            total_ways = 0
            for i in range(1, x + 1):
                total_ways += dp[i - 1] * dp[x - i]
            
            dp[x] = total_ways
        
        return dp[n]
