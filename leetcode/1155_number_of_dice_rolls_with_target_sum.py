class Solution:
    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        # n dice, k possible values for dice from 1..k
        # find number of ways to reach target
        # let dp[i][j] = number of ways to reach sum of j rolling i number of k-faced dice
        # (n + 1) x (target + 1) dims
        # dp[i][j] = dp[i - 1][j - 1..k] + 1..k
        # k sided die information is encoded in number of ways to reach sum of j
        # Instead of having a third nested loop we maintain a sliding window
        # dp[n][target] is final answer

        # Since we only rely on the previous row for 2D DP matrix, we can optimize to 1D DP

        m = n + 1
        n = target + 1
        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = 1
        for i in range(1, m):
            win_start, win_end = 0, 0
            win_sum = dp[i - 1][0]
            for j in range(1, n):
                dp[i][j] = win_sum
                if win_end - win_start + 1 == k:
                    win_sum -= dp[i - 1][win_start]
                    win_sum %= (10**9 + 7)
                    win_start += 1
                win_end += 1
                win_sum += dp[i - 1][win_end]
                win_sum %= (10**9 + 7)

        return dp[-1][-1]

        # inner loop is finding sum of subarray; sliding window
        # window of length k, where initially it's length is less than k starting from 1
