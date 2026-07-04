from collections import Counter

class Solution:
    def minimumDeletions(self, s: str) -> int:
        # We iterate through candidates for the last position of a
        # Count b's before it, a's after it -> becomes deletions required
        n = len(s)
        a_after = 0
        b_before = 0 # counts of letters relative to index i
        for i in range(1, n):
            char = s[i]
            if char == 'a':
                a_after += 1

        min_deletions = a_after + b_before
        for i in range(n):
            min_deletions = min(min_deletions, a_after + b_before)
            if s[i] == 'b':
                b_before += 1
            if i + 1 < n and s[i + 1] == 'a':
                a_after -= 1

        return min_deletions
