from typing import List


class UnionFind:
    def __init__(self, m: int, n: int) -> None:
        self.root = {}
        self.size = {}
        self.not_enclosed = {} # val is True is region doesn't need to change, otherwise turn it to X
        self.m = m
        self.n = n

    def find(self, node: tuple[int, int]) -> tuple[int, int]:
        if node not in self.root:
            self.root[node] = node
            self.size[node] = 1
            i, j = node
            self.not_enclosed[node] = (i == 0 or i == self.m - 1 or j == 0 or j == self.n - 1)
        if self.root[node] != node:
            self.root[node] = self.find(self.root[node])
        return self.root[node]

    def union(self, n1: tuple[int, int], n2: tuple[int, int]) -> bool:
        r1 = self.find(n1)
        r2 = self.find(n2)
        if r1 == r2:
            return False
        # r2 is smaller tree
        if self.size[r1] < self.size[r2]:
            r1, r2 = r2, r1
        self.root[r2] = self.root[r1]
        self.size[r1] += self.size[r2]
        self.not_enclosed[r1] |= self.not_enclosed[r2]
        del self.size[r2]
        del self.not_enclosed[r2]
        return True

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        '''
        'X' and 'O'
        4-dir connections
        'O' forms regions
        O region is surrounded if NONE of the O's are on the edge of the board
        If O region is surrounded by X, it should be converted to X

        region has multiple (i, j)
        if min i of all positions is 0 or max i is m - 1 or min_j is 0 or max_j is n - 1 -> region should not get replaced

        mapping of cell position to parent
        mapping of component id to size
        mapping of component id to a boolean for whether it's fully enclosed or not
        '''
        m = len(board)
        n = len(board[0])
        uf = UnionFind(m, n)
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'X':
                    continue
                left = (i, j - 1) if j - 1 >= 0 and board[i][j - 1] == 'O' else None
                top = (i - 1, j) if i - 1 >= 0 and board[i - 1][j] == 'O' else None
                if left is not None:
                    uf.union((i, j), left)
                if top is not None:
                    uf.union((i, j), top)

        for i in range(m):
            for j in range(n):
                if board[i][j] == 'X':
                    continue
                cell = (i, j)
                root = uf.find(cell)
                if not uf.not_enclosed[root]:
                    board[i][j] = 'X'
