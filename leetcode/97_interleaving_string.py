class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False

        # Ensure m <= n, or that len(s1) <= len(s2)
        # i indexes m, j indexes n
        if len(s2) < len(s1):
            s1, s2 = s2, s1

        m = len(s1)
        n = len(s2)

        # Optimize for 1D DP
        # dp[i] on j-th iteration represents whether first i letters of s1 and j letters of s2 can be used to compose s3[:i+j]
        dp = [False for _ in range(m + 1)]
        dp[0] = True
        for i in range(1, m + 1):
            dp[i] = True if (dp[i - 1] and s1[i - 1] == s3[i - 1]) else False
        
        for j in range(1, n + 1):
            dp[0] = True if (dp[0] and s2[j - 1] == s3[j - 1]) else False
            for i in range(1, m + 1):
                dp[i] = (dp[i - 1] and s1[i - 1] == s3[i + j - 1]) or (dp[i] and s2[j - 1] == s3[i + j - 1])

        return dp[-1]

        '''
        # Set up base case for DP
        dp[0][0] = True
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
        
        return dp[-1][-1]        
        '''

        

        '''
        # See if s3 is formed by interleaving s1 and s2
        # s1, s2 are divided into n and m substrings
        # n and m differ by at most 1
        # interleaving is concatenation of substrings where adjacent substrings are from different source

        # Is len(s3) = len(s1) + len(s2)?
        
        if len(s3) != len(s1) + len(s2):
            return False

        # At each step, we have the option of using s1 or s2 char
        # If we can use both, then diverge down either path
        # If one of the chars doesn't match, we automatically try other
        # If both don't work, then we return false
        # If both work, then diverge down either path and OR the results together

        # There would be 2^k ways to reach each state if not memoized
        # Store keys as (i, j)
        # memo[(i, j)] indicates whether (i, j) can form s3 via interleaving
        
        # Form dp table of the smaller length
        # len(s1) <= len(s2) always

        memo = {}

        def canInterleave(i: int, j: int) -> bool:
            # Base case
            if i + j >= len(s3):
                return True
            if i >= len(s1):
                return s2[j:] == s3[i+j:]
            if j >= len(s2):
                return s1[i:] == s3[i+j:]
            
            # Check memoized results
            if (i, j) in memo:
                return memo[(i, j)]
            
            # First, check whether both work
            if s1[i] == s2[j] == s3[i + j]:
                memo[(i, j)] = canInterleave(i + 1, j) or canInterleave(i, j + 1)
            elif s1[i] == s3[i + j]:
                memo[(i, j)] = canInterleave(i + 1, j)
            elif s2[j] == s3[i + j]:
                memo[(i, j)] = canInterleave(i, j + 1)
            else:
                memo[(i, j)] = False
            
            return memo[(i, j)]
        
        return canInterleave(0, 0)
                
            
        '''