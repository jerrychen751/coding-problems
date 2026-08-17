from typing import List


class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        '''
        0..n-1 nodes
        adj list, graph[i] contains neighbors of i-th node
        no edges = terminal node
        all paths starting from node eventuall end at a terminal node = safe node
        return array of all safe nodes in graph
        terminal node is safe by default

        set of non-safe nodes

        0 -> 1 -> 3 -> 0
        0 -> 2 -> 5

        Postorder DFS, each node 3 states
        -1: unvisited
        0: visiting
        1: visited, this node and all of its outgoing paths/neighbors are fully explored

        if we find node in dfs is already marked as visiting, then all nodes currently with visiting status become non-safe
        '''
        unsafe = set()
        state = {}
        def dfs(node: int) -> bool:
            # True if cycle, false otherwise
            if state.get(node, -1) == 1:
                return False
            if state.get(node, -1) == 0:
                unsafe.add(node)
                return True

            state[node] = 0
            for neighbor in graph[node]:
                if dfs(neighbor):
                    unsafe.add(node)
                    return True

            state[node] = 1
            return False

        for i in range(len(graph)):
            dfs(i)

        return [i for i in range(len(graph)) if i not in unsafe]
