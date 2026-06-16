class Solution:
    def numDecodings(self, s: str) -> int:
        # Start from back
        # Can always contribute 1x
        # Move left; if next value is between 1-2 and prev value is 0-6 then we can either interpret as single or two digit letter
        # Let dp[i] represent number of ways to decode s[i:]
        # dp[i] = dp[i + 1] + dp[i + 2] if s[i] between 1-2 and s[i + 1] between 0-6 else dp[i + 1]
        n = len(s)
        if s[0] == '0':
            return 0
        if n == 1:
            return 1

        dp = [1] * (n + 1)
        dp[-1] = 1
        dp[-2] = 0 if s[-1] == '0' else 1
        for i in range(n - 2, -1, -1):
            n_decodings = 0
            if s[i] != '0':
                n_decodings += dp[i + 1]
                if '10' <= s[i:i + 2] <= '26':
                    n_decodings += dp[i + 2]

            dp[i] = n_decodings

        return dp[0]
