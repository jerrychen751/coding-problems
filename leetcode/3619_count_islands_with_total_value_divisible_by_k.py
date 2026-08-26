from collections import deque
from typing import List


class Solution:
    def countIslands(self, grid: List[List[int]], k: int) -> int:
        '''
        Flood-fill BFS, sum elements mod k, avoid large ints by continually modding
        Maintain total count of islands fulfilling property
            If at end of queue / island and fulfill, increment count, otherwise not
        return final count
        '''
        m = len(grid)
        n = len(grid[0])
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n
        visited = [[False for _ in range(n)] for _ in range(m)]
        num_islands = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] <= 0 or visited[i][j]:
                    continue
                total = 0
                queue = deque([(i, j)])
                while queue:
                    r, c = queue.popleft()
                    if visited[r][c]:
                        continue
                    visited[r][c] = True
                    total += grid[r][c]
                    total %= k
                    for di, dj in dirs:
                        ni, nj = r + di, c + dj
                        if in_bounds(ni, nj) and not visited[ni][nj] and grid[ni][nj] > 0:
                            queue.append((ni, nj))
                if total == 0:
                    num_islands += 1
        return num_islands
