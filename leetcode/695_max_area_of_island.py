from collections import deque
from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        '''
        Find max area of any island in grid -> BFS flood-fill while tracking largest island

        for each cell in grid:
            if water or visited, continue
            island_area = 0 (initialize)
            add cell to queue (BFS)
            while queue:
                pop cell, mark cell visited, append neighbors to queue if not water and not visited
                increment island area
            check if island_area beats max tracked so far; update if so
        return max_island_area
        '''
        m = len(grid)
        n = len(grid[0])
        visited = [[False for _ in range(n)] for _ in range(m)]
        max_area = 0
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0 or visited[i][j]:
                    continue
                area = 0
                queue = deque([(i, j)])
                while queue:
                    i, j = queue.popleft()
                    if visited[i][j]:
                        continue
                    visited[i][j] = True
                    area += 1
                    for di, dj in dirs:
                        ni, nj = i + di, j + dj
                        if in_bounds(ni, nj) and not visited[ni][nj] and grid[ni][nj] == 1:
                            queue.append((ni, nj))

                max_area = max(max_area, area)
        return max_area
