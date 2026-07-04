class Solution:
    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        # 8 dirs
        # nxn chessboard
        # always moves in L shape
        # starts at different (row, col) cell

        # For each cell, we need prob of staying on board, not just after 1 more step, but k more steps
        # This makes it n x n x k
        # Let dp[i][j][k] represent probability of knight staying on board if it's currently at (i, j) and has k more jumps
        # Then dp[i][j][k] = 1/8 * dp[a][b][k - 1] + ... for all squares a_1, b_1... which is still on the board
        # Base case is k = 1, where it is just p where p is num_valid_jumps / 8

        dp = [[[1 for _ in range(k + 1)] for _ in range(n)] for _ in range(n)] # base case when k=0 is 1; always on board
        dirs = [
            (-1, -2), (-2, -1), (-2, 1), (-1, 2), # top half of moves
            (1, -2), (2, -1), (2, 1), (1, 2) # bottom half of moves
        ]
        def in_bound(i: int, j: int, n: int) -> bool:
            return i >= 0 and i < n and j >= 0 and j < n

        for k in range(1, k + 1):
            for i in range(n):
                for j in range(n):
                    p = 0
                    for di, dj in dirs:
                        p += 1/8 * dp[i + di][j + dj][k - 1] if in_bound(i + di, j + dj, n) else 0

                    dp[i][j][k] = p

        return dp[row][column][k]
