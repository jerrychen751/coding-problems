import heapq
from collections import defaultdict
from typing import List


class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int, end_node: int) -> float:
        '''
        0..n-1
        may not be able to traverse from start to end (not fully connected graph)
        succProb[i] may be 0
        start/end are different nodes

        factorial time for DFS searches
        dijkstra with max-heap for probabilities

        probs = {} # maps node to probability of reaching node from start
        # start: 1, everything else: 0
        min_heap = [(-1, start)] # (-prob, node)
        finalized = set() # set of nodes

        while min_heap:
            pop top element in heap
            continue if finalized
            finalize node
            check if finalized node if end_node:
                if so, return prob
            for each neighbor:
                skip if finalized
                neigbor_prob = curr_prob * edge_weight
                if neighbor_prob > probs[neighbor]:
                    update probs
                    push to min_heap

        return 0
        '''
        # build the graph
        graph = defaultdict(list) # node: [(neighbor, prob)]
        edge_ct = len(edges)
        for i in range(edge_ct):
            u, v = edges[i]
            prob = succProb[i]
            graph[u].append((v, prob))
            graph[v].append((u, prob))

        probs = {} # maps node to probability of reaching node from start
        for i in range(n):
            probs[i] = 0
        probs[start_node] = 1
        min_heap = [(-1, start_node)] # (-prob, node)
        finalized = set() # set of nodes

        while min_heap:
            prob, node = heapq.heappop(min_heap)
            prob = -prob
            if node in finalized:
                continue
            finalized.add(node)
            if node == end_node:
                return prob

            for neighbor, neighbor_prob in graph[node]:
                if neighbor in finalized:
                    continue
                new_prob = prob * neighbor_prob
                if new_prob > probs[neighbor]:
                    probs[neighbor] = new_prob
                    heapq.heappush(min_heap, (-new_prob, neighbor))

        return 0
