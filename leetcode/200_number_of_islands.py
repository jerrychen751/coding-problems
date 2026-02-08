from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m = len(grid)
        n = len(grid[0])
        dirs = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        def dfs(i: int, j: int) -> None:
            """
            If grid[i][j] == '0', then we do nothing and immediately return.
            If grid[i][j] == '1', then we change it to 0 and change all surrounding 1's to 0's.
            """
            if i < 0 or i >= m or j < 0 or j >= n:
                return
            if grid[i][j] == '0':
                return
            
            grid[i][j] = '0'
            for di, dj in dirs:
                dfs(i + di, j + dj)
            
        n_islands = 0
        for i in range(m):
            for j in range(n):
                n_islands += int(grid[i][j])
                dfs(i, j)
        
        return n_islands            