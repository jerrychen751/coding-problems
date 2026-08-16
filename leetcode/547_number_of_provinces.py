from typing import List


class UnionFind:
    def __init__(self, n: int) -> None:
        self.roots = list(range(n))
        self.sizes = {k: 1 for k in range(n)}
        self.root_ct = n # this is answer at the end after merging all provinces

    def find(self, node: int) -> int:
        if self.roots[node] != node:
            self.roots[node] = self.find(self.roots[node])

        return self.roots[node]

    def union(self, node1: int, node2: int) -> bool:
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 == root2:
            return False

        # Merge the shorter of the two into larger one
        # Let root2 be smaller one consistently
        if self.sizes[root1] < self.sizes[root2]:
            root1, root2 = root2, root1
        self.roots[root2] = root1
        self.sizes[root1] += self.sizes[root2]
        del self.sizes[root2]
        self.root_ct -= 1
        return True

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        '''
        n cities
        not all connected
        a-b, b-c --> a-c indirectly
        province is group of cities; either connected directly or indirectly

        we're given adjacency matrix
        return total number of provinces

        union find data structure
        '''
        n = len(isConnected)
        union_find = UnionFind(n)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    union_find.union(i, j)

        return union_find.root_ct
