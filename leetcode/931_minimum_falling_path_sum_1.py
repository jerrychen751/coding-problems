from typing import List


class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        # Start from second row, move down to last
        # Let dp[i][j] track min sum of any falling path through matrix[:i][:j] i.e. min path from row 0 to row i - 1
        # Ask if we can modify input matrix
        m = len(matrix)
        n = len(matrix[0])
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        for i in range(1, m):
            for j in range(n):
                top_left = matrix[i - 1][j - 1] if in_bounds(i - 1, j - 1) else float('inf')
                top = matrix[i - 1][j]
                top_right = matrix[i - 1][j + 1] if in_bounds(i - 1, j + 1) else float('inf')
                matrix[i][j] += min(top_left, top, top_right)

        return min(matrix[-1])
