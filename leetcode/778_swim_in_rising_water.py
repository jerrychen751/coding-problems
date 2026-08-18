from collections import deque
from typing import List

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        '''
        grid is elevation for each cell
        time t = water level t
        move to 4-dir adj cells for free, return min time until reaching bottom right square
        find a path from top left to bottom right such that max value in that path is minimized

        grid elements are non-negative, non-empty grid
        Perform BFS, guess a max value in the path, try to see if we can reach end without exceeding max value
        m*n*log(k) where k is max(grid)
        '''
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        m = len(grid)
        n = len(grid[0])
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        def bfs(max_value: int) -> bool:
            queue = deque([(0, 0)])
            seen = set()
            while queue:
                cell = queue.popleft()
                if cell in seen:
                    continue
                seen.add(cell)
                i, j = cell
                if i == m - 1 and j == n - 1:
                    return True

                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if (ni, nj) in seen or not in_bounds(ni, nj) or grid[ni][nj] > max_value:
                        continue
                    queue.append((ni, nj))

            return False

        lo = max(grid[0][0], grid[-1][-1])
        hi = max(max(row) for row in grid)
        best = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if bfs(mid):
                best = mid
                hi = mid - 1
            else:
                lo = mid + 1

        return best
