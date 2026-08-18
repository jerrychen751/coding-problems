import heapq
from typing import List

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        '''
        graph via edges
        edge = u, v, w

        w negative? no
        valid input

        dists = {} stores node: shortest known dist from source to node
        min_heap (dist, node)
        finalized = set()

        while min_heap:
            pop min_heap
            process if not finalized
            iterate through neighbors
                skip neighbor if neighbor is finalized
                if dist_to_curr_node + curr_node_to_neighbor_dist < dists[neighbor]:
                    update dists
                    push to min_heap

        check dists; see if any keys were never updated (cannot reach)
        if so, return -1, otherwise return max(dists.values())
        '''
        graph = {}
        for u, v, dist in times:
            if u in graph:
                graph[u].append((v, dist))
            else:
                graph[u] = [(v, dist)]

        dists = {}
        min_heap = [(0, k)] # (dist, node)
        finalized = set()
        for i in range(1, n + 1):
            dists[i] = float('inf')
        dists[k] = 0

        while min_heap:
            dist, node = heapq.heappop(min_heap)
            if node in finalized:
                continue
            finalized.add(node)
            for neighbor, neighbor_dist in graph.get(node, []):
                if neighbor in finalized:
                    continue
                if dist + neighbor_dist < dists[neighbor]:
                    dists[neighbor] = dist + neighbor_dist
                    heapq.heappush(min_heap, (dist + neighbor_dist, neighbor))

        for node, dist in dists.items():
            if dist == float('inf'):
                return -1

        return max(dists.values())
