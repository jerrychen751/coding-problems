class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        # At each step, we can add string length by either zero or one (not actually 0/1 but rather values of these variables)
        # Final string length must be between low and high
        # Return number of different strings satisfying this length requirement constructed this way

        # Compress the string representation into a bitstring
        # For example, if zero=1 and one=2, then 01 would be "011"
        # Say that for a bitstring of length l, there were x ways to form a good string. then, for a bitstring of length l + 1, there are 2x ways if adding either 0 or 1 would work (i.e., low <= l <= high AND low <= l + zero <= high AND low <= l + one <= high)
        # Let dp[i] represent number of ways to build string of length i
        # dp[i] = dp[i - zero] + dp[i - one]
        # answer would be sum(dp[low:high + 1]) mod (10^9 + 7)

        dp = [0] * (high + 1)
        dp[0] = 1 # base case; we can form string length 0 exactly 1 way
        for i in range(1, high + 1):
            # track number of ways to form string i - zero / i - one
            ways_0 = dp[i - zero] if i - zero >= 0 else 0
            ways_1 = dp[i - one] if i - one >= 0 else 0
            dp[i] = (ways_0 + ways_1) % (10**9 + 7)

        res = 0
        for i in range(low, high + 1):
            res += dp[i]
            res %= (10**9 + 7)

        return res
