from typing import List


class UnionFind:
    def __init__(self, n: int) -> None:
        self.root = {i: i for i in range(1, n + 1)}
        self.size = {i: 1 for i in range(1, n + 1)}

    def find(self, node: int) -> int:
        if node not in self.root:
            self.root[node] = node
            self.size[node] = 1
        if self.root[node] != node:
            self.root[node] = self.find(self.root[node])
        return self.root[node]

    def union(self, n1: int, n2: int) -> bool:
        # If originally in same component, return False
        r1 = self.find(n1)
        r2 = self.find(n2)
        if r1 == r2:
            return False

        if self.size[r1] < self.size[r2]:
            r1, r2 = r2, r1
        self.root[r2] = self.root[r1]
        self.size[r1] += self.size[r2]
        del self.size[r2]
        return True

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        '''
        edges is a list of [a, b] where a,b are two nodes that are connected
        1..n nodes, n nodes

        n nodes, n edges
        no self-loop
        remove last edge in edges which caused graph to not be tree anymore

        all except 1 edge are necessary for all nodes to remain connected
        find and return that one edge

        {1: [2, 3], 2: [1], 3: [1]}
        Try removing each edge, and then running BFS to see how many nodes we can traverse
        N^2 time

        union find
        start off by each node as its own component
        if we go through edges in order, the first edge that doesn't connect two distinct components is the one we
        can safely remove and still have nodes be connected
        aN, N
        '''
        n = len(edges)
        uf = UnionFind(n)
        for u, v in edges:
            if uf.union(u, v):
                continue
            return [u, v]
