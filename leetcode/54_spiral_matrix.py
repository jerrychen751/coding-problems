from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        spiral = []
        m = len(matrix)
        n = len(matrix[0])

        l, r = 0, n - 1 # range of cols (inclusive) that we can traverse
        t, b = 0, m - 1 # range of rows (inclusive) that we can traverse

        while l <= r and t <= b:
            # traverse matrix[t][l..r]
            for i in range(l, r + 1):
                spiral.append(matrix[t][i])
            t += 1
            # traverse matrix[t..b][r]
            for i in range(t, b + 1):
                spiral.append(matrix[i][r])
            r -= 1
            # traverse matrix[b][r..l]
            if t <= b:
                for i in range(r, l - 1, -1):
                    spiral.append(matrix[b][i])
                b -= 1
            # traverse matrix[b..t][l]
            if l <= r:
                for i in range(b, t - 1, -1):
                    spiral.append(matrix[i][l])
                l += 1

        return spiral
