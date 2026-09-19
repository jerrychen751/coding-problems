from functools import cache


class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        best = float('inf')
        def is_pow(x: int, base: int) -> bool:
            if x < 1:
                return False

            while x % base == 0:
                x //= base

            return x == 1

        n = len(s)
        # Let dp(i) be min number of beautiful substrings of s[i:]
        # Then dp(i) = 1 + dp(j) minimized over all j as long as s[i:j] is a power of 5
        # O(n^2) at most

        @cache
        def dp(i: int) -> float:
            """
            Return min beautiful substrings in s[i:].
            """
            if i >= n:
                return 0
            if int(s[i]) == 0:
                return float('inf')

            num = 0
            best = float('inf') # min of dp(j) where j > i and int(s[i:j + 1], 2) is divisible by 5
            for j in range(i, n):
                num = (num << 1) | int(s[j])
                if is_pow(num, 5):
                    best = min(best, dp(j + 1))

            return best + 1

        res = dp(0)
        if res == float('inf'):
            return -1
        return int(res)
