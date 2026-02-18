class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        # Approach
        # Use two pointers starting from the end, moving to the front
        # At each index, compare the two letters. If it is a valid char (not '#'), then keep moving if they are the same, or return false immediately if they are different.
        # If it is a '#', then we should move that pointer forward until it lands on a normal char. If we meet more hashtags, then we need to keep track of how many times we need to keep moving forward with a counter until that counter is 0 and we are on normal char.

        # If at any point one pointer goes negative (went through whole string) and other pointer is not negative, then we failed to match. If both become negative at the same time, then we have found a full match

        # O(n) time, O(1) space

        def decrement(s: str, i: int) -> int:
            """Return the next index to compare for string s."""
            if s[i] != '#':
                return i

            skips = 0
            while i >= 0:
                if s[i] == '#':
                    skips += 1
                elif skips > 0:
                    skips -= 1
                else:
                    break # found char idx to stop at
                i -= 1
            return i # -1 if nothing remains
                

        i, j = len(s) - 1, len(t) - 1 # tracks index
        while True:
            i = decrement(s, i)
            j = decrement(t, j)
            if i < 0 and j < 0:
                return True
            if i < 0 or j < 0 or s[i] != t[j]:
                return False

            i -= 1
            j -= 1