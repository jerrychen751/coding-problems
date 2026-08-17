from collections import deque
from typing import List

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        '''
        nxn matrix
        top-left to bottom-right
        all visited cells must be 0; 8-directions

        shortest path is diagonal (or take as many diagonals as possible)
        (a,b) (c,d) -> shortest path dist min(c-a, d-b) + abs((c-a) - (d-b))

        BFS
        queue of elements to explore next
        seen set

        A*
        dist = g(n) + h(n)
        g(n) is actual cost from source to node
        h(n) is estimated cost from node to dest
        max(n - 1 - i, n - 1 - j) where (i, j) is position of node

        '''
        seen = set()
        if grid[0][0] != 0 or grid[-1][-1] != 0:
            return -1

        n = len(grid)
        queue = deque([(0, 0)])
        path_len = 0
        dirs = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < n and j >= 0 and j < n

        while queue:
            path_len += 1
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr in seen:
                    continue
                seen.add(curr)
                i, j = curr
                if i == n - 1 and j == n - 1:
                    return path_len
                for di, dj in dirs:
                    new_i, new_j = i + di, j + dj
                    if (new_i, new_j) in seen or not in_bounds(new_i, new_j) or grid[new_i][new_j] == 1:
                        continue
                    queue.append((new_i, new_j))

        return -1
