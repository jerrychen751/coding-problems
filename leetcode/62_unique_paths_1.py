from math import factorial

class MathSolution:
    def uniquePaths(self, m: int, n: int) -> int:
        return factorial(m + n - 2) // (factorial(m - 1) * factorial(n - 1))
    
class DynamicProgrammingSolution:
    def uniquePaths(self, m: int, n: int) -> int:
        # dp[m - 1][n - 1] gives the desired answer
        dp = [[0 for _ in range(n)] for _ in range(m)] # dp[i][j] represents the number of ways to arrive at grid[i][j]
        dp[0][0] = 1 # base case for starting position

        for i in range(m):
            for j in range(n):
                # dp[i][j] = dp[i - 1][j] + dp[i][j - 1], as long as both are within bounds
                if self._isValid(i - 1, j, m, n):
                    dp[i][j] += dp[i - 1][j]
                if self._isValid(i, j - 1, m, n):
                    dp[i][j] += dp[i][j - 1]
        
        return dp[m - 1][n - 1]
    
    def _isValid(self, row: int, col: int, m: int, n: int) -> bool:
        return 0 <= row < m and 0 <= col < n
    
if __name__ == '__main__':
    s = DynamicProgrammingSolution()
    print(s.uniquePaths(3, 7))