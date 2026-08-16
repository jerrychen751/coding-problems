from collections import defaultdict
from typing import List

class UnionFind:
    def __init__(self) -> None:
        self.parent = {} # maps node to parent
        self.size = {} # maps component to its size

    def find(self, node: int) -> int:
        if node not in self.parent:
            self.parent[node] = node
            self.size[node] = 1
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, n1: int, n2: int) -> bool:
        r1 = self.find(n1)
        r2 = self.find(n2)
        if r1 == r2:
            return False

        if self.size[r1] < self.size[r2]:
            r1, r2 = r2, r1
        self.parent[r2] = self.parent[r1]
        self.size[r1] += self.size[r2]
        del self.size[r2]
        return True

class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        '''
        string s
        given sequence of pairs of indices
        swaps allowed
        return smallest string that can be formed

        [[1, 2], [1, 3]]
        indices are interchangeable via swaps
        1, 2, 3 are part of the same group -> order old idx of s into smallest for new string
        cba -> abc -> 321

        union find
        iterate through pairs -> form components of union find

        keep mapping of component to list of indices belonging to that component
            list of indices is in increasing order
        go through lists in dict (iterate through .values())
            obtain letters from s
            sort letters
            for i in range(len(indices)):
                res[indices[i]] = letters[i]

        return "".join(res)

        O(nlogn + am + an)
        '''

        uf = UnionFind()
        n = len(s)
        for i in range(n):
            uf.find(i)

        for u, v in pairs:
            uf.union(u, v)

        component_idx = defaultdict(list)
        for i in range(n):
            root = uf.find(i)
            component_idx[root].append(i)

        res = [char for char in s]
        for indices in component_idx.values():
            # res[i] for i in indices needs to be sorted
            letters = sorted([res[i] for i in indices])
            # if i indexes into both indices and letters, then res[indices[i]] = letters[i]
            for letter, index in zip(letters, indices):
                res[index] = letter

        return "".join(res)
