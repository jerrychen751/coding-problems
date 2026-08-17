from collections import deque
from typing import List


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        '''
        return dist of nearest 0 for each cell
        dist for two cells sharing common edge is 1

        all elements
        output is matrix of same shape of dists
        if mat[i][j] == 0, then res[i][j] = 0
        neighbors are 4-connected component
        not all 1's

        dist(i, j)
            if mat[i][j] == 0:
                return 0
            return min(dist(for each neighbor))

        Use BFS, maintain a queue of cell positions where we can confidently determine min dist to 0
        Process each cell in queue
            if zero, res[i][j] = 0, deal with neighbors
            otherwise take min of 4 neighbors
            append neighbors

        we're guaranteed that any node in queue, we can determine the real min dist to 0 using neighbors
        it's possible some neighbor's dist to 0 is not finalized, but that neighbor is guarantee to not be smallest neighbor so doesn't affect answer

        O(nm) time, O(nm) space
        '''
        m = len(mat)
        n = len(mat[0])
        res = [[float('inf') for _ in range(n)] for _ in range(m)]
        queue = deque()
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    queue.append((i, j))
                    res[i][j] = 0

        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        while queue:
            i, j = queue.popleft() # queue is finalized elements only
            curr = res[i][j]
            for di, dj in dirs:
                new_i, new_j = i + di, j + dj
                if not in_bounds(new_i, new_j) or res[new_i][new_j] <= curr + 1:
                    continue
                res[new_i][new_j] = curr + 1
                queue.append((new_i, new_j))

        return res
