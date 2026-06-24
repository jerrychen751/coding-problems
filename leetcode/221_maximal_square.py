from typing import List


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        # A square of size n + 1 can be formed with top left corner at dp[i][j] if dp[i + 1][j], dp[i + 1][j + 1], and dp[i][j + 1] are of size n
        # and matrix[i][j] is 1

        largest = 0
        m = len(matrix)
        n = len(matrix[0])
        dp = [0 for _ in range(n)] # start with state of last row, iterate right->left bottom->top
        for i in range(m - 1, -1, -1):
            right = 0
            diag = 0
            for j in range(n - 1, -1, -1):
                bottom = dp[j]
                potential = min(right, diag, bottom) + 1
                if matrix[i][j] == '1':
                    dp[j] = potential
                    largest = max(largest, potential)
                else:
                    dp[j] = 0

                diag = bottom
                right = dp[j]

        return largest * largest
