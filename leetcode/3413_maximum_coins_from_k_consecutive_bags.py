from typing import List


class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        '''
        intervals of bags contain same number of coins; intervals are non-overlapping; inclusive bounds
        given an integer k; return max coins obtainable by collecting k consecutive bags

        window must be size k; maximize sum of coins in that window given intervals
        sort based on start; sliding window across coins

        Let the bounds of window end within intervals a and b respectively
        Suppose a.val >= b.val; then greedy approach makes it ok to let window left bound be a.start
        If a.val < b.val; greedy approach makes it ok to let window right bound be b.end
        That means that for every interval x, we can test window start at x.left and end at x.right

        For efficient search, we slide window left -> right for possible interval left bounds
        Then right -> left for possible interval right bounds
        '''
        coins = sorted(coins)
        n = len(coins)
        res = 0 # max window sum

        # Try coin[0] as left edge for intervals
        # Let i, j denote interval indices of interval
        # Let left, right denote coordinate on number line
        j = 0
        win_sum = 0
        for i in range(n):
            if i > 0:
                win_sum -= (coins[i - 1][1] - coins[i - 1][0] + 1) * coins[i - 1][2]

            left = coins[i][0]
            right = left + k - 1
            while j < n and right >= coins[j][1]:
                # Entire coins[j] interval is within window
                win_sum += (coins[j][1] - coins[j][0] + 1) * coins[j][2]
                j += 1
            # Deal with partial interval included
            # win_sum should track full windows; curr_sum tracks win_sum + any partial interval
            curr_sum = win_sum
            if j < n and right >= coins[j][0]:
                curr_sum += (right - coins[j][0] + 1) * coins[j][2]

            res = max(res, curr_sum)

        # Try coin[1] as right edge for intervals
        i = n - 1
        win_sum = 0
        for j in range(n - 1, -1, -1):
            if j < n - 1:
                win_sum -= (coins[j + 1][1] - coins[j + 1][0] + 1) * coins[j + 1][2]

            right = coins[j][1]
            left = right - k + 1
            while i >= 0 and left <= coins[i][0]:
                win_sum += (coins[i][1] - coins[i][0] + 1) * coins[i][2]
                i -= 1
            curr_sum = win_sum
            # left is somewhere between coins[i][0] and coins[i][1]
            if i >= 0 and left <= coins[i][1]:
                curr_sum += (coins[i][1] - left + 1) * coins[i][2]

            res = max(res, curr_sum)

        return res
