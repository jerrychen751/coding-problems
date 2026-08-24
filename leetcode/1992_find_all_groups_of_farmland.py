from typing import List


class Solution:
    def findFarmland(self, land: List[List[int]]) -> List[List[int]]:
        '''
        0 = forest, 1 = farm
        groups are 4-dir connected farmland
        groups can be represented with [r1, c1, r2, c2] where (r1, c1) is top left corner and (r2, c2) is bottom right corner
        return a list of groups of farmland represented this way

        Iterate left -> right, top -> bottom for each cell (top-left candidates):
            if cell is forest or visited already, continue
            otherwise this is candidate for top left corner so we record (r1, c1)
            iterate from r1..m - 1 and c1..n - 1 to find r2 and c2 (largest values still farmland)
            that is bottom corner
            record [r1, c1, r2, c2]
        return result

        To efficiently determine whether we're upon a new top-left corner, there needs to be no farmland
        to the left/top of the current cell (otherwise it belongs to a group rather than top-left corner)
        '''
        m = len(land)
        n = len(land[0])
        def in_bounds(i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n
        res = []
        for i in range(m):
            for j in range(n):
                # Land is forest
                if land[i][j] == 0:
                    continue
                left_forest = not in_bounds(i, j - 1) or land[i][j - 1] == 0
                top_forest = not in_bounds(i - 1, j) or land[i - 1][j] == 0
                # Land is part of another group of farmland
                if not (left_forest and top_forest):
                    continue
                r1, c1 = i, j
                r2, c2 = i, j
                while r2 + 1 < m and land[r2 + 1][j] == 1:
                    r2 += 1
                while c2 + 1 < n and land[r2][c2 + 1] == 1:
                    c2 += 1
                res.append([r1, c1, r2, c2])
        return res
