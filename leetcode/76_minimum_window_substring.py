from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_freqs = Counter(t)
        s_freqs = defaultdict(int)

        required = len(t_freqs)
        formed = 0
        i, j = 0, 0
        best_i, best_j = 0, 0
        min_size = float("inf")

        while j < len(s):
            char = s[j]
            s_freqs[char] += 1
            if char in t_freqs and s_freqs[char] == t_freqs[char]:
                formed += 1
            j += 1

            while formed == required:
                if j - i < min_size:
                    min_size = j - i
                    best_i, best_j = i, j

                char = s[i]
                if char in t_freqs and s_freqs[char] == t_freqs[char]:
                    formed -= 1
                s_freqs[char] -= 1
                i += 1

        return s[best_i:best_j]
