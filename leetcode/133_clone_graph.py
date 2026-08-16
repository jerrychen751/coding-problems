from collections import deque

"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        '''
        given a graph, represented as Node object
        undirected, so if n1 and n2 are neighbors, then n2 is in n1.neighbors and n1 is in n2.neighbors
        return a copy of the given node

        BFS, queue to contain all nodes that we want to explore neighbors of next
        store a set containing values of nodes that we've seen before, so when processing a node's neighbors we don't re-append
        have a hash map mapping node val to node reference for new graph

        queue = [node]
        map[node.val] = Node(node.val, [])
        while queue:
            pop first element in queue, process it
            if finalized, continue to next iteration (neighboring connection alr added to curr node)
            for each neighbor:
                skip if finalized alr
                add to queue
                if neighbor.val in map:
                    map[neighbor.val].neighbors.append(curr)
                else:
                    map[neighbor.val] = Node(neighbor.val, [curr])
                map[curr.val].neighbors.append(map[neighbor.val])

            finalize curr node

        return map[node.val]
        '''

        if node is None:
            return None

        finalized = set()
        mapping = {node.val: Node(node.val)} # val of node to Node reference where ref is new graph
        queue = deque([node])

        while queue:
            curr = queue.popleft()
            if curr.val in finalized:
                continue

            for neighbor in curr.neighbors:
                if neighbor.val in finalized:
                    continue

                if neighbor.val not in mapping:
                    mapping[neighbor.val] = Node(neighbor.val)
                mapping[neighbor.val].neighbors.append(mapping[curr.val])
                mapping[curr.val].neighbors.append(mapping[neighbor.val])
                queue.append(neighbor)

            finalized.add(curr.val)

        return mapping[node.val]
