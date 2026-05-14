class Solution1:
    def minDistance(self, word1: str, word2: str) -> int:
        # horse, ros -> 4x6 matrix
        # * h o r s e
        # r 1
        # o
        # s

        # Key idea 1: we simulate insertion/deletion by adjusting indices within a word
        # For example, ac -> abc comparison is moving j=1 to j=2 without moving i=1
        # Let us have a dp tracking min edits; dp will be (m + 1) x (n + 1)
        # dp[i][j] tracks min edits to transform word1[:i] into word2[:j]

        # update: dp[i][j] = dp[i - 1][j - 1] + 1 (i.e., all prev chars match, char at end of substring is edited)
        # insert into word2 / delete from word1: dp[i][j] = dp[i][j - 1] + 1
        # insert into word1 / delete from word2: dp[i][j] =  dp[i - 1][j] + 1
        # min of these 3 types of operations for each dp[i][j]

        m = len(word2)
        n = len(word1)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        # dp[i][0] represents number of edits for word2 -> ""
        for i in range(1, m + 1):
            dp[i][0] = i
        # dp[0][j] represents number of edits for word1 -> ""
        for j in range(1, n + 1):
            dp[0][j] = j

        for i in range(1, m + 1): # word2
            for j in range(1, n + 1): # word1
                # Two cases; either we find a match and don't use an operation, or we need to use an operation (pick best)
                if word1[j - 1] == word2[i - 1]:
                    # match -> take num_edits as whatever was needed for word1[:j - 1] == word2[:i - 1]
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    best = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
                    dp[i][j] = best + 1

        return dp[-1][-1]


class Solution2:
    def minDistance(self, word1: str, word2: str) -> int:
        # Next, we optimize for space by noticing that dp only takes top left, left, and top cells
        # We can space-optimize this by using 1D dp using the length of the shorter word
        l1 = len(word1)
        l2 = len(word2)
        if l1 > l2:
            # swap so that word1 is always shorter / l1 <= l2
            l1, l2 = l2, l1
            word1, word2 = word2, word1

        dp = [i for i in range(l1 + 1)] # for word1="ros" this would be [0, 1, 2, 3]
        for i in range(1, l2 + 1):
            top_left = dp[0]
            dp[0] = i
            for j in range(1, l1 + 1):
                left = dp[j - 1]
                top = dp[j]
                best = min(left, top_left, top)
                tmp = dp[j] # store for next iteration
                dp[j] = best + 1 if word1[j - 1] != word2[i - 1] else top_left
                top_left = tmp

        return dp[-1]
