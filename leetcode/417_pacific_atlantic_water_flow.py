from collections import deque
from typing import List

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        '''
        mxn
        pacific is top/left
        atlantic is bottom/right

        heights[i][j] represents sea level at i, j
        neighbors are 4-directional
        water flows to neighboring cells if neighbor height is <= curr cell height
        borders are treated as -inf; water always goes to border

        returning 2d list; list of [i, j] where water from cell i,j can reach both pacific and atlantic

        BFS
        queue, set of seen values
        queue stores all cell positions that can reach a specific ocean
        '''
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        m = len(heights)
        n = len(heights[0])
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        def bfs(queue: deque) -> set[tuple[int, int]]:
            seen = set()
            while queue:
                curr = queue.popleft()
                if curr in seen:
                    continue
                seen.add(curr)
                i, j = curr
                for di, dj in dirs:
                    new_i, new_j = i + di, j + dj
                    if (new_i, new_j) in seen:
                        continue
                    if in_bounds(new_i, new_j) and heights[new_i][new_j] >= heights[i][j]:
                        queue.append((new_i, new_j))

            return seen

        pacific_q = deque()
        atlantic_q = deque()
        for i in range(m):
            pacific_q.append((i, 0))
            atlantic_q.append((i, n - 1))
        for j in range(n):
            pacific_q.append((0, j))
            atlantic_q.append((m - 1, j))

        pacific_reachable = bfs(pacific_q)
        atlantic_reachable = bfs(atlantic_q)
        return [list(cell) for cell in pacific_reachable.intersection(atlantic_reachable)]
