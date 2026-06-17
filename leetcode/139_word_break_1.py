from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Iterate through s, if we find a match with a word in wordDict accept that, backtrack if it doesn't work out to try to match to a longer word
        # Words in dictionary can be used with replacement

        # Let dp[i] be whether s[:i] can be segmented into a space-separated sequence of wordDict's words
        # dp[i] is True if for any j=0..i-1 s[j + 1:i] is in wordDict
        # Turn wordDict into a set for fast checks
        # If dp[-1] is True, then that means entire string can be segmented
        # dp is of length n + 1

        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True # empty string can be split
        word_set = set(wordDict)
        for i in range(1, n + 1):
            for j in range(0, i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break

        return dp[-1]
